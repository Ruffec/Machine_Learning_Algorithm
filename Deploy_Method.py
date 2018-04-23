# -*- coding: utf-8 -*-
import random
import math

class Server(object):
    '''
    用于模拟退火的工具类，后面的01背包可以独立拿出来运行
    '''
    def __init__(self, cpu, mem):
        self.free_cpu = cpu
        self.total_cpu = cpu
        self.free_mem = mem
        self.total_mem = mem
        self.flavors = []

    def __str__(self):
        return str(self.flavors)

    def put_flavor(self, flavor):
        if self.free_cpu >= flavor[1] and self.free_mem >= flavor[2]:
            self.free_cpu -= flavor[1]
            self.free_mem -= flavor[2]
            self.flavors.append(flavor[0])
            return True
        return False

    def get_cpu_usage_rate(self):
        return float(1 - self.free_cpu / self.total_cpu)

    def get_mem_usage_rate(self):
        return float(1 - self.free_mem / self.total_mem)

# ---------------------Simulated Anneal--------------------------
def deploy_flavor_use_sa(count, flavors, phy_server, cpu_if):
    """
    模拟退火进行装包
    :param count:        int 输入的虚拟机总数
    :param flavors:      list[list,list...] 将每种虚拟机的型号参数数目写出来,如[[10, 8, 8], [10, 8, 8], [10, 8, 8], [7, 4, 4], [7, 4, 4], [7, 4, 4], [7, 4, 4], [7, 4, 4], [7, 4, 4]]
    :param phy_server:   list[] 物理虚拟机的参数,如[56, 128, 1200]
    :param cpu_if:       int 优化参数，1：CPOU， 0：MEM
    :return:             list[list, list...] 每台物理服务器的装包方式
    """
    min_score = len(flavors) + 1
    best_result = []
    T = 100
    Tmin = 1
    r = 0.9999
    dice = [i for i in range(count)]
    # print dice
    while T > Tmin:
        temp = random.sample(dice, 2)
        flavors[temp[0]], flavors[temp[1]] = flavors[temp[1]], flavors[temp[0]]

        servers = []
        firstserver = Server(phy_server[0], phy_server[1])
        servers.append(firstserver)

        for i in range(len(flavors)):
            for j in range(len(servers)):
                if servers[j].put_flavor(flavors[i]):
                    break
                if j == len(servers) - 1:
                    newserver = Server(phy_server[0], phy_server[1])
                    newserver.put_flavor(flavors[i])
                    servers.append(newserver)

        if cpu_if == 1:
            server_score = len(servers) - 1 + servers[-1].get_cpu_usage_rate()
        else:
            server_score = len(servers) - 1 + servers[-1].get_mem_usage_rate()
        if server_score < min_score:
            min_score = server_score
            best_result = servers
        else:
            if math.exp(min_score - server_score) / T > random.random():
                min_score = server_score
                best_result = servers
        T = r * T
    final_result = []
    for i in range(len(best_result)):
        # charArray.append(array.array('B', best_result[i].flavors))
        final_result.append(best_result[i].flavors)
    return final_result

# ---------------------01背包问题--------------------------------
def deploy_flavor_use_01bag(count_all, predict, server_CPU, server_MEM, target):
    """
    01背包算法装包
    :param count_all:   int 输入的虚拟机总数
    :param predict:     list[list,list...] 将每种虚拟机的型号参数数目写出来,如[[10, 8, 8], [10, 8, 8], [10, 8, 8], [7, 4, 4], [7, 4, 4], [7, 4, 4], [7, 4, 4], [7, 4, 4], [7, 4, 4]]
    :param server_CPU:  int 物理服务器的CPU大小
    :param server_MEM:  int 物理服务器的Memory的大小
    :param target:      int 优化类型 1：CPU， 0：MEM
    :return:            list[list, list...] 每台物理服务器的装包方式    int 每台服务器最大装包结果
    """
    if target:
        server = server_MEM
        limit_factor = server_CPU
        capacity = 2 #every MEM
        weight = 1 #every CPU
    else:
        server = server_CPU
        limit_factor = server_MEM
        capacity = 1 #every CPU
        weight = 2 #every MEM
    bag = [[0 for col in range(server + 1)] for raw in range(count_all + 1)]
    result = []
    # 计算背包问题
    for i in range(1, count_all + 1):
        for j in range(1, server + 1):
            bag[i][j] = bag[i - 1][j]
            if j >= predict[i - 1][capacity]:
                bag[i][j] = max(bag[i][j], bag[i - 1][j - predict[i - 1][capacity]] + predict[i - 1][weight])
            if bag[i][j] > limit_factor:
                n = j - 1
                for m in range(i, 0, -1):
                    if bag[m][n] > bag[m - 1][n]:
                        result.append(predict[m - 1][0])
                        n = n - predict[m - 1][capacity]
                return result, bag[i][j - 1]

    # 递推出装入背包的物体
    big = bag[i][j]
    j = server
    for i in range(count_all, 0, -1):
        if bag[i][j] > bag[i - 1][j]:
            result.append(predict[i - 1][0])
            j = j - predict[i - 1][capacity]

    return result, big

