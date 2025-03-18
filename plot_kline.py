def plot_kline(start_date=None, end_date=None):
    import json
    import akshare as ak
    import pandas as pd
    import mplfinance as mpf
    import matplotlib.pyplot as plt
    from datetime import datetime

    # 设置中文字体 - 使用Linux和macOS通用字体
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Noto Sans CJK JP', 'Noto Sans CJK SC', 'WenQuanYi Micro Hei', 'SimHei', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    # 读取龙虎榜数据
    with open('lhb.json', 'r') as f:
        lhb_data = json.load(f)

    # 转换日期格式并创建DataFrame
    lhb_dates = []
    lhb_counts = []
    for date_str, count in lhb_data.items():
        lhb_dates.append(date_str)
        lhb_counts.append(count)

    lhb_df = pd.DataFrame({'date': lhb_dates, 'count': lhb_counts})
    lhb_df['date'] = pd.to_datetime(lhb_df['date'])
    lhb_df.set_index('date', inplace=True)

    # 使用传入的日期范围或默认使用全部数据范围
    if start_date is None:
        start_date = min(lhb_df.index).strftime('%Y%m%d')
    if end_date is None:
        end_date = max(lhb_df.index).strftime('%Y%m%d')

    # 获取上证指数数据
    sh_df = ak.stock_zh_index_daily(symbol="sh000001")

    # 处理上证指数数据
    sh_df['date'] = pd.to_datetime(sh_df['date'])
    sh_df.set_index('date', inplace=True)
    sh_df = sh_df.loc[start_date:end_date]
    
    # 设置matplotlib使用Agg后端，避免字体问题
    import matplotlib
    matplotlib.use('Agg')
    
    # 尝试使用更多可能存在的字体
    plt.rcParams['font.sans-serif'] = ['Liberation Sans', 'DejaVu Sans', 'Noto Sans CJK SC', 'WenQuanYi Zen Hei', 'WenQuanYi Micro Hei', 'SimHei', 'sans-serif']
    # 如果字体仍有问题，可以禁用中文标题，使用英文
    
    # 计算图表宽度
    start_dt = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date)
    year_diff = (end_dt - start_dt).days / 200
    fig_width = max(30, year_diff * 15)  # 每年15个单位宽度，最小宽度为30

    # 创建图表
    fig = plt.figure(figsize=(fig_width, 10))

    # 设置子图之间的间距
    plt.subplots_adjust(hspace=0.1)

    # 上方K线图
    ax1 = plt.subplot2grid((5, 1), (0, 0), rowspan=3)
    mc = mpf.make_marketcolors(up='red', down='green',
                                 edge='inherit',
                                 wick='inherit',
                                 volume='in')
    s = mpf.make_mpf_style(marketcolors=mc)
    mpf.plot(sh_df, type='candle', style=s,
             ylabel='Index Price',
             ax=ax1,
             volume=False,
             axtitle='Shanghai Index & LHB Count')

    # 清空上方K线图的x轴标签
    ax1.set_xticklabels([])

    # 设置x轴标签只显示月初和月中
    ax1.xaxis.set_major_locator(plt.MaxNLocator(20))  # 限制最大刻度数
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: sh_df.index[int(x)].strftime('%m.%d') if x >= 0 and x < len(sh_df) and (sh_df.index[int(x)].day == 1 or sh_df.index[int(x)].day == 15) else ''))
    ax1.tick_params(axis='x', rotation=45)

    # 在K线图上添加龙虎榜数量标注
    for idx, date in enumerate(sh_df.index):
        if date in lhb_df.index:
            count = lhb_df.loc[date, 'count']
            ax1.text(idx, sh_df.loc[date, 'high'], str(count),
                     verticalalignment='bottom',
                     horizontalalignment='center',
                     fontsize=10)

    # 下方龙虎榜数量柱状图
    ax2 = plt.subplot2grid((5, 1), (3, 0), rowspan=2, sharex=ax1)  # 恢复共享x轴
    # 筛选指定日期范围的龙虎榜数据
    lhb_df_filtered = lhb_df.loc[start_date:end_date]
    bars = lhb_df_filtered['count'].plot(kind='bar', ax=ax2, color='blue', alpha=0.7)
    ax2.set_ylabel('Long Hu Bang')

    # 清除原有的x轴标签设置
    ax2.xaxis.set_major_formatter(plt.NullFormatter())

    # 手动添加日期标签
    for idx, date in enumerate(lhb_df_filtered.index):
        # 检查是否为年初（1月份）
        if date.month == 1 and (date.day <= 5):
            label = date.strftime('%Y.%m.%d')
        # 检查是否为月初（1-5日）或月中（13-17日）
        elif (date.day <= 5) or (13 <= date.day <= 17):
            label = date.strftime('%m.%d')
        else:
            continue  # 跳过不需要标签的日期
            
        # 在适当位置添加文本标签
        ax2.text(idx, -max(lhb_df_filtered['count'])*0.1, label, 
                 rotation=45, ha='center', va='top', fontsize=8)

    # 在柱状图上添加数值标注
    for idx, count in enumerate(lhb_df_filtered['count']):
        ax2.text(idx, count, str(count),
                 verticalalignment='bottom',
                 horizontalalignment='center',
                 fontsize=10)

    # 调整布局
    plt.tight_layout()

    # 保存图表
    image_path = f'{start_date}-{end_date}.png'
    plt.savefig(image_path)
    plt.close()
    
    return image_path

if __name__ == '__main__':
    plot_kline()