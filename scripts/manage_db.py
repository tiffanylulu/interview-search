"""
面试题库 SQLite 管理脚本
功能：建库建表 / JSON导入 / JSON导出 / 统计查询
"""
import sqlite3, json, os, sys, argparse

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'questions.db')
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

def get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """创建面试题库表结构"""
    conn = get_conn()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            position    TEXT    NOT NULL,
            difficulty  TEXT    NOT NULL,
            source      TEXT    NOT NULL,
            publish_date TEXT   NOT NULL,
            title       TEXT    NOT NULL,
            description TEXT    NOT NULL,
            answer      TEXT    NOT NULL,
            tags        TEXT    NOT NULL,
            sub_category TEXT   DEFAULT "",
            created_at  TEXT    DEFAULT (datetime('now','localtime')),
            updated_at  TEXT    DEFAULT (datetime('now','localtime'))
        )
    ''')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_position ON questions(position)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_difficulty ON questions(difficulty)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_source ON questions(source)')
    conn.commit()
    conn.close()
    print("数据库初始化完成:", DB_PATH)

def import_from_json(json_path=None):
    """从 JSON 导入题目到 SQLite"""
    if not json_path:
        json_path = os.path.join(DATA_DIR, 'questions.json')
    
    if not os.path.exists(json_path):
        print(f"文件不存在: {json_path}")
        sys.exit(1)
    
    with open(json_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    conn = get_conn()
    
    # 清空旧数据
    conn.execute('DELETE FROM questions')
    
    for q in questions:
        conn.execute('''
            INSERT INTO questions (id, position, difficulty, source, publish_date, title, description, answer, tags, sub_category)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            q['id'],
            q['position'],
            q['difficulty'],
            q['source'],
            q['publishDate'],
            q['title'],
            q['description'],
            q['answer'],
            json.dumps(q['tags'], ensure_ascii=False),
            q.get('sub_category', '')
        ))
    
    conn.commit()
    count = conn.execute('SELECT COUNT(*) FROM questions').fetchone()[0]
    conn.close()
    print(f"导入完成，共 {count} 道题目")

def export_to_json(output_path=None):
    """从 SQLite 导出为 JSON（供前端加载）"""
    if not output_path:
        output_path = os.path.join(DATA_DIR, 'questions.json')
    
    conn = get_conn()
    rows = conn.execute('SELECT * FROM questions ORDER BY id').fetchall()
    
    data = []
    for r in rows:
        data.append({
            'id': r['id'],
            'position': r['position'],
            'difficulty': r['difficulty'],
            'source': r['source'],
            'publishDate': r['publish_date'],
            'title': r['title'],
            'description': r['description'],
            'answer': r['answer'],
            'tags': json.loads(r['tags']),
            'sub_category': r['sub_category'] if 'sub_category' in r.keys() else ''
        })
    
    conn.close()
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"导出完成: {output_path} ({len(data)} 道题目)")

def show_stats():
    """显示题库统计"""
    conn = get_conn()
    
    print("\n====== 题库统计 ======")
    
    total = conn.execute('SELECT COUNT(*) FROM questions').fetchone()[0]
    print(f"总题目数: {total}")
    
    print("\n岗位分布:")
    rows = conn.execute('''
        SELECT position, COUNT(*) as cnt FROM questions 
        GROUP BY position ORDER BY cnt DESC
    ''').fetchall()
    for r in rows:
        print(f"  {r['position']}: {r['cnt']} 道")
    
    print("\n难度分布:")
    rows = conn.execute('''
        SELECT difficulty, COUNT(*) as cnt FROM questions 
        GROUP BY difficulty ORDER BY 
        CASE difficulty WHEN '初级' THEN 1 WHEN '中级' THEN 2 WHEN '高级' THEN 3 WHEN '专家级' THEN 4 END
    ''').fetchall()
    for r in rows:
        print(f"  {r['difficulty']}: {r['cnt']} 道")
    
    print("\n后端开发子分类:")
    rows = conn.execute('''
        SELECT sub_category, COUNT(*) as cnt FROM questions 
        WHERE position = '后端开发' AND sub_category != ''
        GROUP BY sub_category ORDER BY cnt DESC
    ''').fetchall()
    for r in rows:
        print(f"  {r['sub_category']}: {r['cnt']} 道")
    
    conn.close()

def add_questions(questions_list):
    """批量添加题目（试题为 dict 列表）"""
    conn = get_conn()
    
    for q in questions_list:
        max_id = conn.execute('SELECT COALESCE(MAX(id), 0) FROM questions').fetchone()[0]
        new_id = max_id + 1
        
        conn.execute('''
            INSERT INTO questions (id, position, difficulty, source, publish_date, title, description, answer, tags, sub_category)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            new_id,
            q['position'],
            q['difficulty'],
            q['source'],
            q['publishDate'],
            q['title'],
            q['description'],
            q['answer'],
            json.dumps(q['tags'], ensure_ascii=False),
            q.get('sub_category', '')
        ))
    
    conn.commit()
    new_count = conn.execute('SELECT COUNT(*) FROM questions').fetchone()[0]
    conn.close()
    print(f"新增 {len(questions_list)} 道题目，当前共 {new_count} 道")

def main():
    parser = argparse.ArgumentParser(description='面试题库 SQLite 管理工具')
    parser.add_argument('action', choices=['init', 'import', 'export', 'stats'],
                       help='操作: init(建库)/import(导入JSON)/export(导出JSON)/stats(统计)')
    parser.add_argument('--json', help='JSON 文件路径（可选）')
    
    args = parser.parse_args()
    
    if args.action == 'init':
        init_db()
    elif args.action == 'import':
        import_from_json(args.json)
    elif args.action == 'export':
        export_to_json(args.json)
    elif args.action == 'stats':
        show_stats()

if __name__ == '__main__':
    main()
