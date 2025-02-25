import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties
from matplotlib.colors import LinearSegmentedColormap
import os
import numpy as np
# 查找系统中的中文字体
import matplotlib.font_manager as fm

from plot_yearly_heatmaps import plot_yearly_heatmaps
from plot_hourly_sender import plot_hourly_sender
from plot_hourly_sender import plot_yearly_ratio


# MacOS系统
font_path = '/System/Library/Fonts/PingFang.ttc'  # 苹方字体

try:
    font = FontProperties(fname=font_path)
except:
    print("警告：未找到指定字体文件，将尝试使用系统默认字体")
    font = FontProperties()

plt.style.use('seaborn')

# 读取数据
df = pd.read_csv('data/msg.csv')

# 将时间字符串转换为datetime对象
df['StrTime'] = pd.to_datetime(df['StrTime'])

# 绘制年份比例
plot_yearly_ratio(df)

# 绘制年份热力图
plot_yearly_heatmaps(df)

# 绘制小时发送者比例
plot_hourly_sender(df)



