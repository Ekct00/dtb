import akshare as ak
import json
from datetime import datetime, timedelta

def get_top_list(date_str):
    result = None
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
        # 打印结果
        print(df)
        count = len(df)
        
        result = count
    except Exception as e:
        print(f'获取{date_str}数据失败: {str(e)}')
    return result

def main():
    # 设置起始日期和结束日期
    start_date = datetime(2024, 9, 20)
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
            formatted_date = current_date.strftime('%-m.%-d')
            result_dict[formatted_date] = count
        current_date += timedelta(days=1)
    
    # 输出结果
    print(json.dumps(result_dict, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()