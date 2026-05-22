"""
为后端开发题目添加 sub_category 字段
根据标签 + 标题关键词自动分类
"""
import json
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'questions.db')

# 分类规则：按标签匹配优先级定义
SUBCATEGORY_RULES = [
    ('Java基础', ['Java基础', 'String', '反射', '异常处理', '重载', '重写', '排序', '深拷贝', '浅拷贝']),
    ('Java容器', ['容器', 'ArrayList', 'LinkedList', 'HashMap', 'HashTable', 'ConcurrentHashMap', 'HashSet', 'Vector', 'Map']),
    ('JVM', ['JVM', 'GC', '类加载', '内存溢出', '内存泄漏', '堆', '栈']),
    ('多线程', ['多线程', 'ThreadLocal', 'volatile', 'synchronized', 'Lock', '线程池', 'Runnable', 'Callable']),
    ('MySQL', ['MySQL', '索引优化', 'EXPLAIN', '事务', 'InnoDB', '主从', '日志', 'B+Tree', '最左前缀', '覆盖索引', '分库分表', 'SQL优化']),
    ('Spring全家桶', ['Spring', 'SpringMVC', 'MyBatis', 'SpringBoot', '@Transactional', 'AOP', 'IOC', '@Autowired', '拦截器', '过滤器', 'Bean', 'OAuth', 'RBAC']),
    ('微服务', ['微服务', 'Nacos', 'Eureka', 'Gateway', 'Zuul', 'Feign', 'Sentinel', '服务熔断', '服务降级', '熔断降级', '服务发现', '负载均衡', 'Kubernetes', 'Docker']),
    ('Redis', ['Redis', '缓存', 'ZSet', 'RDB', 'AOF']),
    ('分布式', ['分布式', '分布式锁', '分布式事务', 'CAP', 'BASE', '最终一致性', '一致性', 'TCC', 'Saga', '消息队列', 'MQ', 'Kafka', 'RocketMQ', 'RabbitMQ', '全链路追踪', 'API网关']),
    ('其他', ['REST', 'API设计', 'gRPC', 'GraphQL', 'Protobuf', 'JWT', 'Dubbo', 'ES', 'Elasticsearch', 'Linux', 'SSO', 'RBAC', '定时任务', '日志系统', 'RPC']),
]


def classify_question(q):
    """根据一道题的 tags + title 进行最优先匹配分类"""
    tags = [t.strip() for t in q.get('tags', [])]
    title = q.get('title', '')
    combined = ' '.join(tags + [title])

    best_match = None
    best_score = 0

    for cat, keywords in SUBCATEGORY_RULES:
        score = 0
        for kw in keywords:
            if kw in combined:
                # 标签直接命中权重更高
                if kw in tags:
                    score += 3
                elif kw in title:
                    score += 2
                else:
                    score += 1
        if score > best_score:
            best_score = score
            best_match = cat

    return best_match if best_match else '其他'


def main():
    # 1. 读取 JSON
    json_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'questions.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 2. 分类
    print(f'总题数: {len(data)}')
    backend_count = 0
    cat_counts = {}
    for q in data:
        if q['position'] == '后端开发':
            cat = classify_question(q)
            q['sub_category'] = cat
            cat_counts[cat] = cat_counts.get(cat, 0) + 1
            backend_count += 1
        else:
            q['sub_category'] = ''  # 非后端题留空

    print(f'后端开发: {backend_count} 道')
    print(f'\n子分类分布:')
    for cat, cnt in sorted(cat_counts.items(), key=lambda x: -x[1]):
        print(f'  {cat}: {cnt} 道')

    # 3. 保存 JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'\n已更新 {json_path}')

    # 4. 更新 SQLite
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # 添加列（如果不存在）
    try:
        conn.execute('ALTER TABLE questions ADD COLUMN sub_category TEXT DEFAULT ""')
    except sqlite3.OperationalError:
        pass  # 列已存在

    for q in data:
        conn.execute('UPDATE questions SET sub_category = ? WHERE id = ?',
                     [q.get('sub_category', ''), q['id']])
    conn.commit()
    conn.close()
    print('已更新 SQLite 数据库')


if __name__ == '__main__':
    main()
