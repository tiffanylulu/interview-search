"""
为 AI-Agent 工程师题目自动标注子分类
基于标题关键词匹配，覆盖 82 道题 → 10 个子分类
"""
import json, os, sys

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
QUESTIONS_FILE = os.path.join(DATA_DIR, 'questions.json')

# 子分类定义（优先级从高到低）
CATEGORIES = [
    ("Agent 基础与架构", [
        "Agent 的对话状态管理", "什么是 AI Agent", "Agentic Loop", "Agentic AI",
        "Agent 架构模式", "ReAct、Plan", "Agent 项目的典型目录结构",
        "Structured Output", "Agent 的流式输出", "Context Window",
        "从 0 到 1 设计", "Agent 错误恢复", "Agent 测试策略",
        "LLM 幻觉",
    ]),
    ("LangChain 与框架", [
        "LangChain", "LangGraph", "LlamaIndex", "LCEL", "OpenAI Assistants API",
        "OpenAI API", "ReAct 框架",
    ]),
    ("RAG 基础", [
        "RAG 的完整流程", "什么是 RAG 中的分块", "分块策略",
        "Embedding 嵌入", "Embedding Model", "Rerank",
        "RAG 的主要流程", "什么是 RAG",
    ]),
    ("RAG 进阶与优化", [
        "RAG 的优化", "RAG 调优", "混合检索", "查询扩展",
        "自查询", "提示压缩", "RAG 系统的评估方法",
        "GraphRAG", "Agentic RAG", "生产级 RAG",
        "大规模 RAG", "RAG 中的查询优化",
    ]),
    ("Function Calling 与 Tool Use", [
        "Function Calling", "Tool Use", "Tool Calling",
    ]),
    ("Multi-Agent 系统", [
        "Multi-Agent", "AutoGen", "CrewAI", "多 Agent", "多智能体",
        "A2A 协议",
    ]),
    ("MCP 协议与集成", [
        "MCP", "OpenClaw", "Google ADK",
    ]),
    ("Prompt 工程与安全", [
        "Prompt Engineering", "Prompt 注入", "Prompt 版本管理",
    ]),
    ("模型与推理优化", [
        "微调", "Fine-tuning", "LoRA", "推理加速", "量化",
        "LLM 主流模型横向对比", "Embedding 模型选型",
        "LLM 推理", "Token 消耗优化", "成本优化",
    ]),
    ("企业级 Agent 系统设计", [
        "企业级 Agent", "Agent 可观测性", "Agent 的记忆系统",
        "Agent 的评估体系", "Agent 的权限控制", "AI Gateway",
        "Agent 评估体系建设", "Agent 记忆系统", "冲突解决与记忆合并",
        "Agent 平台的系统设计", "AI 应用的成本优化",
        "Agent 可观测性体系设计",
    ]),
]


def classify(title):
    title_lower = title.lower()
    for cat, keywords in CATEGORIES:
        for kw in keywords:
            if kw.lower() in title_lower:
                return cat
    return "Agent 基础与架构"  # 默认


def main():
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated = 0
    stats = {}
    for q in data:
        if q['position'] == 'AI-Agent工程师':
            cat = classify(q['title'])
            q['sub_category'] = cat
            stats[cat] = stats.get(cat, 0) + 1
            updated += 1

    # 输出分类统计
    print(f"AI-Agent 题目总数: {updated}")
    print(f"\n{'子分类':<20} {'数量':>5}")
    print("-" * 27)
    for cat in [c[0] for c in CATEGORIES]:
        print(f"{cat:<20} {stats.get(cat, 0):>5}")
    print("-" * 27)
    print(f"{'合计':<20} {sum(stats.values()):>5}")

    # 保存
    with open(QUESTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n已更新 {QUESTIONS_FILE}")

    # 列出各分类题目
    print("\n" + "=" * 60)
    for cat in [c[0] for c in CATEGORIES]:
        items = [q for q in data if q.get('sub_category') == cat]
        if items:
            print(f"\n【{cat}】(共 {len(items)} 题)")
            for q in items:
                print(f"  - {q['title']}")


if __name__ == '__main__':
    main()
