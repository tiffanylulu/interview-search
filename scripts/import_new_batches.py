"""
导入所有新题目批次到 SQLite
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from manage_db import add_questions

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

batch_files = [
    'new_batch1_ai_agent.json',
    'new_batch2_ai_agent.json',
    'new_batch3_backend.json',
    'new_batch4_ai_frontend.json',
    'new_batch5_product_data.json',
    'new_batch6_test_devops.json',
]

total = 0
all_questions = []

for fname in batch_files:
    path = os.path.join(DATA_DIR, fname)
    if not os.path.exists(path):
        print(f" 跳过: {fname}")
        continue
    with open(path, 'r', encoding='utf-8') as f:
        batch = json.load(f)
    all_questions.extend(batch)
    print(f"  {fname}: {len(batch)} 道")

print(f"\n总计新增: {len(all_questions)} 道")

# 导入
add_questions(all_questions)

# 统计
from manage_db import get_conn
conn = get_conn()
total = conn.execute('SELECT COUNT(*) FROM questions').fetchone()[0]
print(f"\n数据库总题目数: {total}")

# 各岗位数量
rows = conn.execute('''
    SELECT position, COUNT(*) as cnt FROM questions 
    GROUP BY position ORDER BY cnt DESC
''').fetchall()
print("\n更新后各岗位数量:")
for r in rows:
    print(f"  {r['position']}: {r['cnt']} 道")
conn.close()
