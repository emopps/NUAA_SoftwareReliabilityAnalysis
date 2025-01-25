import fault_tree as ft
import networkx as nx
import matplotlib.pyplot as plt

filePath = "ex3/test.json"
TreeCreator = ft.TreeCreator()
Tree = TreeCreator.jsonToTree(filePath)

def plot_node(node, x_pos, y_pos, level, ax, base_spacing=0.5, level_factor=0.4):
    """
    绘制故障树节点及其子节点的函数。

    :param node: 当前节点的信息列表，包含节点编号、符号、子节点列表等。
    :param x_pos: 当前节点的x坐标。
    :param y_pos: 当前节点的y坐标。
    :param level: 当前节点的层级。
    :param ax: 用于绘制的matplotlib轴对象。
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
            plot_node(child_node, child_x + i * child_spacing, y_pos - 1, level + 1, ax, base_spacing, level_factor)

def draw_tree(Tree):
    """
    绘制故障树的函数。

    :param Tree: 故障树的结构，以列表形式表示。
    """
    # 创建一个新的图形和轴对象，设置图形大小为10x6英寸
    fig, ax = plt.subplots(figsize=(10, 6))
    # 关闭轴显示，只显示绘制的图形内容
    ax.axis('off')  
    # 从根节点开始绘制故障树，根节点位于(0.5, 0)位置，层级为0
    plot_node(Tree[0], 0.5, 0, 0, ax)  
    # 显示绘制的故障树图形
    plt.show()

draw_tree(Tree)
