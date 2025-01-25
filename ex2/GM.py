import numpy as np


class GMModel:
    def __init__(self):
        """
        初始化GMModel类的实例。

        在这里定义了一系列用于存储模型相关数据和参数的属性，初始化为空的numpy数组或零值。
        """
        self.test_data = np.array(())  # 用于存储实验数据集，初始为空数组
        self.add_data = np.array(())  # 存储一次累加产生的数据，初始为空数组
        self.argu_a = 0  # 模型的参数a，初始化为0
        self.argu_b = 0  # 模型的参数b，初始化为0
        self.MAT_B = np.array(())  # 矩阵B，用于后续的计算，初始为空数组
        self.MAT_Y = np.array(())  # 矩阵Y，用于后续的计算，初始为空数组
        self.modeling_result_arr = np.array(())  # 存储对实验数据的拟合值，初始为空数组
        self.P = 0  # 小误差概率，初始化为0
        self.C = 0  # 后验方差比值，初始化为0

    def set_model(self, arr:list):
        """
        设置GM模型的参数并进行相关计算。

        该方法接收一个列表作为输入，通常是实验数据的列表形式。
        它会依次调用内部的几个私有方法来完成数据处理、参数计算和拟合值的获取。
        """
        self.__acq_data(arr)  # 调用私有方法获取数据并构建矩阵B和矩阵Y
        self.__compute()  # 调用私有方法计算模型的参数a和b
        self.__modeling_result()  # 调用私有方法获取对实验数据的拟合值

    def __acq_data(self, arr:list):
        """
        私有方法：获取并处理数据，构建矩阵B和矩阵Y。

        该方法将输入的列表数据转换为numpy数组，并进行一次累加操作，然后根据累加后的数据构建矩阵B和矩阵Y。

        参数:
        arr (list): 实验数据的列表形式。
        """
        self.test_data = np.array(arr).flatten()  # 将输入的列表转换为一维的numpy数组，作为实验数据集

        add_data = []
        sum_val = 0
        for i in range(len(self.test_data)):
            sum_val = sum_val + self.test_data[i]  # 对实验数据进行累加
            add_data.append(sum_val)
        self.add_data = np.array(add_data)  # 将累加后的数据转换为numpy数组

        ser = []
        for i in range(len(self.add_data) - 1):
            temp = (-1) * ((1 / 2) * self.add_data[i] + (1 / 2) * self.add_data[i + 1])
            ser.append(temp)
        B = np.vstack((np.array(ser).flatten(), np.ones(len(ser), ).flatten()))
        self.MAT_B = np.array(B).T  # 构建矩阵B并转置

        Y = np.array(self.test_data[1:])
        self.MAT_Y = np.reshape(Y, (len(Y), 1))  # 构建矩阵Y并重塑为列向量形式

    def __compute(self):
        """
        私有方法：计算模型的参数a和b。

        通过之前构建的矩阵B和矩阵Y，利用矩阵运算来计算出模型的两个重要参数a和b。
        """
        temp_1 = np.dot(self.MAT_B.T, self.MAT_B)  # 先计算矩阵B的转置与自身的点积
        temp_2 = np.matrix(temp_1).I  # 对上述结果求逆
        temp_3 = np.dot(np.array(temp_2), self.MAT_B.T)  # 再与矩阵B的转置做点积
        vec = np.dot(temp_3, self.MAT_Y)  # 最后与矩阵Y做点积得到包含参数a和b的向量

        self.argu_a = vec.flatten()[0]  # 从向量中获取参数a的值
        self.argu_b = vec.flatten()[1]  # 从向量中获取参数b的值

    def __predict(self, k:int) -> float:
        """
        私有方法：根据模型参数进行预测计算。

        基于已经计算出的参数a和b，以及给定的预测步数k，计算出相应的预测值。

        参数:
        k (int): 预测的步数。

        返回:
        float: 预测的值。
        """
        part_1 = 1 - np.exp(self.argu_a)  # 计算预测公式的第一部分
        part_2 = self.test_data[0] - self.argu_b / self.argu_a  # 计算预测公式的第二部分
        part_3 = np.exp((-1) * self.argu_a * k)  # 计算预测公式的第三部分

        return part_1 * part_2 * part_3  # 返回预测结果

    def __modeling_result(self):
        """
        私有方法：获取对实验数据的拟合值。

        通过调用__predict方法，依次计算出每个实验数据点对应的拟合值，并存储在modeling_result_arr中。
        """
        ls = [self.__predict(i + 1) for i in range(len(self.test_data) - 1)]
        ls.insert(0, self.test_data[0])
        self.modeling_result_arr = np.array(ls)  # 将计算出的拟合值转换为numpy数组并存储

    def predict(self, number:int) -> list:
        """
        根据模型进行外部预测。

        基于已经训练好的模型（即已经计算出参数a和b），对后续指定个数的数据进行预测。

        参数:
        number (int): 需要预测的数据个数。

        返回:
        list: 预测结果的列表形式。
        """
        prediction = [self.__predict(i + len(self.test_data)) for i in range(number)]
        return prediction

    def precision_evaluation(self):
        """
        对模型的精度进行评估。

        通过计算实验数据与拟合数据之间的误差，进而计算出平均误差、平均实验数据值等，最终得出小误差概率P和后验方差比值C。
        """
        error = [
            self.test_data[i] - self.modeling_result_arr[i]
            for i in range(len(self.test_data))
        ]  # 计算每个实验数据点与对应拟合值的误差

        aver_error = np.mean(error)  # 计算平均误差

        aver_test_data = np.mean(self.test_data)  # 计算平均实验数据值

        temp1 = 0
        temp2 = 0
        for i in range(len(error)):
            temp1 = temp1 + (self.test_data[i] - aver_test_data) ** 2
            temp2 = temp2 + (error[i] - aver_error) ** 2
        square_S_1 = temp1 / len(self.test_data)  # 计算实验数据的方差
        square_S_2 = temp2 / len(error)  # 计算误差的方差

        self.C = np.sqrt(square_S_2) / np.sqrt(square_S_1)  # 计算后验方差比值

        ls = [i
              for i in range(len(error))
              if np.abs(error[i] - aver_error) < (0.6745 * np.sqrt(square_S_1))
              ]
        self.P = len(ls) / len(error)  # 计算小误差概率

        # print("精度指标P,C值为：", self.P, self.C)

    def get_predicted_data(self):
        """
        获取模型对实验数据的拟合值。

        返回:
        numpy.ndarray: 模型对实验数据的拟合值数组。
        """
        return self.modeling_result_arr