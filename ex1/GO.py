from typing import List
import math
import matplotlib.pyplot as plt


class GOModel:
    def __init__(self):
        """
        初始化GOModel类的实例。

        该方法设置了类的初始状态，包括时间列表t、精度参数epslv、参数a和b。
        """
        self.t = []  # 存储故障时间的列表，初始为空列表
        self.epslv = None  # 精度参数，初始值为None
        self.a = 0  # 参数a，初始值为0
        self.b = 0  # 参数b，初始值为0

    def Dfunction(self, lst: List[float]) -> float:
        """
        计算故障时间的累积故障数。

        :param lst: 故障时间列表。
        :return: 累积故障数。
        """
        result = 0
        n = len(lst)
        for i in range(1, n):
            t1 = lst[i]
            result += t1

        tn = lst[-1]
        result /= tn
        result /= n
        return result

    def read_data(self):
        """
        从文件中读取故障数据。

        该方法从名为"test.txt"的文件中读取故障数据，并将故障时间存储在t列表中。
        """
        try:
            with open("test.txt", 'r') as input_file:
                for line in input_file:
                    failure_Number, Timetofailure = map(int, line.strip().split())
                    self.t.append(float(Timetofailure))
        except FileNotFoundError:
            print("文件未找到，请检查文件路径是否正确。")

    def set_epslv(self):
        """
        设置精度参数epslv的值。

        该方法通过用户输入获取epslv的值，并将其存储在类的属性中。
        """
        self.epslv = float(input("请输入epslv的值："))

    def calculate(self):
        """
        计算模型的参数a和b。

        该方法根据读取的故障数据和设置的精度参数epslv，计算模型的参数a和b。
        """
        N = len(self.t)
        tn = self.t[-1]
        xl = 0
        xr = 0
        xm = 0
        D = self.Dfunction(self.t)
        f = 0

        # 步骤1: 判断D大小
        if 0 < D < 0.5:
            # 根据模型的要求，首先计算 `D` 值（通过调用 `self.Dfunction` 方法），然后判断 `D` 的范围。
            # 如果 `D` 的值在 `0` 和 `0.5` 之间，就按照特定公式设置 `xl` 和 `xr` 的初始值，这两个值将作为后续迭代计算的边界。
            # `xl` 和 `xr` 的设置是基于模型的理论和算法要求，为后续的迭代搜索确定一个初始的区间范围。
            xl = (1 - 2 * D) / 2
            xr = 1 / D
        else:
            # 如果 `D` 不在 `0` 到 `0.5` 这个范围内，说明当前的数据情况可能不满足模型的有效计算条件，
            # 所以直接返回，不进行后续的复杂计算流程。
            return

        # 转步骤2：
        max_iterations = 1000  # 设置一个最大迭代次数，防止无限循环
        iteration_count = 0

        while True:
            # 进入一个循环，这个循环的目的是通过不断迭代来逼近满足特定条件的 `xm` 值。
            # 每次迭代都会更新 `xm` 的值，并根据 `xm` 计算相关的函数值 `f`，然后根据 `f` 与 `self.epslv` 的比较结果来调整 `xl` 和 `xr` 的值，
            # 从而逐步缩小搜索范围，直到找到满足条件的 `xm` 值或者达到最大迭代次数。
            xm = (xl + xr) / 2
            if math.fabs(xr - xl) <= self.epslv:
                # 如果当前 `xr` 和 `xl` 的差值的绝对值小于等于用户设置的 `self.epslv` 值，说明已经找到了满足精度要求的 `xm` 值，
                # 此时就可以跳出循环，进入下一步的计算。
                break
            else:
                y = math.exp(xm)
                f = (1 - D * xm) * y + (D - 1) * xm - 1
                if f > self.epslv:
                    # 如果计算得到的函数值 `f` 大于 `self.epslv`，说明当前的 `xm` 值使得函数值偏大，
                    # 所以将 `xl` 更新为当前的 `xm` 值，以便在下一次迭代中缩小搜索范围，让函数值更接近目标范围。
                    xl = xm
                elif f < -self.epslv:
                    # 如果计算得到的函数值 `f` 小于负的 `self.epslv`，说明当前的 `xm` 值使得函数值偏小，
                    # 所以将 `xr` 更新为当前的 `xm` 值，同样是为了在下一次迭代中调整搜索范围，使函数值更符合要求。
                    xr = xm
                else:
                    # 如果函数值 `f` 在 `[-self.epslv, self.epslv]` 范围内，说明已经找到了满足精度要求的 `xm` 值，
                    # 直接跳出循环，不再进行后续的迭代调整。
                    break

            iteration_count += 1
            if iteration_count >= max_iterations:
                # 在每次迭代过程中，会记录迭代的次数。如果迭代次数达到了设置的最大迭代次数 `max_iterations`（这里设置为1000次），
                # 说明可能由于数据问题或者算法本身的原因，没有在规定的迭代次数内找到满足精度要求的 `xm` 值。
                # 此时会打印提示信息，告知用户可能需要检查数据或算法，然后直接返回，不再继续计算。
                print("达到最大迭代次数，可能未收敛，请检查数据或算法。")
                return

        # 步骤4
        b = xm / tn
        ahelp = math.exp(-b * tn)
        a = N / (1 - ahelp)

        # 在通过上述迭代过程找到满足精度要求的 `xm` 值后，就可以根据模型的公式计算出关键参数 `a` 和 `b` 的值。
        # 首先计算 `b` 值，它是 `xm` 与最后一个故障时间 `tn` 的比值。然后通过 `b` 值计算出 `ahelp`，再根据 `ahelp` 和数据长度 `N` 计算出 `a` 值。
        # 最后将计算得到的 `a` 和 `b` 值分别赋值给 `self.a` 和 `self.b`，以便在类的其他方法中可以使用这些计算出来的关键参数。
        self.a = a
        self.b = b

    def print_results(self):
        """
        打印计算结果。

        该方法打印出精度参数epslv、参数a和b的值。
        """
        print(f"当epslv={self.epslv}时，")
        print(f"a={self.a}")
        print(f"b={self.b}")

    def calculate_MTBF(self):
        """
        计算GO模型的平均故障间隔时间（MTBF）。
        :return: 平均故障间隔时间（MTBF）。
        """
        MTBF = 1 / self.b
        # print(f"MTBF: {MTBF}")
        return MTBF

    def calculate_failure_rate_mean(self):
        """
        计算GO模型的失效率均值。
        :return: 失效率均值。
        """
        N = len(self.t)
        failure_rate_sum = 0
        for i in range(0, N):
            failure_rate_sum += self.a * self.b * math.exp(-self.b * self.t[i])
        failure_rate_mean = failure_rate_sum / N
        # print(f"失效率均值: {failure_rate_mean}")
        return failure_rate_mean