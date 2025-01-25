from typing import List
import matplotlib.pyplot as plt

class JMModel:
    def __init__(self):
        """
        初始化JMModel类的实例。

        该方法设置了类的初始状态，包括时间列表t、参数ex和ey、根值root、初始故障数N0和故障强度Fi。
        """
        self.t = []  # 存储故障时间的列表，初始为空列表
        self.ex = None  # 参数ex，初始值为None
        self.ey = None  # 参数ey，初始值为None
        self.root = 0  # 用于计算的根值，初始值为0
        self.N0 = 0  # 初始故障数，初始值为0
        self.Fi = 0  # 故障强度，初始值为0

    def getP(self, lst: List[float]) -> float:
        """
        计算故障时间的累积故障数。

        :param lst: 故障时间列表。
        :return: 累积故障数。
        """
        result = 0
        n = len(lst)
        for i in range(1, n):
            t1 = lst[i]
            t2 = lst[i - 1]
            result += (i - 1) * (t1 - t2)
        tn = lst[-1]
        result /= tn
        return result

    def function(self, lst: List[float], N: float) -> float:
        """
        计算给定N值下的函数值。

        :param lst: 故障时间列表。
        :param N: 待计算的N值。
        :return: 函数值。
        """
        result = 0
        n = len(lst)
        P = self.getP(lst)
        for i in range(1, n):
            result += 1 / (N - i + 1)
        result -= (n - 1) / (N - P)
        return result

    def read_data(self):
        """
        从文件中读取故障数据。

        该方法从名为"test.txt"的文件中读取故障数据，并将故障时间存储在t列表中。
        """
        with open("test.txt", 'r') as input_file:
            for line in input_file:
                failure_Number, Timetofailure = map(int, line.strip().split())
                self.t.append(float(Timetofailure))

    def set_ex_ey(self):
        """
        设置ex和ey的值。

        该方法通过用户输入获取ex和ey的值，并将其存储在类的属性中。
        """
        self.ex = float(input("请输入ex的值："))
        self.ey = float(input("请输入ey的值："))

    def calculate(self):
        """
        计算N0和Fi的值。

        该方法根据读取的故障数据和设置的ex、ey值，计算N0和Fi的值。
        """
        n = len(self.t)

        P = self.getP(self.t)
        # print(f"当ex={self.ex},ey={self.ey}时")

        # 以下是根据P值与((n - 1) / 2)的比较结果来确定后续计算的初始边界值left和right
        if P > ((n - 1) / 2):
            left = n - 1
            right = n
        else:
            return  # 如果P不满足大于((n - 1) / 2)的条件，则直接返回，不进行后续复杂计算。

        # 以下循环用于通过不断调整right的值，使得function(self.t, right) <= self.ey
        while self.function(self.t, right) > self.ey:
            left = right
            right += 1

        # 经过上述循环后，根据function(self.t, right)与self.ex的比较结果，确定self.root的值
        if self.function(self.t, right) >= self.ex:
            self.root = right
        else:
            while True:
                # 以下是一个二分查找类似的循环，用于更精确地确定self.root的值，使得function(self.t, self.root)在一定误差范围内满足条件
                if abs(right - left) < self.ex:
                    self.root = (right + left) / 2
                    break
                self.root = (right + left) / 2
                if self.function(self.t, self.root) > self.ey:
                    left = self.root
                else:
                    if self.function(self.t, self.root) < (-self.ey):
                        right = self.root
                    else:
                        break

        # 至此，已经确定了self.root的值，接下来根据已确定的值以及之前读取的故障时间数据来计算N0和Fi

        self.N0 = self.root
        sum_val = 0
        tn = self.t[-1]
        for i in range(1, n):
            t1 = self.t[i]
            t2 = self.t[i - 1]
            sum_val += (i - 1) * (t1 - t2)
        self.Fi = (n - 1) / (self.N0 * tn - sum_val)

    def print_results(self):
        """
        打印计算结果。

        该方法打印出ex、ey、N0和Fi的值。
        """
        print(f"当ex={self.ex},ey={self.ey}时")
        print(f"N0={self.N0}")
        print(f"Fi={self.Fi}")

    def calculate_MTBF(self):
        """
        计算JM模型的平均故障间隔时间（MTBF）。

        :return: 平均故障间隔时间（MTBF）。
        """
        MTBF = 1 / self.Fi
        # print(f"MTBF: {MTBF}")
        return MTBF

    def calculate_failure_rate_mean(self):
        """
        计算JM模型的失效率均值。

        :return: 失效率均值。
        """
        n = len(self.t)
        failure_rate_sum = 0
        for i in range(1, n):
            t1 = self.t[i]
            t2 = self.t[i - 1]
            failure_rate_sum += self.Fi * (n - (i - 1)) * (t1 - t2)
        failure_rate_mean = failure_rate_sum / (self.t[-1])
        # print(f"失效率均值: {failure_rate_mean}")
        return failure_rate_mean