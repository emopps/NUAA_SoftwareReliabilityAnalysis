import tkinter as tk
from tkinter import messagebox, simpledialog
import fault_tree as ft
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FaultTreeGUI:
    def __init__(self, master):
        self.master = master
        master.title("故障树分析工具")
        master.geometry("400x200")  # 设置窗口大小为800x600像素
        # 创建按钮
        self.show_tree_button = tk.Button(master, text="显示故障树", command=self.show_fault_tree)
        self.show_tree_button.pack(side=tk.TOP, padx=20, pady=30)  # 将按钮放在顶部，

        self.calculate_importance_button = tk.Button(master, text="计算重要度", command=self.calculate_importance)
        self.calculate_importance_button.pack(side=tk.TOP, padx=20, pady=30)  # 将按钮放在顶部，并设置垂直间距为30像素

    def show_fault_tree(self):
        try:
            filePath = "ex3/test.json"
            TreeCreator = ft.TreeCreator()
            Tree = TreeCreator.jsonToTree(filePath)
            self.draw_tree(Tree)
        except Exception as e:
            messagebox.showerror("错误", f"显示故障树时发生错误: {str(e)}")

    def calculate_importance(self):
        try:
            filePath = "ex3/test.json"
            TreeCreator = ft.TreeCreator()
            Tree = TreeCreator.jsonToTree(filePath)
            cutSet = ft.getCutSet(Tree)
            cutSet = ft.getMinCutSet(cutSet)
            # 获取各组件的lambda参数
            #lambda_params = self.get_lambda_params(Tree)
            # 检查 calProb0 函数的调用，确保只传递两个参数
            Prob = ft.calProb(cutSet, Tree)
            newcutSet, H, x = ft.Structural_importance(Tree, cutSet)
            t = 100
            # 调用 Probabilistic_importance 函数时，只传递三个参数
            probImportance, probImportanceNode = ft.Probabilistic_importance(t, newcutSet, cutSet)
            # 调用 Critical_importance 函数时，也只传递三个参数
            critical_importance_list, critical_importance_node = ft.Critical_importance(t, cutSet, Tree)

            Lamda = [0.004,0.002,0.003,0.001,0.001]
            messagebox.showinfo("重要度计算结果", 
                                f"顶事件发生概率: {Prob}\n"
                                f"各组件指数分布Lamda参数: {Lamda}\n"
                                f"结构重要度节点顺序: {x}\n结构重要度: {H}\n"
                                f"概率重要度节点顺序: {probImportanceNode}\n概率重要度: {probImportance}\n"
                                f"关键重要度节点顺序: {critical_importance_node}\n关键重要度: {critical_importance_list}")
        except Exception as e:
            messagebox.showerror("错误", f"计算重要度时发生错误: {str(e)}")

    def get_lambda_params(self, Tree):
        """
        获取用户输入的各组件lambda参数。

        :param Tree: 故障树的结构，以列表形式表示。
        :return: 包含各组件lambda参数的字典。
        """
        lambda_params = {}
        for node in Tree:
            node_code = node[0]
            # 使用tkinter的simpledialog获取用户输入
            lambda_param = simpledialog.askfloat(f"输入组件 {node_code} 的lambda参数", f"请输入组件 {node_code} 的lambda参数:")
            if lambda_param is not None:
                lambda_params[node_code] = lambda_param
        return lambda_params

    def plot_node(self, node, x_pos, y_pos, level, ax, Tree, base_spacing=0.5, level_factor=0.4):
        """
        绘制故障树节点及其子节点的函数。

        :param node: 当前节点的信息列表，包含节点编号、符号、子节点列表等。
        :param x_pos: 当前节点的x坐标。
        :param y_pos: 当前节点的y坐标。
        :param level: 当前节点的层级。
        :param ax: 用于绘制的matplotlib轴对象。
        :param Tree: 故障树的结构，以列表形式表示。
        :param base_spacing: 子节点之间的基本间距，默认为0.5。
        :param level_factor: 随着层级增加，子节点间距的缩放因子，默认为0.4。
        """
        node_code = node[0]  # 节点编号
        sign = node[2]  # 节点的符号（+ 或 *）
        
        # 在指定位置绘制节点文本，包括节点编号和符号，并设置文本框样式
        ax.text(x_pos, y_pos, f"{node_code}\n({sign})", ha='center', va='center', fontsize=10, bbox=dict(facecolor='skyblue', edgecolor='black'))
        
        # 如果当前节点有子节点，递归绘制子节点
        if node[6]:  # 子节点列表
            num_children = len(node[6])
            child_spacing = base_spacing * level_factor ** level  # 根据层级调整子节点间距
            child_x = x_pos - (num_children - 1) * child_spacing / 2  # 为子节点分配x坐标位置
            for i, child in enumerate(node[6]):
                # 查找子节点在故障树中的信息
                child_node = next(item for item in Tree if item[0] == child)  
                # 绘制当前节点与子节点之间的连线
                ax.plot([x_pos, child_x + i * child_spacing], [y_pos, y_pos - 1], 'k-', lw=1)  
                # 递归调用plot_node函数绘制子节点及其子节点
                self.plot_node(child_node, child_x + i * child_spacing, y_pos - 1, level + 1, ax, Tree, base_spacing, level_factor)

    def draw_tree(self, Tree):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.axis('off')
        self.plot_node(Tree[0], 0.5, 0, 0, ax, Tree)
        plt.show()  # 使用plt.show()在弹出窗口中显示图形

# 创建主窗口
root = tk.Tk()
gui = FaultTreeGUI(root)
root.mainloop()
