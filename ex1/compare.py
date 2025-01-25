from JM import JMModel
from GO import GOModel
import os

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    while True:
        # 创建JMModel实例
        jm_model = JMModel()
        jm_model.read_data()
        jm_model.set_ex_ey()
        jm_model.calculate()
        jm_model.print_results()
        jm_model.calculate_MTBF()
        jm_model.calculate_failure_rate_mean()

        # 创建GOModel实例
        go_model = GOModel()
        go_model.read_data()
        go_model.set_epslv()
        go_model.calculate()
        go_model.print_results()
        go_model.calculate_MTBF()
        go_model.calculate_failure_rate_mean()

        # 计算并比较MTBF
        jm_MTBF = jm_model.calculate_MTBF()
        go_MTBF = go_model.calculate_MTBF()
        print(f"JM模型MTBF: {jm_MTBF}")
        print(f"GO模型MTBF: {go_MTBF}")
        if jm_MTBF > go_MTBF:
            print("在MTBF方面，JM模型表现更好。")
        elif jm_MTBF < go_MTBF:
            print("在MTBF方面，GO模型表现更好。")
        else:
            print("在MTBF方面，JM模型和GO模型表现相同。")

        # 计算并比较失效率均值
        jm_failure_rate_mean = jm_model.calculate_failure_rate_mean()
        go_failure_rate_mean = go_model.calculate_failure_rate_mean()
        print(f"JM模型失效率均值: {jm_failure_rate_mean}")
        print(f"GO模型失效率均值: {go_failure_rate_mean}")

        if jm_failure_rate_mean > go_failure_rate_mean:
            print("在失效率均值方面，GO模型表现更好。")
        elif jm_failure_rate_mean < go_failure_rate_mean:
            print("在失效率均值方面，JM模型表现更好。")
        else:
            print("在失效率均值方面，JM模型和GO模型表现相同。")