# -*- coding: utf-8 -*-
'''
Linear Regression(线性回归算法)的手工实现(无第三方库)
Author : Kabuto_hui
Date   : 2018.04.16
'''

def compute_error(w,data):
    """
    计算误差
    :param w:       求解参数
    :param data:    传入数据
    :return:        当前误差
    """
    error_count = 0
    for i in range(len(data)):
        x = data[i][:len(data[i]) - 1]  #取出x， list
        y = data[i][-1]                 #取出y

        error_count = error_count + (w_mul_x(w, x) - y)**2

    return error_count / (2 * len(data))

def mean_normlization(x):
    '''
    均值归一化：(x - s) /（max - min）,其中s是均值
    :param x: 数据序列，list
    :return: 返回处理好的数据
    '''
    mean_x = sum(x) / len(x)
    x_temp = [(i - mean_x) / (max(x) - min(x)) for i in x]
    return x_temp

def w_mul_x(w,x):
    """
    模拟矩阵运算，计算两个向量的数量积
    :param w:   w
    :param x:   x
    :return:    计算结果
    """
    sum_wx = 0
    for (i, j) in zip(w, x):
        sum_wx = sum_wx + i * j
    return sum_wx

def compute_gradient(w,data,learning_rate):
    """
    计算梯度下降
    :param w:               求解参数list
    :param data:            训练数据list[list,list]
    :param learning_rate:   学习率
    :return:                返回当前w的更新结果
    """
    w_temp = [0 for n in range(len(w))]             #w的计算结果临时存储，最后一起更新
    partial_diff = [0 for m in range(0,len(data))]  #用于存储偏微分方程城的结果

    for j in range(0,len(w)):
        for i in range(0,len(data)):
            x = data[i][:len(data[i]) - 1]
            y = data[i][-1]
            partial_diff[i] = (w_mul_x(w, x) - y) * x[j]  #计算偏微分
        w_temp[j] = w[j] - learning_rate * sum(partial_diff) / len(data)

    #同时更新w
    w = w_temp
    return w

def LinearRegression(w_initial, data, learning_rate, iterations):
    """
    线性回归算法
    :param w_initial:       求解参数
    :param data:            训练数据, list[list] --->每个训练样例占
    :param learning_rate:   学习率
    :param iterations:      迭代次数
    :return:                返回训练好的参数
    """
    w = w_initial

    for i in range(iterations):
        w = compute_gradient(w, data, learning_rate)
    return w

if __name__ == "__main__":
    # x1+x2 = y
    data = [[0.1,0.2,0.3],\
            [0.2,0.3,0.5],\
            [0.1,0.4,0.5],\
            [0.2,0.2,0.4],\
            [0.3,0.4,0.7],\
            [0.5,0.6,1.1],\
            [0.7,0.8,1.5],\
            [1.2,1.3,2.5],\
            [0.9,1.1,2.0],\
            [0.4,0.5,0.9]]

    w_initial = [0,0]
    learning_rate = 0.1
    iterations = 1000


    w = LinearRegression(w_initial, data, learning_rate, iterations)

    print(w)
