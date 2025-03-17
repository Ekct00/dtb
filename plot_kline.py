import json
import akshare as ak
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
from datetime import datetime

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # macOS系统自带的支持中文的字体
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

# 获取上证指数数据
start_date = min(lhb_df.index).strftime('%Y%m%d')
end_date = max(lhb_df.index).strftime('%Y%m%d')
sh_df = ak.stock_zh_index_daily(symbol="sh000001")

# 处理上证指数数据
sh_df['date'] = pd.to_datetime(sh_df['date'])
sh_df.set_index('date', inplace=True)
sh_df = sh_df.loc[start_date:end_date]

# 计算图表宽度
min_date = min(lhb_df.index)
max_date = max(lhb_df.index)
year_diff = (max_date - min_date).days / 200
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
         ylabel='指数价格',
         ax=ax1,
         volume=False,
         axtitle='上证指数K线图与龙虎榜数量对比')

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
bars = lhb_df['count'].plot(kind='bar', ax=ax2, color='blue', alpha=0.7)
ax2.set_ylabel('龙虎榜数量')

# 清除原有的x轴标签设置
ax2.xaxis.set_major_formatter(plt.NullFormatter())

# 手动添加日期标签
for idx, date in enumerate(lhb_df.index):
    # 检查是否为年初（1月份）
    if date.month == 1 and (date.day <= 5):
        label = date.strftime('%Y.%m.%d')
    # 检查是否为月初（1-5日）或月中（13-17日）
    elif (date.day <= 5) or (13 <= date.day <= 17):
        label = date.strftime('%m.%d')
    else:
        continue  # 跳过不需要标签的日期
        
    # 在适当位置添加文本标签
    ax2.text(idx, -max(lhb_df['count'])*0.1, label, 
             rotation=45, ha='center', va='top', fontsize=8)

# 在柱状图上添加数值标注
for idx, count in enumerate(lhb_df['count']):
    ax2.text(idx, count, str(count),
             verticalalignment='bottom',
             horizontalalignment='center',
             fontsize=10)

# 调整布局
plt.tight_layout()

# 保存图表
plt.savefig(f'{start_date}-{end_date}.png')
plt.close()