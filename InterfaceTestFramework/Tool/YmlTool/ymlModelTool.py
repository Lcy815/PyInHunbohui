# encoding=utf-8
from Tool.Config.configTool import ConfigTool
from Database.test_model import TestModel


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
                                   check_value=data['check_value'],
                                   check_type=data['check_type'],
                                   result=data['result'],
                                   response=data['response'])
            if execute == 'TRUE':
                if test_model.execute == 1:
                    model_list.append(test_model)
            else:
                model_list.append(test_model)
        return model_list


print(YmlModelTool.read_from_yml('/Config/case_model.yml'))

