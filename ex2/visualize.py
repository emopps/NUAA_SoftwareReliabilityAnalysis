import numpy as np
import matplotlib.pyplot as plt
from GM import GMModel
from EMD import EMDModel

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的"-"负号的乱码问题

def visualize_models():
    """
    可视化模型拟合对比的函数。

    该函数生成了数据，初始化了GM模型和EMD模型实例，设置了模型参数，计算了相关参数，
    并绘制了原始数据、GM模型和EMD模型的拟合曲线。
    """
    # 生成数据
    datax = np.linspace(1, 34, 34)  # 生成从1到34的等间隔的34个数据点作为x轴数据
    datay = np.array([9, 12, 11, 4, 7, 2, 5, 8, 5, 7, 1, 6, 1, 9, 4, 1, 3, 8, 6, 1, 1, 33, 7, 91, 2, 1, 87, 47, 12, 9, 135, 258, 16, 35], float)  # 给定的y轴数据点

    # GM模型
    gm_model = GMModel()  # 初始化GM模型实例
    gm_model.set_model(datay.tolist())  # 设置GM模型的参数为给定的y轴数据点列表
    gm_predicted = gm_model.get_predicted_data()  # 获取GM模型对实验数据的拟合值数组

    # EMD模型
    emd_model = EMDModel(datax, datay)  # 初始化EMD模型实例，传入x轴和y轴数据
    imfs, residual = emd_model.extract_imf(N=2)  # 从输入数据中提取指定数量的IMF分量
    emd_predicted = emd_model.fit_residual(degree=3)  # 对剩余数据进行拟合，获取拟合值

    plt.figure(figsize=(10, 6))  # 创建一个新的图形，设置图形大小为10x6英寸
    plt.plot(datax, datay, 'o', label='原始数据', color='black')  # 绘制原始数据点，用黑色圆圈表示，添加标签“原始数据”
    plt.plot(datax, gm_predicted, label='GM模型拟合', linestyle='-', color='blue')  # 绘制GM模型的拟合曲线，用蓝色实线表示，添加标签“GM模型拟合”
    plt.plot(datax, emd_predicted, label='EMD模型拟合', linestyle='--', color='red')  # 绘制EMD模型的拟合曲线，用红色虚线表示，添加标签“EMD模型拟合”
    plt.title('模型拟合对比')  # 设置图形标题为“模型拟合对比”
    plt.xlabel('数据x值')  # 设置x轴标签为“数据x值”
    plt.ylabel('数据y值')  # 设置y轴标签为“数据y值”
    plt.legend()  # 显示图例
    plt.show()  # 显示图形


if __name__ == "__main__":
    visualize_models()