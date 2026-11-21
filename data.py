"""6 candidates + 2 team contexts, deliberately hard-coded as plain dicts."""

CANDIDATES = [
    {
        "id": "c1",
        "name": "林晓",
        "learning_experience": [
            {"school": "华中科技大学", "degree": "本科", "major": "软件工程", "period": "2014-2018"},
            {"type": "自学", "topics": ["LLM 应用架构", "分布式事务", "可观测性"]},
        ],
        "work_experience": [
            {
                "company": "某支付科技公司", "role": "高级后端工程师", "period": "2020-至今",
                "responsibilities": ["Python 支付 API", "异步任务状态机", "生产故障治理"],
                "achievements": ["实现任务断点恢复与幂等重放", "上线链路归因，将失败率降低 35%"],
                "delivery_scope": "production_owner",
            },
            {
                "company": "某电商公司", "role": "后端工程师", "period": "2018-2020",
                "responsibilities": ["订单服务", "SQL 数据治理"],
                "achievements": ["参与双十一容量治理"], "delivery_scope": "production_contributor",
            },
        ],
        "skills": ["python", "api", "sql", "docker", "aws", "状态机", "可观测性"],
        "previous_compensation": {"currency": "CNY", "base_monthly_k": 38, "months": 15, "annual_total_k": 620},
        "expectations": {
            "target_roles": ["AI Agent 平台后端", "后端技术负责人"],
            "work_content": ["复杂工作流", "线上可靠性", "LLM 应用基础设施"],
            "annual_total_k_range": [700, 850], "cities": ["上海", "杭州"], "work_mode": "hybrid",
            "team_culture": ["工程决策透明", "重视线上质量"], "growth": "承担架构与小团队带领职责",
        },
    },
    {
        "id": "c2",
        "name": "周然",
        "learning_experience": [
            {"school": "同济大学", "degree": "本科", "major": "工业设计", "period": "2016-2020"},
        ],
        "work_experience": [
            {
                "company": "某 SaaS 公司", "role": "前端工程师", "period": "2020-至今",
                "responsibilities": ["React 中后台", "设计系统"],
                "achievements": ["主导前端重构，首屏时间降低 40%"], "delivery_scope": "production_owner",
            }
        ],
        "skills": ["javascript", "typescript", "react", "css", "figma"],
        "previous_compensation": {"currency": "CNY", "base_monthly_k": 30, "months": 14, "annual_total_k": 450},
        "expectations": {
            "target_roles": ["高级前端工程师", "全栈工程师"], "work_content": ["复杂交互", "设计工程"],
            "annual_total_k_range": [520, 650], "cities": ["上海"], "work_mode": "onsite_or_hybrid",
            "team_culture": ["产品与研发协作紧密"], "growth": "逐步转向全栈",
        },
    },
    {
        "id": "c3",
        "name": "陈雨",
        "learning_experience": [
            {"school": "北京师范大学", "degree": "硕士", "major": "应用统计", "period": "2017-2020"},
            {"type": "课程", "topics": ["因果推断", "实验设计", "机器学习评测"]},
        ],
        "work_experience": [
            {
                "company": "某内容平台", "role": "增长数据科学家", "period": "2020-至今",
                "responsibilities": ["A/B 实验", "推荐 badcase 分析", "跨团队增长诊断"],
                "achievements": ["建立 800 条 golden set 与失败分类体系", "把 badcase 转成产品 backlog 并完成线上因果归因"],
                "delivery_scope": "production_owner",
            }
        ],
        "skills": ["sql", "python", "statistics", "experimentation", "causal inference", "评测集"],
        "previous_compensation": {"currency": "CNY", "base_monthly_k": 35, "months": 16, "annual_total_k": 600},
        "expectations": {
            "target_roles": ["AI 评测", "增长数据科学"], "work_content": ["评测体系", "因果实验", "参与产品决策"],
            "annual_total_k_range": [650, 800], "cities": ["北京", "上海"], "work_mode": "hybrid",
            "team_culture": ["用实验而非职级做决策", "允许挑战需求"], "growth": "成为 AI 产品评测负责人",
        },
    },
    {
        "id": "c4",
        "name": "赵可",
        "learning_experience": [
            {"school": "电子科技大学", "degree": "本科", "major": "计算机科学", "period": "2021-2025"},
            {"type": "开源/比赛", "topics": ["Agent demo", "RAG", "Prompt Engineering"]},
        ],
        "work_experience": [
            {
                "company": "某 AI 创业公司", "role": "后端实习生", "period": "2024-2025",
                "responsibilities": ["Python API", "Agent demo"], "achievements": ["两周完成客服 Agent 演示"],
                "delivery_scope": "demo_only",
            }
        ],
        "skills": ["python", "api", "sql", "docker", "langchain", "agent"],
        "previous_compensation": {"currency": "CNY", "base_monthly_k": 8, "months": 12, "annual_total_k": 96},
        "expectations": {
            "target_roles": ["AI Agent 后端工程师"], "work_content": ["从 demo 到生产", "快速学习"],
            "annual_total_k_range": [300, 400], "cities": ["深圳", "上海", "杭州"], "work_mode": "flexible",
            "team_culture": ["有导师", "允许试错"], "growth": "补齐生产工程能力",
        },
    },
    {
        "id": "c5",
        "name": "王敏",
        "learning_experience": [
            {"school": "西安交通大学", "degree": "本科", "major": "自动化", "period": "2010-2014"},
            {"type": "认证", "topics": ["AWS Solutions Architect", "Kubernetes CKA"]},
        ],
        "work_experience": [
            {
                "company": "某云服务公司", "role": "平台工程负责人", "period": "2018-至今",
                "responsibilities": ["分布式工作流", "Kubernetes", "SRE"],
                "achievements": ["实现工作流 checkpoint 与故障恢复", "建立线上 SLO、告警和根因归因机制"],
                "delivery_scope": "production_owner",
            },
            {
                "company": "某银行科技部", "role": "后端工程师", "period": "2014-2018",
                "responsibilities": ["Java/Python 服务", "数据库"],
                "achievements": ["核心批处理平台连续三年零重大事故"], "delivery_scope": "production_owner",
            },
        ],
        "skills": ["python", "api", "aws", "kubernetes", "distributed systems", "checkpoint", "sre"],
        "previous_compensation": {"currency": "CNY", "base_monthly_k": 48, "months": 15, "annual_total_k": 800},
        "expectations": {
            "target_roles": ["平台工程负责人", "AI 基础设施负责人"],
            "work_content": ["可靠性", "分布式工作流", "团队建设"],
            "annual_total_k_range": [900, 1100], "cities": ["上海"], "work_mode": "hybrid",
            "team_culture": ["长期主义", "工程质量优先"], "growth": "进入 AI 基础设施并继续管理团队",
        },
    },
    {
        "id": "c6",
        "name": "孙哲",
        "learning_experience": [
            {"school": "某财经大学", "degree": "本科", "major": "信息管理", "period": "2013-2017"},
            {"type": "在线课程", "topics": ["Python", "微服务", "Kubernetes", "LLM Agent"]},
        ],
        "work_experience": [
            {
                "company": "某咨询公司", "role": "解决方案顾问", "period": "2017-至今",
                "responsibilities": ["售前方案", "客户演示", "PoC"],
                "achievements": ["完成多个 Agent、推荐与高并发架构 demo"], "delivery_scope": "demo_only",
            }
        ],
        "skills": ["python", "api", "sql", "docker", "kubernetes", "aws", "agent", "recommendation"],
        "previous_compensation": {"currency": "CNY", "base_monthly_k": 32, "months": 14, "annual_total_k": 480},
        "expectations": {
            "target_roles": ["AI 技术负责人", "AI Agent 平台后端"], "work_content": ["Agent 产品", "技术管理"],
            "annual_total_k_range": [800, 1000], "cities": ["北京", "上海", "远程"], "work_mode": "remote_preferred",
            "team_culture": ["快速迭代", "业务导向"], "growth": "直接负责 AI 产品技术方向",
        },
    },
]


TEAM_CONTEXTS = [
    {
        "id": "agent_platform_backend",
        "role": "AI Agent 平台后端",
        "jd_requirements": [
            "3 年以上 Python 或 Go 后端经验",
            "熟悉高并发服务、SQL、容器与云平台",
            "有 LLM、Agent 或分布式系统经验优先",
        ],
        "team_undocumented": [
            "JD 写了高并发服务，实际 70% 时间在改 agent 状态机的断点恢复",
            "团队半年内砍过两次推荐方向，现在真正卡的是评测集缺失",
            "负责人明确不接受只做 demo 不做线上归因的人",
        ],
    },
    {
        "id": "ai_evaluation_growth",
        "role": "AI 产品评测与增长",
        "jd_requirements": [
            "2 年以上数据分析或数据科学经验",
            "熟练使用 SQL、Python 与统计方法",
            "有 A/B 实验、推荐或增长分析经验优先",
        ],
        "team_undocumented": [
            "JD 写增长分析，实际首要任务是从零补 agent 评测集和 badcase 失败分类",
            "模型升级不是当前瓶颈，团队缺能把 badcase 转成产品 backlog 并推动落地的人",
            "负责人不接受只报相关性，关键结论必须有因果实验或线上归因",
        ],
    },
]


OFFLINE_CASES = [
    {"candidate_id": "c1", "team_id": "agent_platform_backend", "expected": "go", "note": "有状态机恢复和线上归因证据"},
    {"candidate_id": "c1", "team_id": "ai_evaluation_growth", "expected": "no-go", "note": "缺评测集与 badcase 产品闭环"},
    {"candidate_id": "c2", "team_id": "agent_platform_backend", "expected": "no-go", "note": "背景与实际后端工作不匹配"},
    {"candidate_id": "c2", "team_id": "ai_evaluation_growth", "expected": "no-go", "note": "缺评测、实验和归因经验"},
    {"candidate_id": "c3", "team_id": "agent_platform_backend", "expected": "no-go", "note": "评测强但缺状态机与后端交付"},
    {"candidate_id": "c3", "team_id": "ai_evaluation_growth", "expected": "go", "note": "覆盖评测集、产品闭环与因果归因"},
    {"candidate_id": "c4", "team_id": "agent_platform_backend", "expected": "no-go", "note": "仅有 demo，正中团队红线"},
    {"candidate_id": "c4", "team_id": "ai_evaluation_growth", "expected": "no-go", "note": "无评测与实验交付"},
    {"candidate_id": "c5", "team_id": "agent_platform_backend", "expected": "go", "note": "状态恢复与生产归因能力强"},
    {"candidate_id": "c5", "team_id": "ai_evaluation_growth", "expected": "no-go", "note": "缺评测数据与产品闭环"},
    {"candidate_id": "c6", "team_id": "agent_platform_backend", "expected": "no-go", "note": "JD 关键词很多但仅做 demo"},
    {"candidate_id": "c6", "team_id": "ai_evaluation_growth", "expected": "no-go", "note": "无实际评测和因果归因交付"},
]


TRUST_CRITERIA = {
    "min_cases": 10,
    "min_accuracy": 0.80,
    "min_positive_recall": 0.80,
    "max_private_constraint_false_positives": 0,
    "min_attribution_rate": 1.00,
    "must_beat_or_equal_baseline": True,
}
