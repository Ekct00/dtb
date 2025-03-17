import akshare as ak
import json
from datetime import datetime, timedelta

# 全局变量，用于存储lhb.json的数据
existing_data = {}

# 初始化时读取lhb.json文件
try:
    with open('lhb.json', 'r') as f:
        existing_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    pass

def get_top_list(date_str):
    result = None
    # 检查内存中是否已有该日期的数据
    if date_str in existing_data:
        print(f'{date_str}数据已存在，直接返回缓存数据')
        return existing_data[date_str]

    try:
        # 获取指定日期的龙虎榜数据
        df = ak.stock_lhb_detail_em(start_date=date_str, end_date=date_str)
        # 只保留需要的字段
        df = df[['代码', '名称', '上榜日', '涨跌幅']]
        # 去除名称重复的记录
        df = df.drop_duplicates(subset=['名称'], keep='first')
        # 筛选涨跌幅大于0的记录
        df = df[df['涨跌幅'] > 0]
        # 筛选主板、创业板和科创板的股票
        df['代码'] = df['代码'].astype(str)
        valid_prefixes = ['60', '00', '30', '68']
        df = df[df['代码'].str[:2].isin(valid_prefixes)]
        count = len(df)
        print(f'{date_str}龙虎榜数量：{count}')
        result = count
    except Exception as e:
        print(f'获取{date_str}数据失败: {str(e)}')
    return result

def main():
    # 设置起始日期和结束日期
    start_date = datetime(2019, 12, 1)
    end_date = datetime.now()
    
    # 用于存储结果的字典
    result_dict = {}
    
    # 遍历日期范围
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y%m%d')
        count = get_top_list(date_str)
        if count is not None:
            # 将日期格式化为 "M.D" 格式
            formatted_date = date_str
            result_dict[formatted_date] = count
        current_date += timedelta(days=1)
    
    # 保存结果到文件
    with open('lhb.json', 'w', encoding='utf-8') as f:
        json.dump(result_dict, f, ensure_ascii=False, indent=2)
    
    print('数据已保存到lhb.json文件')

if __name__ == '__main__':
    main()