# encoding=utf-8
from Base.HttpRequest.baseRequest import RequestHttp
from Tool.Config.configTool import ConfigTool
from Database.test_model import TestModel
from Base.HttpRequest.result_check import CheckResult


class YmlModelTool(object):

    @classmethod
    def read_from_yml(cls, path, execute='ALL'):
        '''
           从yml中读取执行测试案例
        :param execute: 全部执行ALL  or 部分执行 TRUE
        :param path: yml测试案例路径
        :return: 案例model 列表
        '''
        data_list = ConfigTool.get_case(path)
        model_list = []
        for data in data_list:
            test_model = TestModel(number=data['number'],
                                   method=data['method'],
                                   execute=data['execute'],
                                   design=data['design'],
                                   name=data['name'],
                                   params=data['params'],
                                   check_value=YmlModelTool.change_check_value(data['check_value']),
                                   check_type=data['check_type'],
                                   result=data['result'],
                                   response=data['response'])
            if execute == 'TRUE':
                if test_model.execute == 1:
                    model_list.append(test_model)
            else:
                model_list.append(test_model)
        return model_list

    @staticmethod
    def change_check_value(check_value):
        if not check_value:
            return {}
        value_list = check_value.split(',')
        check_dict = {}
        for value in value_list:
            dict_value = value.split('=')
            check_dict[dict_value[0]] = dict_value[1]
        return check_dict

# a = 'err=hapn.ok,title=喜铺'
# dic = YmlModelTool.change_check_value(a)
# print(dic)


case = YmlModelTool.read_from_yml('/Config/case_model.yml', execute='TRUE')
model = case[0]
print(model.check_value)
#
data = RequestHttp.get(model.name, param=model.params)

CheckResult.is_exist(data, model.check_value)



