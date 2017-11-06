# encoding=utf-8


# 测试案例model类
class TestModel(object):

    def __init__(self, number, method, execute, design, name, params, check_value, check_type, result, response):
        '''
             测试案例model
        :param number:     案例编号
        :param method:     请求方法
        :param execute:    是否执行(TRUE执行，FALSE不执行)
        :param design:     案例设计（缺参，少参，正常传参等）
        :param name:       模块名称
        :param params:     请求参数
        :param check_value: 检查请值
        :param check_type:  检查类型（equal,contains,uncontains）
        :param result:      执行结果
        :param response:    返回数据
        '''
        self.number = number
        self.method = method
        self.execute = execute
        self.name = name
        self.design = design
        self.params = params
        self.check_value = check_value
        self.check_type = check_type
        self.result = result
        self.response = response