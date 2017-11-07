# encoding=utf-8
from Tool.Config.configTool import ConfigTool
import json
from Base.HttpRequest.baseRequest import RequestHttp
from Database.test_model import TestModel

# 读写2007 excel xlsx结尾
import openpyxl
# 读写2003 excel  xls结尾


class ExcelTool(object):

    @classmethod
    def read_excel(cls, path, sheet_list, execute='ALL'):
        '''
           获取表格内案例model
        :param path: 表格路径
        :param sheet_list:  需要获取的表名（可能是一个表，也可能是多个）
        :param execute : 执行方式（默认全部获取执行测试，如果传递‘TRUE’,则之执行为TURE的案例）
        :return:  返回 案例列表
        '''
        wb = openpyxl.load_workbook(path)
        sum_model = []

        for sheet_name in sheet_list:
            sheet = wb.get_sheet_by_name(sheet_name)

            value_list = []
            model_list = []
            for m, row in enumerate(sheet.rows):
                # 去除表头
                if m > 0:
                    for cell in row:
                        model_list.append(cell.value)
                    # 创建案例model
                    case_model = TestModel(model_list[0], model_list[1], model_list[2], model_list[3], model_list[4],
                                           model_list[5], ExcelTool.change_check_value(model_list[6]), model_list[7],
                                           model_list[8], model_list[9])
                    # 如果部分执行
                    if execute == 'TRUE':
                        if case_model.execute == 1:
                            value_list.append(case_model)
                    else:
                        value_list.append(case_model)
                    model_list = []
            sum_model.extend(value_list)
        return sum_model

    @classmethod
    def write_excel(cls):
        pass

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










