import json
from datetime import datetime, timedelta
from send import sc_send
from stock_top_list import get_top_list

def get_recent_data():
    # 获取今天的数据
    today = datetime.now()
    date_str = today.strftime('%Y%m%d')
    date_str = "20250317"
    count = get_top_list(date_str)
    
    # 读取历史数据
    try:
        with open('lhb.json', 'r') as f:
            all_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        all_data = {}
    
    # 如果今天有数据，更新到文件中
    if count is not None:
        all_data[date_str] = count
        with open('lhb.json', 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    # 获取最近5天的数据
    recent_data = []
    days_back = 0
    while len(recent_data) < 5:  # 直到找到5个有数据的交易日
        date = today - timedelta(days=days_back)
        date_str = date.strftime('%Y%m%d')
        if date_str in all_data:
            recent_data.append((date.strftime('%m.%d'), all_data[date_str]))
        days_back += 1
        if days_back > 30:  # 设置一个最大查找范围，避免无限循环
            break
    
    return recent_data

def send_report():
    recent_data = get_recent_data()
    if not recent_data:
        return
    
    # 构造消息内容
    title = f"龙虎榜数据统计 {datetime.now().strftime('%m.%d')}"
    desp = "最近5个交易日龙虎榜数量（主板+双创+上涨+去重）：\n"
    for date, count in reversed(recent_data):  # 使用reversed()倒序显示
        desp += f"{date}: {count}只\n"
    key = "SCT237911TGhewiKR8rjSIQaU32XnI2rhF"
    print(title)
    print(desp)
    # 发送消息
    # sc_send(key, title, desp)

if __name__ == '__main__':
    send_report()