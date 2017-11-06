# encoding=utf-8
from Tool.Config.configTool import ConfigTool
import json
from Base.HttpRequest.baseRequest import RequestHttp
from Database.test_model import TestModel

# 读写2007 excel xlsx结尾
import openpyxl
# 读写2003 excel  xls结尾

EXCEL_PATH = ConfigTool.get('ExcelDataDriven', 'Filepath')
TEST_SHEET = ConfigTool.get('ExcelDataDriven', 'TestSheet')


class ExcelTool(object):

    @classmethod
    def read_excel(cls, execute='ALL'):
        '''
           获取表格内案例model
        :param sheet_name:  表名
        :param execute : 执行方式（默认全部获取执行测试，如果传递‘TRUE’,则之执行为TURE的案例）
        :return:  返回 案例列表
        '''
        wb = openpyxl.load_workbook(EXCEL_PATH)
        sheet = wb.get_sheet_by_name(TEST_SHEET)

        value_list = []
        model_list = []
        for m, row in enumerate(sheet.rows):
            # 去除表头
            if m > 0:
                for cell in row:
                    model_list.append(cell.value)
                # 创建案例model
                case_model = TestModel(model_list[0], model_list[1], model_list[2], model_list[3], model_list[4],
                                       model_list[5], model_list[6], model_list[7], model_list[8], model_list[9])
                print(case_model.execute)
                # 如果部分执行
                if execute == 'TRUE':
                    if case_model.execute == 1:
                        value_list.append(case_model)
                else:
                    value_list.append(case_model)
                model_list = []
        return value_list

    @classmethod
    def write_excel(cls):
        pass





# print(ExcelTool.read_all_excel('test'))
for case in ExcelTool.read_excel(execute='TRUE'):
    if case.method == 'GET':
        print(RequestHttp.get(case.name, param=case.params))









