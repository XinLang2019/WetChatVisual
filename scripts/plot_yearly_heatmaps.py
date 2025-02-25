import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties
from matplotlib.colors import LinearSegmentedColormap
import numpy as np



def plot_yearly_heatmaps(df, font_path = '/System/Library/Fonts/PingFang.ttc'):
    """
    绘制按年份分组的聊天频率热图
    
    参数:
    df: DataFrame, 包含 'StrTime' 列的聊天数据
    font_path: str, 中文字体路径
    """
    # 设置中文字体
    try:
        font = FontProperties(fname=font_path)
    except:
        print("警告：未找到指定字体文件，将尝试使用系统默认字体")
        font = FontProperties()

    plt.style.use('seaborn')
    
    # 计算每天的消息总数
    df['date'] = pd.to_datetime(df['StrTime']).dt.date
    daily_counts = df.groupby('date').size().reset_index(name='count')
    daily_counts['date'] = pd.to_datetime(daily_counts['date'])
    daily_counts['weekday'] = daily_counts['date'].dt.weekday

    # 确保日期连续
    date_range = pd.date_range(start=daily_counts['date'].min(), end=daily_counts['date'].max())
    full_dates = pd.DataFrame({'date': date_range})
    full_dates['weekday'] = full_dates['date'].dt.weekday
    daily_counts = full_dates.merge(daily_counts[['date', 'count']], 
                                  on='date', 
                                  how='left').fillna(0)

    # 将数据按年份分割
    df_2023 = daily_counts[(daily_counts['date'] >= '2023-01-01') & (daily_counts['date'] < '2024-01-01')]
    df_2024 = daily_counts[(daily_counts['date'] >= '2024-01-01') & (daily_counts['date'] < '2025-01-01')]
    df_2025 = daily_counts[daily_counts['date'] >= '2025-01-01']

    # 创建GitHub风格的颜色映射
    colors = ['#ebedf0', '#9be9a8', '#40c463', '#30a14e', '#216e39']
    custom_cmap = LinearSegmentedColormap.from_list("github", colors, N=5)

    # 获取全局最大值
    vmax_global = daily_counts['count'].quantile(0.95)

    # 创建图形
    fig = plt.figure(figsize=(16, 7))  # 减小图形整体大小
    gs = fig.add_gridspec(3, 2, 
                         width_ratios=[40, 1],  # 调整宽度比例
                         wspace=0.01,  # 减小水平间距
                         hspace=0.15,  # 减小垂直间距
                         left=0.02,    # 减小左边距
                         right=0.98,   # 增大右边距
                         top=0.95,     # 增大上边距
                         bottom=0.05)  # 减小下边距

    # 处理每一年的数据
    for idx, (year_df, year) in enumerate([(df_2023, 2023), (df_2024, 2024), (df_2025, 2025)]):
        # 确保日期连续
        start_date = pd.Timestamp(f'{year}-01-01')
        end_date = pd.Timestamp(f'{year}-12-31')
        date_range = pd.date_range(start=start_date, end=end_date)
        full_dates = pd.DataFrame({'date': date_range})
        full_dates['weekday'] = full_dates['date'].dt.weekday
        
        # 合并数据
        year_counts = full_dates.merge(year_df[['date', 'count']], 
                                     on='date', 
                                     how='left').fillna(0)
        
        # 创建热图矩阵
        total_weeks = int(np.ceil(len(year_counts) / 7))
        heatmap_data = np.zeros((7, total_weeks))
        
        for i, row in year_counts.iterrows():
            week_num = i // 7
            day_num = row['weekday']
            heatmap_data[day_num, week_num] = row['count']
        
        # 创建子图
        ax_heat = fig.add_subplot(gs[idx, 0])
        ax_cbar = fig.add_subplot(gs[idx, 1])
        
        # 设置坐标轴的纵横比
        ax_heat.set_aspect('equal')
        
        # 绘制热图
        sns.heatmap(heatmap_data,
                    cmap=custom_cmap,
                    cbar=True,
                    cbar_ax=ax_cbar,
                    ax=ax_heat,
                    cbar_kws={'label': '消息数量'},
                    yticklabels=['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
                    xticklabels=[],
                    square=True,
                    linewidths=0.5,
                    linecolor='white',
                    vmin=0,
                    vmax=vmax_global)
        
        # 设置标题和标签（减小间距）
        ax_heat.set_title(f'{year}年聊天频率', fontproperties=font, pad=3, fontsize=10)
        ax_heat.set_ylabel('星期', fontproperties=font, fontsize=8, labelpad=2)
        
        # 设置中文标签
        ax_heat.set_yticklabels(['周一', '周二', '周三', '周四', '周五', '周六', '周日'], 
                               fontproperties=font, 
                               fontsize=7)
        
        # 设置颜色条
        ax_cbar.tick_params(labelsize=7)
        ax_cbar.set_ylabel('消息数量', fontproperties=font, fontsize=7)
        
        # 添加月份分隔线和标签
        month_labels = []
        month_label_positions = []
        current_month = year_counts['date'].dt.month.iloc[0]
        
        for i, date in enumerate(year_counts['date']):
            if date.month != current_month:
                current_month = date.month
                month_labels.append(date.strftime('%b'))
                month_label_positions.append(i // 7)
                ax_heat.axvline(x=i/7, color='gray', linestyle='--', alpha=0.2, linewidth=0.3)
        
        # 设置月份标签
        ax_heat.set_xticks(month_label_positions)
        ax_heat.set_xticklabels(month_labels, fontproperties=font, fontsize=7)
        ax_heat.tick_params(axis='x', pad=2)

    # 保存图片时进一步减小边距
    plt.savefig('figs/yearly_heatmaps.png', 
                dpi=300, 
                bbox_inches='tight', 
                facecolor='white',
                pad_inches=0.01)  # 减小保存时的边距
    plt.show()
    
    # # 打印统计信息
    # for stats in yearly_stats:
    #     print(f"\n{stats['year']}年统计：")
    #     print(f"总消息数：{stats['total_messages']:.0f}")
    #     print(f"平均每天消息数：{stats['avg_daily']:.1f}")
    #     print(f"最活跃的一天：{stats['max_day'].strftime('%Y-%m-%d')}，")
    #     print(f"消息数：{stats['max_count']:.0f}")
    #     print(f"有聊天记录的天数：{stats['active_days']}天")
    
    