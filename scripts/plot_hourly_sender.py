import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import seaborn as sns
import numpy as np

def plot_hourly_sender(df, font_path = '/System/Library/Fonts/PingFang.ttc'):
    # 设置中文字体
    try:
        font = FontProperties(fname=font_path)
    except:
        print("警告：未找到指定字体文件，将尝试使用系统默认字体")
        font = FontProperties()
    
    # 设置全局样式
    plt.style.use('seaborn')
    colors = ['#FF6B6B', '#4ECDC4']
    
    # 1. 聊天消息比例分布图
    sender_counts = df['NickName'].value_counts()
    plt.figure(figsize=(10, 8))
    plt.pie(sender_counts, 
            labels=sender_counts.index, 
            autopct='%1.1f%%',
            colors=colors,
            textprops={'fontproperties': font, 'size': 12},
            wedgeprops={'width': 0.7, 'edgecolor': 'white'})
    plt.title('聊天消息比例分布', fontproperties=font, size=16, pad=20)
    plt.axis('equal')
    plt.savefig('figs/chat_ratio.png', dpi=300)
    # plt.close()

    # 2. 24小时聊天数量分布图
    df['hour'] = df['StrTime'].dt.hour
    hourly_counts = df['hour'].value_counts().sort_index()

    plt.figure(figsize=(15, 8))
    sns.barplot(x=hourly_counts.index, 
                y=hourly_counts.values, 
                color=colors[0],
                alpha=0.7)
    plt.title('24小时聊天数量分布', fontproperties=font, size=16, pad=20)
    plt.xlabel('小时', fontproperties=font, size=12)
    plt.ylabel('消息数量', fontproperties=font, size=12)
    plt.xticks(range(24), size=10)
    plt.yticks(size=10)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.savefig('figs/hourly_distribution.png', dpi=300)
    # plt.show()
    
    # 3. 双方24小时聊天频率对比图
    hourly_by_sender = df.groupby(['hour', 'NickName']).size().unstack()
    
    # 创建新的图形
    plt.figure(figsize=(18, 8))
    
    # 为每个发送者绘制柱状图
    bar_width = 0.35
    index = np.arange(24)
    
    # 获取发送者名称
    senders = hourly_by_sender.columns
    
    # 绘制柱状图
    plt.bar(index - bar_width/2, hourly_by_sender[senders[0]], 
            bar_width, alpha=0.7, color=colors[0], label=senders[0])
    plt.bar(index + bar_width/2, hourly_by_sender[senders[1]], 
            bar_width, alpha=0.7, color=colors[1], label=senders[1])
    
    plt.title('双方24小时聊天频率对比', fontproperties=font, size=16, pad=20)
    plt.xlabel('小时', fontproperties=font, size=12)
    plt.ylabel('消息数量', fontproperties=font, size=12)
    plt.xticks(index, range(24), size=10)
    plt.yticks(size=10)
    
    # 添加图例
    plt.legend(prop=font, loc='upper right')
    
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig('figs/hourly_comparison.png', dpi=300)
    plt.show()

    # 打印统计信息
    print("\n消息统计：")
    print(f"总消息数：{len(df)}")
    print("\n每个用户的消息数：")
    print(sender_counts)
    
def plot_yearly_ratio(df, font_path = '/System/Library/Fonts/PingFang.ttc'):
    try:
        font = FontProperties(fname=font_path)
    except:
        print("警告：未找到指定字体文件，将尝试使用系统默认字体")
        font = FontProperties()

    plt.style.use('seaborn')
    
    # 设置颜色方案和样式
    colors = ['#FF6B6B', '#4ECDC4']  # 使用统一的配色
    
    # 按年份和昵称分组统计消息数量
    yearly_sender_counts = df.groupby([df['StrTime'].dt.year, 'NickName']).size().unstack()
    
    # 计算总年份数用于设置子图
    n_years = len(yearly_sender_counts)
    n_rows = (n_years + 2) // 3
    n_cols = min(2, n_years)
    
    # 创建新的图形
    fig = plt.figure(figsize=(15, 6 * n_rows))
    fig.patch.set_facecolor('#F8F9FA')  # 设置背景色
    
    # 为每一年创建饼图
    for idx, (year, data) in enumerate(yearly_sender_counts.iterrows(), 1):
        ax = plt.subplot(n_rows, n_cols, idx)
        
        # 绘制饼图
        wedges, texts, autotexts = plt.pie(
            data, 
            labels=data.index,
            colors=colors,
            autopct='%1.1f%%',
            pctdistance=0.85,
            wedgeprops={
                'width': 0.7,  # 设置为环形图
                'edgecolor': 'white',
                'linewidth': 2
            },
            textprops={
                'fontproperties': font,
                'size': 12,
                'color': '#2C3E50'
            }
        )
        
        # 设置百分比文字的样式
        plt.setp(autotexts, size=10, weight="bold")
        
        # 添加年份标题
        plt.title(f'{year}年聊天比例', 
                 fontproperties=font,
                 pad=20,
                 size=14,
                 weight='bold',
                 color='#2C3E50')
        
        # 添加总消息数说明
        total_messages = data.sum()
        ax.text(0, -1.3, 
                f'总消息数: {total_messages:,}',
                ha='center',
                fontproperties=font,
                size=10,
                color='#666666')
        
        plt.axis('equal')
    
    # 调整子图之间的间距
    plt.tight_layout(pad=3.0)
    
    # 添加总标题
    fig.suptitle('年度聊天比例变化',
                 fontproperties=font,
                 size=16,
                 weight='bold',
                 color='#2C3E50',
                 y=0.98)
    
    # 保存图片
    fig.savefig('figs/yearly_sender_ratio.png', 
                format='png',
                dpi=300,
                facecolor=fig.get_facecolor(),
                edgecolor='none')
    plt.show()
    
    