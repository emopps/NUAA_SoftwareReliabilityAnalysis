import sympy as sp
import json
# 导入符号计算库SymPy和JSON库

class Node():
    def __init__(self):
        """
        Node类的构造函数，用于初始化节点对象。
        :return: 无返回值
        """
        self.list = []

class TreeCreator():
    def __init__(self):
        """
        TreeCreator类的构造函数，用于初始化树对象。
        :return: 无返回值
        """
        self.tree = []

    def search(self, parentNode):
        """
        在树中搜索父节点的索引。

        :param parentNode: 要搜索的父节点。
        :return: 父节点在树中的索引，如果未找到则返回None。
        """
        length = len(self.tree)
        # 获取树的长度
        for i in range(length):
            # 遍历树中的每个节点
            if self.tree[i][0] == parentNode:
                # 如果当前节点的第一个元素等于父节点
                return i
                # 返回当前节点的索引

    def addChild(self, parentNode, childNode):
        """
        将子节点添加到父节点的子节点列表中。

        :param parentNode: 父节点的值。
        :param childNode: 要添加的子节点的值。
        :return: 无返回值。
        """
        if (parentNode == -1):
            # 如果父节点的值为-1，表示没有父节点，直接返回
            return
        parentIdx = self.search(parentNode)
        # 在树中搜索父节点的索引
        self.tree[parentIdx][-1].append(childNode)
        # 将子节点添加到父节点的子节点列表中

    def jsonToTree(self, path):
        """
        从JSON文件中读取数据并构建树结构。

        :param path: JSON文件的路径。
        :return: 构建好的树结构。
        """
        with open(path, "r", encoding="utf-8") as file:
            content = json.load(file)
        for i in content:
            node = []
            node.append(i["code"])  # 节点编号
            node.append(len(i["children"]))  # 子节点数量
            node.append(i["sign"])  # 符号
            if (i["children"] == []):  # 是否是基本事件
                node.append(True)
            else:
                node.append(False)
            node.append(i["possiblity"])  # 概率
            node.append(-1)  # 原素数位置，现轮空
            node.append(i["children"])  # 插入子节点列表
            self.tree.append(node)  # 将该节点插入树中
            # print(node)
        return self.tree

class Queue():
    def __init__(self, Tree, list=[]):
        """
        Queue类的构造函数，用于初始化队列对象。

        :param Tree: 树对象。
        :param list: 初始列表，默认为空列表。
        :return: 无返回值。
        """
        self.list = list
        # 初始化队列的列表
        self.flag = False
        # 初始化标志位
        self.Tree = Tree
        # 初始化树对象

    def length(self):
        """
        返回队列的长度。

        :return: 队列的长度。
        """
        if not self.list:
            # 如果队列为空
            return 0
            # 返回0
        else:
            # 如果队列不为空
            return len(self.list)
            # 返回队列的长度

    def is_Empty(self):
        """
        检查队列是否为空。

        :return: 如果队列为空，返回True；否则返回False。
        """
        return self.list == []
    
    def push(self, value):
        """
        将元素添加到队列的末尾。

        :param value: 要添加到队列的元素。
        :return: 无返回值。
        """
        self.list.append(value)

    def pop(self):
        """
        移除并返回队列头部的元素。

        :return: 队列头部的元素。
        """
        top = self.list[0]
        # 获取队列头部的元素
        self.list.pop(0)
        # 移除队列头部的元素
        return top
    
    def top(self):
        """
        返回队列头部的元素，但不移除它。

        :return: 队列头部的元素。
        """
        return self.list[0]
    
    def queue(self):
        """
        返回队列中的所有元素。

        :return: 队列中的所有元素。
        """
        return self.list
    
    def travel(self):
        """
        打印队列中的所有元素。

        :return: 无返回值。
        """
        print(self.list)
        
    def isALLBase(self):
        """
        检查队列中的所有节点是否都是基本事件。

        :return: 如果队列中的所有节点都是基本事件，返回True；否则返回False。
        """
        self.flag = True  # 初始化标志位为True
        for node1 in self.list:  # 遍历队列中的每个节点
            if not node1 == [-1]:  # 如果节点不是[-1]（表示根节点）
                for node2 in node1:  # 遍历节点的子节点
                    if not self.Tree[node2][3]:  # 如果子节点不是基本事件
                        self.flag = False  # 将标志位设置为False
                        return self.flag  # 返回False
        return self.flag  # 如果所有节点都是基本事件，返回True
    
def getCutSet(Tree):
    """
    从故障树中获取割集的函数。

    :param Tree: 故障树的结构，以列表形式表示。
    :return: 包含所有割集的列表。
    """
    Q = Queue(Tree)
    cutSet = Queue(Tree)  # 存放割集状态
    # getCutSet函数，用于从树中获取割集

    # 设置cutSet初始状态
    if Tree[0][3]:
        return []
    else:
        if Tree[0][2] == '+':
            # 展开列表
            for item in Tree[0][6]:
                itemList = list()
                itemList.append(item)
                cutSet.push(itemList)
        else:
            # 将child直接插到cutSet中去
            cutSet.push(Tree[0][6])
    cutSet.push([-1])
    # 对cutSet进行循环判断
    while (1):
        # cutSet.travel()
        # 1.
        if cutSet.top() == [-1]:
            if (cutSet.isALLBase()):
                break
            else:
                tail = cutSet.pop()
                cutSet.push(tail)
        # 3.2.1.
        flag = True
        for item1 in cutSet.top():
            if not Tree[item1][3]:
                flag = False
                break

        if flag:
            node = cutSet.pop()
            cutSet.push(node)
            continue
        else:
            # 3
            # 首先先找到在top中第一个不是基本事件的元素
            firstNotBase = -1
            nodeSetTop = []
            for item2 in cutSet.top():
                if not Tree[item2][3]:
                    cutSet.top().remove(item2)
                    nodeSetTop = cutSet.pop()[:]
                    # 将非基本事件的节点从队列顶部移除，并记录其索引
                    firstNotBase = item2
                    break
            # 4
            if Tree[firstNotBase][2] == '+':
                for item3 in Tree[firstNotBase][6]:
                    nodeset = nodeSetTop[:]
                    nodeset.append(item3)
                    cutSet.push(nodeset)
            else:
                nodeset = nodeSetTop[:]
                for item4 in Tree[firstNotBase][6]:
                    nodeset.append(item4)
                cutSet.push(nodeset)
    # 将临时队列中的割集转换为最终结果
    cutSetAns = []
    for item in cutSet.queue():
        if item!= [-1]:
            cutSetAns.append(item)
    return cutSetAns

def flatten_list(nested_list):
    """
    将嵌套列表展平成单层列表。

    :param nested_list: 嵌套列表。
    :return: 展平后的单层列表。
    """
    return [item for sublist in nested_list for item in
            (flatten_list(sublist) if isinstance(sublist, list) else [sublist])]

# 定义一个质数列表，用于后续的最小割集计算
prime = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]

def getMinCutSet(cutSet=[]):
    """
    从割集中找到最小割集的函数。

    :param cutSet: 包含所有割集的列表，默认为空列表。
    :return: 包含所有最小割集的列表。
    """
    length = len(cutSet)  # 获取割集列表的长度
    tempSet = set(flatten_list(cutSet))  # 将割集列表展平并转换为集合，去除重复元素
    primeSet = prime[:len(tempSet)]  # 获取与tempSet长度相同的质数列表
    code2prime = dict(zip(tempSet, primeSet))  # 创建一个字典，将tempSet中的元素映射到primeSet中的质数
    prime2code = dict(zip(primeSet, tempSet))  # 创建一个字典，将primeSet中的质数映射到tempSet中的元素

    mulSet = []  # 用于存储每个割集的乘积
    flagSet = []  # 用于标记每个割集是否为最小割集
    for cut in cutSet:  # 遍历每个割集
        mul = 1  # 初始化乘积为1
        for i in cut:  # 遍历割集中的每个元素
            mul *= code2prime[i]  # 计算乘积
        mulSet.append(mul)  # 将乘积添加到mulSet列表中
        flagSet.append(True)  # 初始时，将每个割集标记为最小割集

    for i in range(length):  # 遍历每个割集
        for j in range(length):  # 遍历每个割集
            if i == j:  # 如果是同一个割集，跳过
                continue
            if mulSet[i] % mulSet[j] == 0:  # 如果一个割集的乘积能被另一个割集的乘积整除
                flagSet[i] = False  # 则将该割集标记为非最小割集

    ans = []  # 用于存储最小割集
    for i in range(length):  # 遍历每个割集
        if flagSet[i]:  # 如果该割集是最小割集
            ans.append(cutSet[i])  # 将其添加到ans列表中
    return ans

def calProb(minCutSet, Tree):
    """
    计算最小割集的概率。

    :param minCutSet: 最小割集的列表。
    :param Tree: 故障树的结构，以列表形式表示。
    :return: 最小割集的概率。
    """
    Prob = 0  # 初始化概率为0
    sum = 1  # 初始化总和为1
    for item in minCutSet:  # 遍历最小割集中的每个割集
        prob1 = 1  # 初始化割集的概率为1
        for item2 in item:  # 遍历割集中的每个元素
            prob1 = Tree[item2][4] * prob1  # 计算割集的概率
        sum = (1 - prob1) * sum  # 计算总和
    Prob = 1 - sum  # 计算最小割集的概率
    return Prob

H = []

# 存储所有基本事件的结构重要度
def Structural_importance(Tree, cutSet):
    """
    计算结构重要度的函数。

    :param Tree: 故障树的结构，以列表形式表示。
    :param cutSet: 包含所有割集的列表。
    :return: 包含所有最小割集的列表、基本事件的结构重要度列表和基本事件列表。
    """
    x = []  # 存储基本事件的索引
    # 计算基本事件个数
    for i in Tree:  # 遍历故障树的每个节点
        if (i[3] == True):  # 如果节点是基本事件
            if not i[0] in x:  # 如果基本事件的索引不在x列表中
                x.append(i[0])  # 将基本事件的索引添加到x列表中
                H.append(0)  # 将基本事件的结构重要度初始化为0
    clear_cutSet = []  # 存储清理后的割集
    for i in cutSet:  # 遍历每个割集
        temp = []  # 临时存储清理后的割集
        for j in i:  # 遍历割集中的每个元素
            temp.append(x.index(j))  # 将基本事件的索引转换为x列表中的索引
        clear_cutSet.append(temp)  # 将清理后的割集添加到clear_cutSet列表中

    generate_permutations(len(x), clear_cutSet)  # 生成所有可能的排列
    return clear_cutSet, H, x  # 返回清理后的割集、基本事件的结构重要度列表和基本事件列表

# 定义一个函数，用递归的方式生成所有可能的排列
def generate_permutations(base_events, cutSet, result=[]):
    """
    生成所有可能的排列。

    :param base_events: 基本事件的数量。
    :param cutSet: 割集列表。
    :param result: 当前生成的排列，默认为空列表。
    :return: 无返回值。
    """
    # 如果当前列表的长度等于base_events，说明已经生成了一个排列，将其添加到结果列表中
    if len(result) == base_events:
        calculate_structuralImportance(cutSet, result)
        return
    else:
        for i in [0, 1]:
            result.append(i)
            generate_permutations(base_events, cutSet, result)
            result.pop()  # 回溯，删除最后一个元素
    return

def calculate_structuralImportance(cutSet, event_count):
    """
    计算结构重要度的具体值。

    :param cutSet: 割集列表。
    :param event_count: 事件计数列表。
    :return: 无返回值。
    """
    # 检查所有数组中为1的元素，与最小割集的集合进行判断，如果元素在某个某个中，检测这个割集的其他元素，如果都为1，说明该事件发生，Pxi1=1,
    # 如果元素不在某个割集中，则判断该割集的元素，如果都为1，说明当这个元素为0时，顶事件也发生，Pxi1=Pxi0=1,结果为(Pxi1-Pxi0)/pow(2, len(event_count)-1)
    for i in range(len(event_count)):  # 遍历事件计数列表
        if (event_count[i] == 0):  # 如果事件计数为0，跳过该事件
            continue
        Pxi1 = 0  # 初始化Pxi1为0
        Pxi0 = 0  # 初始化Pxi0为0
        for cutSet_cell in cutSet:  # 遍历割集列表
            if i in cutSet_cell:  # 如果事件i在割集中
                isTop = True  # 初始化isTop为True
                for j in cutSet_cell:  # 遍历割集中的元素
                    if event_count[j] == 0:  # 如果割集中的元素计数为0
                        isTop = False  # 将isTop设置为False
                        break
                if isTop:  # 如果isTop为True，说明该事件发生
                    Pxi1 = 1  # 将Pxi1设置为1
            else:  # 如果事件i不在割集中
                isTop = True  # 初始化isTop为True
                for j in cutSet_cell:  # 遍历割集中的元素
                    if event_count[j] == 0:  # 如果割集中的元素计数为0
                        isTop = False  # 将isTop设置为False
                        break
                if isTop:  # 如果isTop为True，说明当该事件为0时，顶事件也发生
                    # 当一个最小割集中不包含xi也导致顶事件发生则Pxi1和Pxi0都为1
                    Pxi1 = 1  # 将Pxi1设置为1
                    Pxi0 = 1  # 将Pxi0设置为1
        H[i] += (Pxi1 - Pxi0) / pow(2, len(event_count) - 1)  # 计算结构重要度并累加到H列表中

def Probabilistic_importance(t, cutSet, oldcutSet):
    """
    计算概率重要度的函数。

    :param t: 时间点。
    :param cutSet: 最小割集。
    :param oldcutSet: 旧的割集。
    :return: 概率重要性列表以及对应的节点顺序。
    """
    proImportanceNode = []  # 存储概率重要性节点的列表
    # 遍历旧的割集，找到所有不重复的节点并添加到proImportanceNode列表中
    for i in range(len(oldcutSet)):
        for j in range(len(oldcutSet[i])):
            if not oldcutSet[i][j] in proImportanceNode:
                proImportanceNode.append(oldcutSet[i][j])
    parameter = []  # 存储参数的列表
    # 记录最小割集中互不相同的元素个数，方便为后面的Lamda输入
    exp = "1-"  # 初始化表达式字符串
    # 遍历最小割集，构建表达式字符串
    for i in range(len(cutSet)):
        if (i == 0):
            exp += "("
        else:
            exp += "*("
        for j in range(len(cutSet[i])):
            if j == 0:
                exp += "1-"
            else:
                exp += "*"
            temp = chr(ord('a') + cutSet[i][j])  # 将节点索引转换为字符
            exp += temp  # 将字符添加到表达式字符串中
            if not temp in parameter:
                parameter.append(temp)  # 将字符添加到参数列表中
        exp += ")"
    # 读取指数分布的Lamda参数
    #print('请输入各组件指数分布Lamda参数：')
    Lama = []  # 存储Lamda参数的列表
    Lama = [0.004,0.002,0.003,0.001,0.001]
    # 遍历参数列表，读取用户输入的Lamda参数
    # for i in range(len(parameter)):
    #     temp = input()
    #     Lama.append(float(temp))
    f = []  # 存储符号变量的列表
    # 遍历参数列表，创建符号变量并添加到f列表中
    for i in range(len(parameter)):
        temp = sp.symbols(parameter[i])
        f.append(temp)
    func = sp.sympify(exp)  # 将表达式字符串转换为sympy表达式
    result = []  # 存储结果的列表
    # 遍历Lamda参数列表，计算概率重要性并添加到result列表中
    for i in range(len(Lama)):
        temp = sp.diff(func, f[i])  # 对表达式求导
        # 遍历Lamda参数列表，将符号变量替换为具体数值
        for j in range(len(Lama)):
            temp = temp.subs(f[j], 1 - sp.exp(-Lama[j] * t))  # 带入Fj(t)=1-e^(-Lamda[j]*t)
        result.append(temp.evalf())  # 计算表达式的值并添加到result列表中
    return result, proImportanceNode  # 返回结果列表和概率重要性节点列表

def Critical_importance(t, cutSet, Tree):
    """
    计算关键重要度的函数
    :param t: 时间点
    :param cutSet: 最小割集
    :param Tree: 故障树结构
    :return: 关键重要度列表以及对应的节点顺序
    """
    # 先计算顶事件发生概率F_s(t)
    F_s = calProb(cutSet, Tree)
    proImportanceNode = []
    for cut in cutSet:
        for node in cut:
            if node not in proImportanceNode:
                proImportanceNode.append(node)
    # 计算每个基本事件的Fi(t)和Δgi(t)并进而计算关键重要度
    critical_importance_list = []
    for node in proImportanceNode:
        # 模拟该基本事件发生，计算此时顶事件发生概率作为Fi(t)
        temp_cutSet = []
        for cut in cutSet:
            if node in cut:
                temp_cut = cut.copy()
                temp_cut.remove(node)
                if temp_cut:
                    temp_cutSet.append(temp_cut)
                else:
                    continue
            else:
                temp_cutSet.append(cut)
        # 计算此时顶事件发生概率作为Fi(t)
        F_i = calProb(temp_cutSet, Tree)
        # 计算Δgi(t)，这里简单示例为概率变化率（实际可能需要更精确的定义和计算方式，根据具体情况调整）
        delta_g_i = (F_i - F_s) / F_s if F_s!= 0 else 0
        # 计算关键重要度
        critical_importance = (F_i / F_s) * delta_g_i if F_s!= 0 else 0
        # 将关键重要度添加到critical_importance_list列表中
        critical_importance_list.append(critical_importance)
    # 返回关键重要度列表以及对应的节点顺序
    return critical_importance_list, proImportanceNode