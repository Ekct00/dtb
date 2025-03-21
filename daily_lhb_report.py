import json
from datetime import datetime, timedelta
from send import sc_send
from stock_top_list import get_top_list
from wecom import wecom_send

def get_recent_data():
    # 获取今天的数据
    today = datetime.now()
    date_str = today.strftime('%Y%m%d')
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
    
    # 检查是否有今天的数据
    today = datetime.now().strftime('%m.%d')
    if recent_data[0][0] != today:  # recent_data是倒序的，第一个应该是今天
        print(f"今天 {today} 没有数据，不发送消息")
        return
    
    # 构造消息内容
    title = f"最近5个交易日龙虎榜数量（主板+双创+上涨+去重）："
    desp = ""
    for i, (date, count) in enumerate(reversed(recent_data)):
        desp += f"{date}: {count}只" + ("\n" if i < len(recent_data)-1 else "")
    
    # Server酱推送
    sc_key = "SCT237911TGhewiKR8rjSIQaU32XnI2rhF"
    sc_send(sc_key, title, desp)
    
    # 企业微信推送
    wecom_key = "f4efcc56-ab15-45b8-97a7-aabd2125efcd"
    wecom_send(wecom_key, title, desp)
    
    print(title)
    print(desp)

if __name__ == '__main__':
    send_report()