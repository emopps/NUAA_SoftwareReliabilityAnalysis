import fault_tree as ft

filePath = "ex3/test.json"
TreeCreator = ft.TreeCreator()
Tree = TreeCreator.jsonToTree(filePath)
cutSet = ft.getCutSet(Tree)
print("故障树表:", Tree)
cutSet = ft.getMinCutSet(cutSet)
print("最小割集:", cutSet)
Prob = ft.calProb(cutSet, Tree)
print("顶事件发生概率:", Prob)
newcutSet, H, x = ft.Structural_importance(Tree, cutSet)
Lamda = [0.004,0.002,0.003,0.001,0.001]
print("各组件指数分布Lamda参数:", Lamda)
print("结果重要度节点顺序:", x)
print("结构重要度:", H)
t = 100  # 表示要求的时间点
probImportance, probImportanceNode = ft.Probabilistic_importance(t, newcutSet, cutSet)
print("概率重要度节点顺序", probImportanceNode)
print("概率重要度:", probImportance)

# 新增计算关键重要度的调用
critical_importance_list, critical_importance_node = ft.Critical_importance(t, cutSet, Tree)
print("关键重要度节点顺序:", critical_importance_node)
print("关键重要度:", critical_importance_list)
