import numpy as np
import matplotlib.pyplot as plt
from JM import JMModel
from GO import GOModel
import os

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的"-"负号的乱码问题

def visualize_models():
    """
    可视化模型拟合对比的函数。

    该函数初始化了JM模型和GO模型实例，读取数据，设置模型参数，计算相关参数，
    并绘制了原始数据、JM模型和GO模型的故障数量随时间的变化曲线。
    """
    # 初始化JM模型和GO模型实例
    jm_model = JMModel()
    go_model = GOModel()

    # 读取数据
    jm_model.read_data()
    go_model.read_data()

    # 设置JM模型参数
    jm_model.set_ex_ey()
    # 设置GO模型参数
    go_model.set_epslv()

    # 计算JM模型和GO模型的相关参数
    jm_model.calculate()
    go_model.calculate()

    # 时间范围
    time_range = np.linspace(0, 6000, 1000)

    # JM模型预测的故障数量
    jm_cumulative_failures = jm_model.N0 * (1 - np.exp(-jm_model.Fi * time_range))

    # GO模型预测的故障数量
    go_cumulative_failures = go_model.a * (1 - np.exp(-go_model.b * time_range))

    # 实际故障数量
    actual_cumulative_failures = np.arange(1, len(jm_model.t) + 1)

    # 绘图
    plt.figure(figsize=(10, 6))
    plt.plot(jm_model.t, actual_cumulative_failures, 'o', label='原始数据', color='black')
    plt.plot(time_range, jm_cumulative_failures, '-', label='JM模型', color='blue')
    plt.plot(time_range, go_cumulative_failures, '--', label='GO模型', color='red')

    # 设置图例和标签
    plt.title('模型拟合对比')
    plt.xlabel('数据x值')
    plt.ylabel('数据y值')
    plt.legend()
    plt.grid()
    plt.show()

# 调用可视化函数
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    visualize_models()