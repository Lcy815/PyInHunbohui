# encoding=utf-8
from Tool.Config.configTool import ConfigTool
import json
# 读写2007 excel xlsx结尾
import openpyxl
EXCEL_PATH = ConfigTool.get('ExcelDataDriven', 'Filepath')


# 测试案例model类
class TestModel(object):

    def __init__(self, number, method, design, name, params, check_value, result, response):
        self.number = number
        self.method = method
        self.name = name
        self.design = design
        self.params = params
        self.check_value = check_value
        self.result = result
        self.response = response


class ExcelTool(object):

    @classmethod
    def read_all_excel(cls, sheet_name):
        wb = openpyxl.load_workbook(EXCEL_PATH)
        sheet = wb.get_sheet_by_name(sheet_name)

        value_list = []
        model_list = []
        for m, row in enumerate(sheet.rows):
            # 去除表头
            if m > 0:
                for cell in row:
                    model_list.append(cell.value)
                case_model = TestModel(model_list[0], model_list[1], model_list[2], model_list[3], model_list[4],
                                       model_list[5], model_list[6], model_list[7])
                value_list.append(case_model)
                model_list = []
        return value_list

    @classmethod
    def write_excel(cls):
        pass
# print(ExcelTool.read_all_excel('test'))
for case in ExcelTool.read_all_excel('test'):
    print(case.name)







