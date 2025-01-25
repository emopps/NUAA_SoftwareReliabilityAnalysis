import numpy as np
from scipy import interpolate


class EMDModel:
    def __init__(self, datax, datay):
        """
        初始化EMD模型的对象

        此方法在创建EMDModel类的实例时被调用，用于初始化对象的属性。

        参数:
        datax (numpy.ndarray或类似可迭代对象): 数据的x值序列。
        datay (numpy.ndarray或类似可迭代对象): 数据的y值序列，与datax中的元素一一对应。
        """
        self.datax = datax  # 存储输入数据的x值序列，用于后续各种计算和操作
        self.datay = datay  # 存储输入数据的y值序列，与datax相对应，是主要的分析对象
        self.H = []  # 用于储存通过后续处理得到的IMF（本征模态函数）分量，初始化为空列表

    def FindMax(self, Datax, Datay):
        """
        寻找数据中的极大值点

        该方法遍历输入的数据序列，按照一定的条件判断并找出其中的极大值点及其对应的x值。

        参数:
        Datax (numpy.ndarray或类似可迭代对象): 待分析数据的x值序列。
        Datay (numpy.ndarray或类似可迭代对象): 待分析数据的y值序列，与Datax中的元素一一对应。

        返回:
        tuple: 包含两个列表，第一个列表是极大值点对应的x值，第二个列表是极大值点对应的y值。
        """
        x, y = [], []  # 初始化用于存储极大值点的x值和y值的空列表

        if Datay[0] >= Datay[1]:  # 如果第一个数据点的y值大于等于第二个数据点的y值
            x.append(1)  # 将x值设为1（可能是数据序列的索引从1开始的一种约定，具体需根据数据含义确定）
            y.append(Datay[0])  # 将第一个数据点的y值作为极大值点的y值

        for i in range(1, len(Datax) - 2):  # 遍历数据序列中除了首尾几个特殊点之外的部分
            if Datay[i] >= Datay[i + 1] and Datay[i] >= Datay[i - 1]:  # 如果当前数据点的y值大于等于前后相邻数据点的y值
                x.append(Datax[i])  # 将当前数据点的x值添加到极大值点的x值列表中
                y.append(Datay[i])  # 将当前数据点的y值添加到极大值点的y值列表中

        if Datay[len(Datax) - 1] >= Datay[len(Datax) - 2]:  # 如果最后一个数据点的y值大于等于倒数第二个数据点的y值
            x.append(Datax[len(Datax) - 1])  # 将最后一个数据点的x值添加到极大值点的x值列表中
            y.append(Datay[len(Datax) - 1])  # 将最后一个数据点的y值添加到极大值点的y值列表中

        return x, y  # 返回极大值点对应的x值和y值的列表

    def FindMin(self, Datax, Datay):
        """
        寻找数据中的极小值点

        与FindMax方法类似，该方法用于遍历输入的数据序列，找出其中的极小值点及其对应的x值。

        参数:
        Datax (numpy.ndarray或类似可迭代对象): 待分析数据的x值序列。
        Datay (numpy.ndarray或类似可迭代对象): 待分析数据的y值序列，与Datax中的元素一一对应。

        返回:
        tuple: 包含两个列表，第一个列表是极小值点对应的x值，第二个列表是极小值点对应的y值。
        """
        x, y = [], []  # 初始化用于存储极小值点的x值和y值的空列表

        if Datay[0] <= Datay[1]:  # 如果第一个数据点的y值小于等于第二个数据点的y值
            x.append(Datax[0])  # 将第一个数据点的x值添加到极小值点的x值列表中
            y.append(Datay[0])  # 将第一个数据点的y值添加到极小值点的y值列表中

        for i in range(1, len(Datax) - 1):  # 遍历数据序列中除了首尾特殊点之外的部分
            if Datay[i] <= Datay[i + 1] and Datay[i] <= Datay[i - 1]:  # 如果当前数据点的y值小于等于前后相邻数据点的y值
                x.append(Datax[i])  # 将当前数据点的x值添加到极小值点的x值列表中
                y.append(Datay[i])  # 将当前数据点的y值添加到极小值点的y值列表中

        if Datay[len(Datax) - 1] <= Datay[len(Datax) - 2]:  # 如果最后一个数据点的y值小于等于倒数第二个数据点的y值
            x.append(Datax[len(Datax) - 1])  # 将最后一个数据点的x值添加到极小值点的x值列表中
            y.append(Datay[len(Datax) - 1])  # 将最后一个数据点的y值添加到极小值点的y值列表中

        return x, y  # 返回极小值点对应的x值和y值的列表

    def getCubicLine(self, Datax, Datay, length):
        """
        获取极大值和极小值点的包络线

        该方法首先找到数据的极大值点和极小值点，然后利用插值函数生成通过这些极值点的三次样条曲线，作为包络线。

        参数:
        Datax (numpy.ndarray或类似可迭代对象): 待分析数据的x值序列。
        Datay (numpy.ndarray或类似可迭代对象): 待分析数据的y值序列，与Datax中的元素一一对应。
        length (int): 生成包络线时使用的x值序列长度，通常用于控制包络线的分辨率。

        返回:
        tuple: 包含两条曲线的y值序列，分别是极大值点包络线的y值序列和极小值点包络线的y值序列。
        """
        x, y = self.FindMax(Datax, Datay)  # 找到数据中的极大值点及其对应的x值和y值
        tck = interpolate.splrep(x, y, k=3)  # 使用scipy的插值函数生成通过极大值点的三次样条函数的表示形式
        xx = np.linspace(min(Datax), max(Datax), length)  # 生成在Datax的最小值和最大值之间等间距的x值序列，用于计算包络线的y值
        ymax = interpolate.splev(xx, tck, der=0)  # 通过三次样条函数计算极大值点包络线的y值序列

        x, y = self.FindMin(Datax, Datay)  # 找到数据中的极小值点及其对应的x值和y值
        tck = interpolate.splrep(x, y, k=3)  # 使用scipy的插值函数生成通过极小值点的三次样条函数的表示形式
        ymin = interpolate.splev(xx, tck, der=0)  # 通过三次样条函数计算极小值点包络线的y值序列

        return ymax, ymin  # 返回极大值点包络线的y值序列和极小值点包络线的y值序列

    def FindZeros(self, Datax, Datay):
        """
        找到过零点的数量

        该方法遍历数据序列，检查相邻数据点的y值乘积是否小于零，以此来确定过零点的数量。

        参数:
        Datax (numpy.ndarray或类似可迭代对象): 待分析数据的x值序列。
        Datay (numpy.ndarray或类似可迭代对象): 待分析数据的y值序列，与Datax中的元素一一对应。

        返回:
        int: 过零点的数量。
        """
        num = 0  # 初始化过零点数量为0
        for i in range(0, len(Datax) - 1):  # 遍历数据序列中除了最后一个数据点之外的部分
            if Datay[i] * Datay[i + 1] < 0:  # 如果相邻两个数据点的y值乘积小于零，说明存在过零点
                num += 1  # 过零点数量加1
        return num  # 返回过零点的数量

    def is_IMF(self, Hdata):
        """
        判断是否为IMF分量

        该方法根据一系列条件判断输入的数据序列是否符合IMF（本征模态函数）的定义。

        参数:
        Hdata (numpy.ndarray或类似可迭代对象): 待判断的数据序列。

        返回:
        bool: 如果数据序列符合IMF的定义，则返回True；否则返回False。
        """
        x = np.linspace(1, len(Hdata), len(Hdata))  # 生成与输入数据序列长度相同的等间距x值序列，可能用于后续分析与数据序列的对应关系
        xx, y1 = self.FindMax(x, Hdata)  # 找到数据序列中的极大值点及其对应的x值和y值
        xx, y2 = self.FindMin(x, Hdata)  # 找到数据序列中的极小值点及其对应的x值和y值
        num1 = len(y1) + len(y2)  # 计算极大值点和极小值点的总数
        num2 = self.FindZeros(x, Hdata)  # 找到数据序列中的过零点数量

        # 判断局部极值点的数量和过零点的数量是否相等（允许有一定的误差，这里误差范围设定为相差不超过1）
        flag1 = abs(num1 - num2) <= 1

        ymax, ymin = self.getCubicLine(x, Hdata, len(Hdata))  # 获取数据序列的极大值点和极小值点的包络线
        yaver = (ymax + ymin) / 2  # 计算包络线的平均值
        num3 = 0
        error = 0.1
        for i in  range(0, len(Hdata)):
            if abs(yaver[i]) < error:  # 如果包络线平均值的绝对值小于设定的误差值
                num3 += 1  # 满足条件的点数量加1
        flag2 = num3 / len(Hdata) >= 0.95  # 判断满足条件的点占总点数的比例是否达到设定的阈值

        return flag1 and flag2  # 如果两个条件都满足，则返回True，表示是IMF分量；否则返回False

    def CalSD(self, h_k_1, h_k):
        """
        计算SD值

        该方法根据输入的两个数据序列计算它们之间的SD（标准偏差）值。

        参数:
        h_k_1 (numpy.ndarray或类似可迭代对象): 第一个数据序列。
        h_k (numpy.ndarray或类似可迭代对象): 第二个数据序列。

        返回:
        float: 计算得到的SD值。
        """
        SD = h_k_1 - h_k  # 计算两个数据序列对应元素的差值
        SD = np.sum(SD * SD)  # 计算差值的平方和
        SD = SD / np.sum(h_k * h_k)  # 将差值的平方和除以第二个数据序列的平方和，得到SD值

        return SD  # 返回计算得到的SD值

    def extract_imf(self, N=3):
        """
        提取多个IMF分量

        该方法通过迭代的方式从输入数据中提取指定数量的IMF分量。

        参数:
        N (int, 可选): 要提取的IMF分量数量，默认值为3。

        返回:
        tuple: 包含两个元素，第一个元素是提取得到的IMF分量列表，第二个元素是提取完IMF分量后剩余的数据。
        """
        InitalData = self.datay  # 将输入数据的y值序列作为初始数据
        for j in range(1, N + 1):  # 进行指定次数的迭代提取
            ymax, ymin = self.getCubicLine(self.datax, InitalData, len(self.datax))  # 获取当前数据的极大值点和极小值点的包络线
            # self.draw(self.datax, InitalData, ymax, ymin, len(self.datax))  # 可能是用于绘制相关图形的函数，这里暂时注释掉

            m = (ymax + ymin) / 2  # 计算包络线的平均值
            h = InitalData - m  # 用初始数据减去包络线平均值得到中间数据
            is_accept = self.is_IMF(h)  # 判断中间数据是否符合IMF分量的定义

            num = 0
            while not is_accept:  # 如果不符合IMF分量的定义，则进行循环调整
                num += 1
                PreH = h  # 记录当前的中间数据
                ymax, ymin = self.getCubicLine(self.datax, PreH, len(self.datax))  # 获取新的包络线
                m = (ymax + ymin) / 2  # 计算新的包络线平均值
                h = PreH - m  # 用之前的中间数据减去新的包络线平均值得到新的中间数据
                is_accept = self.is_IMF(h)  # 再次判断新的中间数据是否符合IMF分量的定义

            self.H.append(h)  # 将符合IMF分量定义的中间数据添加到IMF分量列表中
            InitalData = InitalData - h  # 用初始数据减去已提取的IMF分量，得到剩余的数据用于下一次迭代

        return self.H, InitalData  # 返回提取得到的IMF分量列表和剩余的数据

    def fit_residual(self, degree=3):
        """
        对余量进行多项式拟合

        该方法使用多项式拟合的方式对剩余的数据（可能是提取完IMF分量后剩余的数据）进行拟合，得到拟合后的预测值。

        参数:
        degree (int, 可选): 多项式的次数，默认值为3。

        返回:
        numpy.ndarray: 拟合后的预测值序列，与输入数据的x值序列相对应。
        """
        z1 = np.polyfit(self.datax, self.datay, degree)  # 使用numpy的polyfit函数根据输入数据的x值和y值序列以及指定的多项式次数，拟合得到多项式的系数
        p1 = np.poly1d(z1)  # 根据拟合得到的系数创建一个多项式对象
        y_pred = p1(self.datax)  # 使用多项式对象计算在输入数据的x值序列上的预测值

        return y_pred  # 返回拟合后的预测值序列