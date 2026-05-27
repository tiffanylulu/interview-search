"""
爬取 面试鸭 (mianshiya.com) 面试题库
目标:
  - Bank 1906189461556076546: AI大模型面试题库 (303题, 16页)
  - Bank 1860871861809897474: Java热门面试题200道 (200题, 10页)
输出: data/scraped_ai_llm.json, data/scraped_java.json
"""
import requests
import re
import json
import time
import os

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

DIFFICULTY_MAP = {
    '简单': '初级',
    '中等': '中级',
    '困难': '高级',
}

BANKS = [
    {
        'id': '1906189461556076546',
        'name': 'AI大模型面试题库',
        'total_pages': 16,
        'position': 'AI-Agent工程师',
        'output': 'scraped_ai_llm.json',
    },
    {
        'id': '1860871861809897474',
        'name': 'Java热门面试题200道',
        'total_pages': 10,
        'position': '后端开发',
        'output': 'scraped_java.json',
    },
]


def fetch_page(bank_id, page):
    """获取单页题目数据"""
    url = f'https://www.mianshiya.com/bank/{bank_id}?current={page}&pageSize=20'
    print(f'  正在请求: {url}')
    
    for attempt in range(3):
        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
            r.encoding = 'utf-8'
            if r.status_code == 200:
                return r.text
            else:
                print(f'    状态码 {r.status_code}, 重试 {attempt+1}/3')
        except Exception as e:
            print(f'    请求失败: {e}, 重试 {attempt+1}/3')
            time.sleep(2)
    
    print(f'    3次重试均失败，跳过此页')
    return None


def parse_questions(html, bank_id):
    """从 HTML 中提取题目列表"""
    questions = []
    
    # 匹配每一行: <tr data-row-key="ID"> ... </tr>
    row_pattern = re.compile(
        r'<tr[^>]*data-row-key="(\d+)"[^>]*>(.*?)</tr>',
        re.DOTALL
    )
    
    for match in row_pattern.finditer(html):
        question_id = match.group(1)
        row_html = match.group(2)
        
        # 提取标题
        title_match = re.search(
            rf'<a[^>]*href="/bank/{bank_id}/question/{question_id}[^"]*"[^>]*>\s*(.*?)\s*</a>',
            row_html, re.DOTALL
        )
        if not title_match:
            continue
        
        title = title_match.group(1).strip()
        # 清理 HTML 实体
        title = title.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
        
        # 提取难度
        diff_match = re.search(r'<span[^>]*>\s*(简单|中等|困难)\s*</span>', row_html)
        difficulty = diff_match.group(1) if diff_match else '中等'
        
        # 提取标签
        tags = []
        tag_matches = re.findall(r'<span class="ant-tag[^"]*"[^>]*>\s*(.*?)\s*</span>', row_html)
        for tag_text in tag_matches:
            tag_text = tag_text.strip()
            tag_text = tag_text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
            if tag_text and tag_text not in ('简单', '中等', '困难'):
                tags.append(tag_text)
        
        # 检测 VIP
        is_vip = 'VIP' in row_html or 'vip' in row_html.lower()
        
        questions.append({
            'question_id': question_id,
            'title': title,
            'difficulty_raw': difficulty,
            'tags': tags,
            'is_vip': is_vip,
        })
    
    return questions


def scrape_bank(bank):
    """爬取单个题库全部页面"""
    bank_id = bank['id']
    total_pages = bank['total_pages']
    all_questions = []
    
    print(f'\n{"="*60}')
    print(f'开始爬取: {bank["name"]} (Bank ID: {bank_id})')
    print(f'预计 {total_pages} 页')
    print(f'{"="*60}')
    
    for page in range(1, total_pages + 1):
        html = fetch_page(bank_id, page)
        if html is None:
            continue
        
        questions = parse_questions(html, bank_id)
        print(f'  第{page}页: 提取到 {len(questions)} 题')
        
        for q in questions:
            q['page'] = page
            all_questions.append(q)
        
        # 页间延迟，避免反爬
        if page < total_pages:
            time.sleep(1.5)
    
    return all_questions


def convert_to_ihub_format(questions, bank):
    """转换为 InterviewHub JSON 格式"""
    result = []
    for q in questions:
        item = {
            'position': bank['position'],
            'difficulty': DIFFICULTY_MAP.get(q['difficulty_raw'], '中级'),
            'source': '面试鸭',
            'publishDate': '2026-05-27',
            'title': q['title'],
            'description': f'本题来自面试鸭「{bank["name"]}」',
            'answer': '（VIP专属题目，详细答案需面试鸭会员查看）' if q['is_vip'] else '（答案待补充）',
            'tags': q['tags'],
            'sub_category': '',
            '_source_id': q['question_id'],
            '_source_bank': bank['id'],
            '_is_vip': q['is_vip'],
        }
        result.append(item)
    return result


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    
    total_scraped = 0
    
    for bank in BANKS:
        questions = scrape_bank(bank)
        print(f'\n{bank["name"]}: 共爬取 {len(questions)} 题')
        total_scraped += len(questions)
        
        # 转换为 InterviewHub 格式
        ihub_data = convert_to_ihub_format(questions, bank)
        
        # 保存原始爬取数据
        raw_path = os.path.join(DATA_DIR, bank['output'].replace('.json', '_raw.json'))
        with open(raw_path, 'w', encoding='utf-8') as f:
            json.dump(questions, f, ensure_ascii=False, indent=2)
        print(f'  原始数据已保存: {raw_path}')
        
        # 保存 InterviewHub 格式数据
        ihub_path = os.path.join(DATA_DIR, bank['output'])
        with open(ihub_path, 'w', encoding='utf-8') as f:
            json.dump(ihub_data, f, ensure_ascii=False, indent=2)
        print(f'  InterviewHub格式已保存: {ihub_path}')
        
        # 统计
        diffs = {}
        for q in questions:
            d = q['difficulty_raw']
            diffs[d] = diffs.get(d, 0) + 1
        vip_count = sum(1 for q in questions if q['is_vip'])
        print(f'  难度分布: {diffs}')
        print(f'  VIP题目: {vip_count}/{len(questions)}')
    
    print(f'\n{"="*60}')
    print(f'爬取完成! 共计 {total_scraped} 题')
    print(f'{"="*60}')


if __name__ == '__main__':
    main()
