#!/usr/bin/env python3
"""Zero-dependency Research Mesh API backed by SQLite."""

import argparse
import json
import mimetypes
import sqlite3
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
DEFAULT_DB = ROOT / "research_mesh.db"


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Store:
    def __init__(self, path=DEFAULT_DB):
        self.path = str(path)
        self.init_db()

    def connect(self):
        db = sqlite3.connect(self.path, timeout=5)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON")
        db.execute("PRAGMA journal_mode=WAL")
        return db

    def init_db(self):
        with self.connect() as db:
            db.executescript("""
            CREATE TABLE IF NOT EXISTS profiles (
              id INTEGER PRIMARY KEY CHECK(id=1), name TEXT NOT NULL,
              affiliation TEXT NOT NULL, offers TEXT NOT NULL, seeking TEXT NOT NULL,
              boundaries TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS memories (
              id INTEGER PRIMARY KEY AUTOINCREMENT, kind TEXT NOT NULL,
              content TEXT NOT NULL, source TEXT NOT NULL, source_ref TEXT,
              is_active INTEGER NOT NULL DEFAULT 1, usage_count INTEGER NOT NULL DEFAULT 0,
              created_at TEXT NOT NULL, updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS sources (
              id INTEGER PRIMARY KEY AUTOINCREMENT, kind TEXT NOT NULL,
              name TEXT NOT NULL, scope TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'connected',
              item_count INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS signals (
              id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT NOT NULL,
              content TEXT NOT NULL, privacy_level TEXT NOT NULL DEFAULT 'anonymous',
              relevance INTEGER NOT NULL DEFAULT 80, actor_name TEXT NOT NULL DEFAULT '匿名研究者',
              created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS matches (
              id INTEGER PRIMARY KEY AUTOINCREMENT, score INTEGER NOT NULL,
              members TEXT NOT NULL, rationale TEXT NOT NULL, agenda TEXT NOT NULL,
              status TEXT NOT NULL DEFAULT 'proposed', created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS feedback (
              id INTEGER PRIMARY KEY AUTOINCREMENT, match_id INTEGER,
              rating INTEGER NOT NULL, useful INTEGER NOT NULL, notes TEXT,
              created_at TEXT NOT NULL, FOREIGN KEY(match_id) REFERENCES matches(id)
            );
            """)
            if not db.execute("SELECT 1 FROM profiles WHERE id=1").fetchone():
                t = now()
                db.execute("INSERT INTO profiles VALUES(1,?,?,?,?,?,?,?)", (
                    "Maya", "米拉研究所 · 博士生",
                    json.dumps(["扩散模型评测", "低资源数据集"], ensure_ascii=False),
                    json.dumps(["机制可解释性", "临床合作者"], ensure_ascii=False),
                    "不聊招聘；偏好聚焦的 20 分钟对谈", t, t))
                memories = [
                    ("need", "正在寻找机制可解释性合作者", "研究笔记", "低资源扩散模型实验记录", 2),
                    ("capability", "可提供低资源临床数据的失败案例", "研究计划", "评测计划 v4", 4),
                    ("boundary", "偏好聚焦的 20 分钟对谈，不接受招聘交流", "手动设置", None, 11),
                ]
                for kind, content, source, ref, uses in memories:
                    db.execute("INSERT INTO memories(kind,content,source,source_ref,usage_count,created_at,updated_at) VALUES(?,?,?,?,?,?,?)",
                               (kind, content, source, ref, uses, t, t))
                for kind, name, scope, count in [
                    ("papers", "论文与研究计划", "已选中的 12 篇文档", 12),
                    ("notes", "私人研究笔记", "NeurIPS 研究文件夹", 19),
                    ("calendar", "日历", "仅空闲状态", 0),
                    ("feedback", "会后匹配反馈", "仅结构化评分", 5),
                ]:
                    db.execute("INSERT INTO sources(kind,name,scope,item_count,created_at) VALUES(?,?,?,?,?)", (kind, name, scope, count, t))
                for typ, content, relevance, actor in [
                    ("demand", "正在寻找真实的扩散模型失败案例，用于验证表征追踪方法。", 94, "Alex"),
                    ("supply", "本周开放两个临床模型评审时段，可提供领域反馈。", 89, "Sofia"),
                    ("info", "关于扩散模型内部表征的新论文被多个智能体标记为高价值。", 86, "论文网络"),
                ]:
                    db.execute("INSERT INTO signals(type,content,relevance,actor_name,created_at) VALUES(?,?,?,?,?)", (typ, content, relevance, actor, t))

    @staticmethod
    def row(row):
        if row is None:
            return None
        data = dict(row)
        for key in ("offers", "seeking", "members", "agenda"):
            if key in data and isinstance(data[key], str):
                data[key] = json.loads(data[key])
        if "is_active" in data:
            data["is_active"] = bool(data["is_active"])
        if "useful" in data:
            data["useful"] = bool(data["useful"])
        return data

    def profile(self):
        with self.connect() as db:
            return self.row(db.execute("SELECT * FROM profiles WHERE id=1").fetchone())

    def update_profile(self, body):
        current = self.profile()
        fields = {k: body.get(k, current[k]) for k in ("name", "affiliation", "offers", "seeking", "boundaries")}
        with self.connect() as db:
            db.execute("UPDATE profiles SET name=?,affiliation=?,offers=?,seeking=?,boundaries=?,updated_at=? WHERE id=1", (
                fields["name"], fields["affiliation"], json.dumps(fields["offers"], ensure_ascii=False),
                json.dumps(fields["seeking"], ensure_ascii=False), fields["boundaries"], now()))
        return self.profile()

    def list_table(self, table, where="", params=()):
        with self.connect() as db:
            rows = db.execute(f"SELECT * FROM {table} {where}", params).fetchall()
            return [self.row(r) for r in rows]

    def list_memories(self, active=None):
        where, params = "ORDER BY updated_at DESC", ()
        if active is not None:
            where, params = "WHERE is_active=? ORDER BY updated_at DESC", (1 if active else 0,)
        return self.list_table("memories", where, params)

    def create_memory(self, body):
        if not body.get("content"):
            raise ValueError("content is required")
        t = now()
        with self.connect() as db:
            cur = db.execute("INSERT INTO memories(kind,content,source,source_ref,created_at,updated_at) VALUES(?,?,?,?,?,?)", (
                body.get("kind", "need"), body["content"], body.get("source", "手动添加"), body.get("source_ref"), t, t))
            row = db.execute("SELECT * FROM memories WHERE id=?", (cur.lastrowid,)).fetchone()
            return self.row(row)

    def update_memory(self, memory_id, body):
        with self.connect() as db:
            old = db.execute("SELECT * FROM memories WHERE id=?", (memory_id,)).fetchone()
            if not old:
                return None
            old = dict(old)
            db.execute("UPDATE memories SET kind=?,content=?,source=?,source_ref=?,is_active=?,usage_count=?,updated_at=? WHERE id=?", (
                body.get("kind", old["kind"]), body.get("content", old["content"]), body.get("source", old["source"]),
                body.get("source_ref", old["source_ref"]), int(body.get("is_active", old["is_active"])),
                int(body.get("usage_count", old["usage_count"])), now(), memory_id))
            return self.row(db.execute("SELECT * FROM memories WHERE id=?", (memory_id,)).fetchone())

    def delete(self, table, item_id):
        with self.connect() as db:
            return db.execute(f"DELETE FROM {table} WHERE id=?", (item_id,)).rowcount > 0

    def create_source(self, body):
        if not body.get("name"):
            raise ValueError("name is required")
        with self.connect() as db:
            cur = db.execute("INSERT INTO sources(kind,name,scope,item_count,created_at) VALUES(?,?,?,?,?)", (
                body.get("kind", "folder"), body["name"], body.get("scope", "用户选择"), int(body.get("item_count", 0)), now()))
            return self.row(db.execute("SELECT * FROM sources WHERE id=?", (cur.lastrowid,)).fetchone())

    def list_signals(self, typ=None, limit=50):
        where, params = "ORDER BY id DESC LIMIT ?", (limit,)
        if typ:
            where, params = "WHERE type=? ORDER BY id DESC LIMIT ?", (typ, limit)
        return self.list_table("signals", where, params)

    def create_signal(self, body):
        if body.get("type") not in ("demand", "supply", "info") or not body.get("content"):
            raise ValueError("type and content are required")
        with self.connect() as db:
            cur = db.execute("INSERT INTO signals(type,content,privacy_level,relevance,actor_name,created_at) VALUES(?,?,?,?,?,?)", (
                body["type"], body["content"], body.get("privacy_level", "anonymous"), int(body.get("relevance", 80)), body.get("actor_name", "Maya"), now()))
            return self.row(db.execute("SELECT * FROM signals WHERE id=?", (cur.lastrowid,)).fetchone())

    def create_match(self):
        members = [
            {"name": "Maya", "role": "失败案例与低资源数据"},
            {"name": "Alex", "role": "机制可解释性"},
            {"name": "Sofia", "role": "临床验证"},
        ]
        agenda = ["展示失败案例", "探查内部机制", "验证真实价值"]
        rationale = "Maya 提供失败案例，Alex 揭示内部成因，Sofia 判断临床价值。"
        with self.connect() as db:
            cur = db.execute("INSERT INTO matches(score,members,rationale,agenda,created_at) VALUES(?,?,?,?,?)", (
                94, json.dumps(members, ensure_ascii=False), rationale, json.dumps(agenda, ensure_ascii=False), now()))
            db.execute("UPDATE memories SET usage_count=usage_count+1,updated_at=? WHERE is_active=1", (now(),))
            return self.row(db.execute("SELECT * FROM matches WHERE id=?", (cur.lastrowid,)).fetchone())

    def create_feedback(self, body):
        rating = int(body.get("rating", 0))
        if rating < 1 or rating > 5:
            raise ValueError("rating must be 1-5")
        with self.connect() as db:
            cur = db.execute("INSERT INTO feedback(match_id,rating,useful,notes,created_at) VALUES(?,?,?,?,?)", (
                body.get("match_id"), rating, int(bool(body.get("useful", True))), body.get("notes"), now()))
            return self.row(db.execute("SELECT * FROM feedback WHERE id=?", (cur.lastrowid,)).fetchone())

    def stats(self):
        with self.connect() as db:
            count = lambda table: db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            return {"memories": count("memories"), "sources": count("sources"), "signals": count("signals"),
                    "matches": count("matches"), "feedback": count("feedback"), "memory_days": 142,
                    "match_precision_gain": 28, "updated_at": now()}


class Handler(BaseHTTPRequestHandler):
    store = None

    def log_message(self, fmt, *args):
        print(f"[api] {self.address_string()} {fmt % args}")

    def send_json(self, data, status=200):
        raw = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,PUT,PATCH,DELETE,OPTIONS")
        self.end_headers()
        self.wfile.write(raw)

    def body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length > 1_000_000:
            raise ValueError("request too large")
        return json.loads(self.rfile.read(length) or b"{}")

    def do_OPTIONS(self):
        self.send_json({}, 204)

    def do_GET(self):
        parsed = urlparse(self.path)
        try:
            if parsed.path == "/api/health": return self.send_json({"ok": True, "database": "sqlite"})
            if parsed.path == "/api/profile": return self.send_json(self.store.profile())
            if parsed.path == "/api/memories": return self.send_json(self.store.list_memories())
            if parsed.path == "/api/sources": return self.send_json(self.store.list_table("sources", "ORDER BY id DESC"))
            if parsed.path == "/api/signals":
                q = parse_qs(parsed.query); return self.send_json(self.store.list_signals(q.get("type", [None])[0]))
            if parsed.path == "/api/matches": return self.send_json(self.store.list_table("matches", "ORDER BY id DESC"))
            if parsed.path == "/api/feedback": return self.send_json(self.store.list_table("feedback", "ORDER BY id DESC"))
            if parsed.path == "/api/stats": return self.send_json(self.store.stats())
            return self.static(parsed.path)
        except Exception as exc:
            self.send_json({"error": str(exc)}, 500)

    def do_POST(self): self.mutate("POST")
    def do_PUT(self): self.mutate("PUT")
    def do_PATCH(self): self.mutate("PATCH")
    def do_DELETE(self): self.mutate("DELETE")

    def mutate(self, method):
        path = urlparse(self.path).path
        try:
            body = {} if method == "DELETE" else self.body()
            parts = [p for p in path.split("/") if p]
            if path == "/api/profile" and method == "PUT": data = self.store.update_profile(body)
            elif path == "/api/memories" and method == "POST": data = self.store.create_memory(body)
            elif len(parts) == 3 and parts[:2] == ["api", "memories"] and method == "PATCH": data = self.store.update_memory(int(parts[2]), body)
            elif len(parts) == 3 and parts[:2] == ["api", "memories"] and method == "DELETE": data = {"deleted": self.store.delete("memories", int(parts[2]))}
            elif path == "/api/sources" and method == "POST": data = self.store.create_source(body)
            elif len(parts) == 3 and parts[:2] == ["api", "sources"] and method == "DELETE": data = {"deleted": self.store.delete("sources", int(parts[2]))}
            elif path == "/api/signals" and method == "POST": data = self.store.create_signal(body)
            elif path == "/api/matches" and method == "POST": data = self.store.create_match()
            elif path == "/api/feedback" and method == "POST": data = self.store.create_feedback(body)
            else: return self.send_json({"error": "not found"}, 404)
            self.send_json(data, 201 if method == "POST" else 200)
        except (ValueError, json.JSONDecodeError) as exc:
            self.send_json({"error": str(exc)}, 400)
        except Exception as exc:
            self.send_json({"error": str(exc)}, 500)

    def static(self, url_path):
        relative = "index.html" if url_path in ("", "/") else url_path.lstrip("/")
        target = (DIST / relative).resolve()
        if DIST.resolve() not in target.parents and target != DIST.resolve():
            return self.send_json({"error": "not found"}, 404)
        if not target.is_file():
            return self.send_json({"error": "not found"}, 404)
        raw = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mimetypes.guess_type(target.name)[0] or "application/octet-stream")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers(); self.wfile.write(raw)


def main():
    parser = argparse.ArgumentParser(description="Research Mesh SQLite server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--db", default=str(DEFAULT_DB))
    args = parser.parse_args()
    Handler.store = Store(args.db)
    print(f"Research Mesh running at http://{args.host}:{args.port}")
    print(f"SQLite database: {args.db}")
    ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
