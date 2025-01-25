from collections import defaultdict, deque

# 定义迁移过程的概率
transition_probs = {
    'T1': 1.0, 'T2': 0.99, 'T3': 0.98, 'T4': 0.8, 'T5': 1.0,
    'T6': 1.0, 'T7': 0.3, 'T8': 0.98, 'T9': 0.98, 'T10': 0.2
}

# 定义组件、连接件和迁移过程的可靠度
C = {
    'C1': 1.0, 'C2': 0.99, 'C3': 0.98, 'C4': 1.0, 'C5': 0.99, 
    'C6': 0.99, 'C7': 1.0, 'C8': 0.98, 'C9': 1.0
}

L = {
    'L1': 0.99, 'L2': 1.0, 'L3': 1.0, 'L4': 0.98, 'L5': 1.0,
    'L6': 0.99, 'L7': 0.99, 'L8': 1.0, 'L9': 0.98, 'L10': 1.0
}

T = {
    'T1': 1.0, 'T2': 0.99, 'T3': 0.98, 'T4': 0.8, 'T5': 0.99,
    'T6': 1.0, 'T7': 0.98, 'T8': 0.98, 'T9': 0.99, 'T10': 1.0
}

# 定义节点位置和连接关系
pos = {
    'S': (0, 3), 'P1': (0.5, 3), 'T1': (1, 3), 'P2': (1.5, 3), 'T2': (1.5, 2), 'P3': (1.5, 1), 'T3': (4, 1),
    'P4': (5, 1.5), 'T4': (4, 2), 'P5': (3, 2.5), 'T5': (4, 3), 'P6': (5, 3), 'T6': (5, 3.5),
    'P7': (5, 4), 'T7': (4, 4), 'P8': (3, 4), 'T8': (2, 4), 'P9': (7, 3), 'T9': (6, 3.5),
    'T10': (6, 2.5), 'EN': (8, 3)
}

arcs = [
    ('S', 'P1'), ('P1', 'T1'), ('T1', 'P2'), ('P2', 'T2'), ('T2', 'P3'), 
    ('P3', 'T3'), ('T3', 'P4'), ('P4', 'T10'), ('T10', 'P9'), ('P9', 'EN'),
    ('S', 'P1'), ('P1', 'T1'), ('T1', 'P2'), ('P2', 'T2'), ('T2', 'P3'),
    ('P3', 'T3'), ('T3', 'P4'), ('P4', 'T4'), ('T4', 'P5'), ('P5', 'T5'),
    ('T5', 'P6'), ('P6', 'T6'), ('T6', 'P7'), ('P7', 'T9'), ('T9', 'P9'), ('P9', 'EN'),
    ('S', 'P1'), ('P1', 'T1'), ('T1', 'P2'), ('P2', 'T2'), ('T2', 'P3'),
    ('P3', 'T3'), ('T3', 'P4'), ('P4', 'T4'), ('T4', 'P5'), ('P5', 'T5'),
    ('T5', 'P6'), ('P6', 'T6'), ('T6', 'P7'), ('P7', 'T7'), ('T7', 'P8'),
    ('P8', 'T8'), ('T8', 'P2'), ('P2', 'T2'), ('T2', 'P3'), ('P3', 'T3'),
    ('T3', 'P4'), ('P4', 'T10'), ('T10', 'P9'), ('P9', 'EN'),
    ('S', 'P1'), ('P1', 'T1'), ('T1', 'P2'), ('P2', 'T2'), ('T2', 'P3'),
    ('P3', 'T3'), ('T3', 'P4'), ('P4', 'T4'), ('T4', 'P5'), ('P5', 'T5'),
    ('T5', 'P6'), ('P6', 'T6'), ('P6', 'P7'), ('P7', 'T9'), ('P9', 'EN')
]

# 构建邻接表
graph = defaultdict(list)
for start, end in arcs:
    graph[start].append(end)

# BFS 寻找从起点到终点的所有路径
def bfs_all_paths(graph, start, end):
    """
    使用广度优先搜索（BFS）算法找到从起始节点到目标节点的所有路径。
    
    :param graph: 图的邻接表表示。
    :param start: 起始节点。
    :param end: 目标节点。
    :return: 从起始节点到目标节点的所有路径列表。
    """
    queue = deque([[start]])  # 队列初始包含起点路径，使用deque提高性能
    all_paths = []  # 存储所有找到的路径

    while queue:
        path = queue.popleft()  # 当前路径，从队列左侧弹出
        node = path[-1]  # 当前路径的最后一个节点
        
        if node == end:
            all_paths.append(path)  # 如果到达终点，保存路径到结果列表
        else:
            for neighbor in graph[node]:
                if neighbor not in path:  # 防止环路，只考虑未访问过的邻居节点
                    new_path = list(path)  # 创建新路径，避免修改原始路径
                    new_path.append(neighbor)  # 添加邻居节点到新路径
                    queue.append(new_path)  # 将新路径加入队列右侧
    
    return all_paths  # 返回所有找到的路径

path_reliabilities = {
    'P1': 0.951,
    'P2': 0.851,
    'P3': 0.785,
    'P4': 0.703
}

path_probabilities = {
    'P1': 0.194,
    'P2': 0.760,
    'P3': 0.044,
    'P4': 0.174
}

# 定义路径结构
paths = [
    {'name': 'P1', 'transitions': ['T1', 'T2', 'T3', 'T10'], 'components': ['C1', 'C2', 'C3', 'C4', 'C9'], 'links': ['L1', 'L2', 'L3', 'L10']},
    {'name': 'P2', 'transitions': ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T9'], 'components': ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C9', 'C4', 'C5', 'C6'], 'links': ['L1', 'L2', 'L3', 'L9']},#, 'L4', 'L5', 'L6'
    {'name': 'P3', 'transitions': ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T2', 'T3', 'T10'], 'components': ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C2', 'C3', 'C4', 'C9', 'C4'], 'links': ['L1', 'L2', 'L3', 'L5', 'L6', 'L7', 'L8', 'L2', 'L3', 'L10']},#, 'L4'
    {'name': 'P4', 'transitions': ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T2', 'T3', 'T4', 'T5', 'T6', 'T9', 'T4', 'T5', 'T6', 'T9'], 'components': ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C9', 'C6'], 'links': ['L1', 'L2', 'L3', 'L4', 'L5', 'L7', 'L8', 'L2', 'L3', 'L4', 'L5', 'L6', 'L9']}#, 'L6'
]

# 计算路径的可靠度
def calculate_path_reliability(path, C, L, T):
    """
    计算路径的可靠度。

    :param path: 路径的字典，包含路径的名称、组件、连接件和迁移过程。
    :param C: 组件的可靠度字典。
    :param L: 连接件的可靠度字典。
    :param T: 迁移过程的可靠度字典。
    :return: 路径的可靠度。
    """
    reliability = 1.0  # 初始化路径可靠度为1.0
    # 计算组件的可靠度
    for component in path['components']:
        reliability *= C[component]  # 累乘组件的可靠度
    
    # 计算连接件的可靠度
    for link in path['links']:
        reliability *= L[link]  # 累乘连接件的可靠度
    
    # 计算迁移过程的可靠度
    for transition in path['transitions']:
        reliability *= T[transition]  # 累乘迁移过程的可靠度
    
    return reliability  # 返回路径的可靠度

# 计算路径的迁移概率
def calculate_path_probability(path, path_probabilities):
    """
    计算给定路径的概率。

    :param path: 路径的字典，包含路径的名称、组件、连接件和迁移过程。
    :param path_probabilities: 路径概率的字典，键为路径名称，值为路径概率。
    :return: 路径的概率，如果路径名称不在 path_probabilities 中，则返回 0。
    """
    # 从 path_probabilities 字典中获取路径的概率，如果路径名称不存在，则返回默认值 0
    return path_probabilities.get(path['name'], 0)
    
for path in paths:
    path_reliability = calculate_path_reliability(path, C, L, T)
    path_probability = calculate_path_probability(path, path_probabilities)
    
    
# 计算系统的可靠性 R_SA
def calculate_system_reliability(paths, path_reliabilities, path_probabilities):
    """
    计算系统的可靠性。

    :param paths: 路径列表，每个路径是一个字典，包含路径的名称、组件、连接件和迁移过程。
    :param path_reliabilities: 路径可靠度的字典，键为路径名称，值为路径可靠度。
    :param path_probabilities: 路径概率的字典，键为路径名称，值为路径概率。
    :return: 系统的可靠性。
    """
    weighted_reliability_sum = 0  # 初始化加权可靠度总和为0
    total_probability = 0  # 初始化总概率为0

    # 遍历所有路径，计算路径的可靠度并加权计算系统可靠性
    for path in paths:
        # 直接使用已定义的路径可靠度和迁移概率
        path_reliability = path_reliabilities[path['name']]  # 获取路径的可靠度
        path_probability = path_probabilities[path['name']]  # 获取路径的迁移概率
        print(f"路径 {path['name']} 的可靠度 = {path_reliability:.3f}, 迁移概率 = {path_probability:.3f}")  # 打印路径的可靠度和迁移概率
        
        # 计算加权可靠度的累加
        weighted_reliability_sum += path_reliability * path_probability  # 累加加权可靠度
        total_probability += path_probability  # 累加总概率

    # 计算系统的可靠性
    R_SA = weighted_reliability_sum / total_probability if total_probability != 0 else 0  # 计算系统的可靠性
    return R_SA  # 返回系统的可靠性

# 计算系统可靠性
R_SA = calculate_system_reliability(paths, path_reliabilities, path_probabilities)

# 打印系统的可靠性
print(f"系统的可靠性 R_SA = {R_SA:.4f}")
