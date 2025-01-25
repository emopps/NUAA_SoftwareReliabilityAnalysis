import numpy as np
from GM import GMModel
from EMD import EMDModel

def compare_models():
    """
    比较GM模型和EMD模型的性能。

    该函数生成了数据，初始化了GM模型和EMD模型实例，设置了模型参数，计算了相关参数，
    并返回了GM模型和EMD模型的均方根误差（RMSE）和均值绝对误差（MAE）。
    """
    # 生成数据
    datax = np.linspace(1, 34, 34)  # 生成从1到34的等间隔的34个数据点作为x轴数据
    datay = np.array([9, 12, 11, 4, 7, 2, 5, 8, 5, 7, 1, 6, 1, 9, 4, 1, 3, 8, 6, 1, 1, 33, 7, 91, 2, 1, 87, 47, 12, 9, 135, 258, 16, 35], float)  # 给定的y轴数据点

    # GM模型
    gm_model = GMModel()  # 初始化GM模型实例
    gm_model.set_model(datay.tolist())  # 设置GM模型的参数为给定的y轴数据点列表
    gm_predicted = gm_model.modeling_result_arr  # 获取GM模型对实验数据的拟合值数组
    gm_residuals = datay - gm_predicted  # 计算GM模型的残差

    # EMD模型
    emd_model = EMDModel(datax, datay)  # 初始化EMD模型实例，传入x轴和y轴数据
    imfs, residual = emd_model.extract_imf(N=2)  # 从输入数据中提取指定数量的IMF分量
    emd_predicted = emd_model.fit_residual(degree=3)  # 对剩余数据进行拟合，获取拟合值
    emd_residuals = datay - emd_predicted  # 计算EMD模型的残差

    # 计算均方根误差（RMSE）
    gm_rmse = np.sqrt(np.mean(gm_residuals ** 2))  # 计算GM模型的均方根误差（RMSE）
    emd_rmse = np.sqrt(np.mean(emd_residuals ** 2))  # 计算EMD模型的均方根误差（RMSE）

    # 计算均值绝对误差（MAE）
    gm_mae = np.mean(np.abs(gm_residuals))  # 计算GM模型的均值绝对误差（MAE）
    emd_mae = np.mean(np.abs(emd_residuals))  # 计算EMD模型的均值绝对误差（MAE）

    return gm_rmse, emd_rmse, gm_mae, emd_mae  # 返回GM模型和EMD模型的均方根误差（RMSE）和均值绝对误差（MAE）


if __name__ == "__main__":
    gm_rmse, emd_rmse, gm_mae, emd_mae = compare_models()

    print("GM模型均方根误差（RMSE）:", gm_rmse)
    print("EMD模型均方根误差（RMSE）:", emd_rmse)

    # 比较均方根误差（MSE）并输出结果
    if gm_rmse < emd_rmse:
        print("在均方根误差（RMSE）指标上，GM模型表现更好。")
    elif gm_rmse > emd_rmse:
        print("在均方根误差（RMSE）指标上，EMD模型表现更好。")
    else:
        print("在均方根误差（RMSE）指标上，GM模型和EMD模型表现相同。")
    
    print("GM模型均值绝对误差（MAE）:", gm_mae)
    print("EMD模型均值绝对误差（MAE）:", emd_mae)

    # 比较均值绝对误差（MAE）并输出结果
    if gm_mae < emd_mae:
        print("在均值绝对误差（MAE）指标上，GM模型表现更好。")
    elif gm_mae > emd_mae:
        print("在均值绝对误差（MAE）指标上，EMD模型表现更好。")
    else:
        print("在均值绝对误差（MAE）指标上，GM模型和EMD模型表现相同。")