import tempfile
import unittest
from pathlib import Path

from server import Store


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmp.name) / "test.db"
        self.store = Store(self.db_path)

    def tearDown(self):
        self.tmp.cleanup()

    def test_seed_and_profile_update(self):
        self.assertEqual(self.store.profile()["name"], "Maya")
        updated = self.store.update_profile({"name": "Emma"})
        self.assertEqual(updated["name"], "Emma")

    def test_memory_crud_and_persistence(self):
        created = self.store.create_memory({"kind": "need", "content": "寻找图学习合作者"})
        self.assertTrue(created["is_active"])
        updated = self.store.update_memory(created["id"], {"is_active": False})
        self.assertFalse(updated["is_active"])
        reopened = Store(self.db_path)
        self.assertTrue(any(m["content"] == "寻找图学习合作者" for m in reopened.list_memories()))
        self.assertTrue(self.store.delete("memories", created["id"]))

    def test_signal_match_and_feedback(self):
        signal = self.store.create_signal({"type": "demand", "content": "寻找评测数据"})
        self.assertEqual(signal["type"], "demand")
        match = self.store.create_match()
        self.assertEqual(match["score"], 94)
        feedback = self.store.create_feedback({"match_id": match["id"], "rating": 5, "useful": True})
        self.assertTrue(feedback["useful"])
        self.assertEqual(self.store.stats()["matches"], 1)

    def test_source_crud(self):
        source = self.store.create_source({"kind": "folder", "name": "NeurIPS 研究", "scope": "selected"})
        self.assertEqual(source["status"], "connected")
        self.assertTrue(self.store.delete("sources", source["id"]))


if __name__ == "__main__":
    unittest.main()
