"""
从 index.html 提取 RAW_QUESTIONS 数组，转换为 JSON
"""
import re, json, sys

def extract_objects(text):
    """从 JS 数组文本中逐个提取对象"""
    objects = []
    depth = 0
    obj_start = -1
    
    lines = text.split('\n')
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('//'): continue
        if stripped == '': continue
        
        # Count braces
        for ch in stripped:
            if ch == '{': 
                if depth == 0:
                    obj_start = i
                depth += 1
            elif ch == '}': 
                depth -= 1
                if depth == 0 and obj_start >= 0:
                    # Extract object
                    obj_text = '\n'.join(lines[obj_start:i+1])
                    objects.append(obj_text)
                    obj_start = -1
                elif depth < 0:
                    depth = 0
    
    return objects

def parse_object(text):
    """解析单个 JS 对象为 dict"""
    obj = {}
    
    def get_str(pattern, text, default=''):
        m = re.search(pattern, text)
        return m.group(1) if m else default
    
    def get_int(pattern, text, default=0):
        m = re.search(pattern, text)
        return int(m.group(1)) if m else default
    
    def get_array(pattern, text):
        m = re.search(pattern, text, re.DOTALL)
        if not m: return []
        inner = m.group(1)
        return re.findall(r"'([^']*)'", inner)
    
    def get_answer(text):
        """提取 backtick 模板字符串"""
        m = re.search(r'answer:\s*`', text)
        if not m: return ''
        start = m.end()
        # 找到匹配的结束反引号（反引号内的 \` 不计算）
        i = start
        while i < len(text):
            if text[i] == '\\' and i+1 < len(text):
                i += 2
                continue
            if text[i] == '`':
                answer = text[start:i]
                answer = answer.replace('\\n', '\n').replace('\\t', '\t').replace('\\`', '`')
                # 去掉后面的 ,
                answer = answer.strip()
                return answer
            i += 1
        return ''
    
    obj['id'] = get_int(r'id:\s*(\d+)', text)
    obj['position'] = get_str(r"position:\s*'([^']*)'", text)
    obj['difficulty'] = get_str(r"difficulty:\s*'([^']*)'", text)
    obj['source'] = get_str(r"source:\s*'([^']*)'", text)
    obj['publishDate'] = get_str(r"publishDate:\s*'([^']*)'", text)
    obj['title'] = get_str(r"title:\s*'([^']*)'", text)
    obj['description'] = get_str(r"description:\s*'([^']*)'", text)
    obj['answer'] = get_answer(text)
    obj['tags'] = get_array(r'tags:\s*\[(.*?)\]', text)
    
    return obj

def main():
    raw_path = 'F:/WorkBuddySpace/interview-search/_raw_data.txt'
    with open(raw_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    objects = extract_objects(text)
    print(f"找到 {len(objects)} 个对象")
    
    questions = [parse_object(obj) for obj in objects]
    questions = [q for q in questions if q.get('id')]
    
    if questions:
        output_path = 'F:/WorkBuddySpace/interview-search/data/questions.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(questions, f, ensure_ascii=False, indent=2)
        
        print(f"成功提取 {len(questions)} 道题目")
        print(f"已保存到 {output_path}")
        
        from collections import Counter
        pos_counts = Counter(q['position'] for q in questions)
        print("\n岗位分布:")
        for pos, cnt in pos_counts.most_common():
            print(f"  {pos}: {cnt} 道")
    else:
        print("未能提取到题目！")
        sys.exit(1)

if __name__ == '__main__':
    main()
