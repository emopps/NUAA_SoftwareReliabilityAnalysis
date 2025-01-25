import matplotlib.pyplot as plt
import networkx as nx

# 创建有向图
G = nx.DiGraph()

# 添加位置和变迁
places = ['S', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'EN']
transitions = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10']
G.add_nodes_from(places, node_type='place')
G.add_nodes_from(transitions, node_type='transition')

# 添加弧（路径）
# PW1: S->P1->T1->P2->T2->P3->T3->P4->T10->P9->EN
# PW2: S->P1->T1->P2->T2->P3->T3->P4->T4->P5->T5->P6->T6->P7->T9->P9->EN
# PW3: S->P1->T1->P2->T2->P3->T3->P4->T4->P5->T5->P6->T6->P7->T7->P8->T8->P2->T2->P3->T3->P4->T10->P9->EN
# PW4: S->P1->T1->P2->T2->P3->T3->P4->T4->P5->T5->P6->T6->P7->T7->P8->T8->P2->T2->P3->T3->P4->T4->P5->T5->P6->T6->P7->T9->P9->ENa
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
G.add_edges_from(arcs)

pos = {
    'S': (0, 3), 'P1': (0.5, 3), 'T1': (1, 3), 'P2': (1.5, 3), 'T2': (1.5, 2), 'P3': (1.5, 1), 'T3': (4, 1),
    'P4': (5, 1.5), 'T4': (4, 2), 'P5': (3, 2.5), 'T5': (4, 3), 'P6': (5, 3), 'T6': (5, 3.5),
    'P7': (5, 4), 'T7': (4, 4), 'P8': (3, 4), 'T8': (2, 4), 'P9': (7, 3), 'T9': (6, 3.5),
    'T10': (6, 2.5), 'EN': (8, 3)
}

# 绘制图形
plt.figure(figsize=(10, 6))
nx.draw_networkx_nodes(G, pos, nodelist=places, node_color='lightblue', node_size=500, node_shape='o')
nx.draw_networkx_nodes(G, pos, nodelist=transitions, node_color='lightgrey', node_size=500, node_shape='s')

# 绘制边
nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=20)

# 绘制标签
nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')

# 显示图形
plt.axis('off')
plt.show()
