import os
from datetime import datetime
from plot_kline import plot_kline
from wecom import wecom_send, wecom_send_image

def plot_and_send():
    # 检查今天是否有数据
    import json
    today = datetime.now()
    today_str = today.strftime('%Y%m%d')
    try:
        with open('lhb.json', 'r') as f:
            lhb_data = json.load(f)
        if today_str not in lhb_data:
            print(f"今天 {today_str} 没有数据，不发送图表")
            return
    except (FileNotFoundError, json.JSONDecodeError):
        print("无法读取数据文件")
        return
    
    # 设置时间范围
    start_date = "20240901"
    end_date = today
    
    # 生成图表
    image_path = plot_kline(start_date, end_date)
    
    # 构造消息内容
    title = f"龙虎榜数据统计图表 ({start_date} - {end_date})"
    
    # 发送到企业微信
    wecom_key = "f4efcc56-ab15-45b8-97a7-aabd2125efcd"
    with open(image_path, 'rb') as f:
        image_data = f.read()
    wecom_send_image(wecom_key, image_data)
    
    # 删除临时图片文件
    os.remove(image_path)

if __name__ == '__main__':
    plot_and_send()