# encoding=utf-8
from Tool.Config.configTool import ConfigTool
import json
# 读写2007 excel xlsx结尾
import openpyxl
EXCEL_PATH = ConfigTool.get('ExcelDataDriven', 'Filepath')


class ExcelTool(object):

    @classmethod
    def read_excel(cls):
        wb = openpyxl.load_workbook(EXCEL_PATH)
        sheet = wb.get_sheet_by_name('test')

        for m, row in enumerate(sheet.rows):
            # 去除表头
            if m > 0:
                for index, cell in enumerate(row):
                    pass


# 测试案例model类
class TestModel(object):

    def __init__(self, number, name, method, params, expect_result, actual_result, response, test_result):
        '''
           测试案例model
        :param number:         测试编号
        :param name:           接口模块名
        :param method:         请求方法 GET POST
        :param params:         请求参数
        :param expect_result:  期望结果
        :param actual_result:
        :param response:
        :param test_result:
        '''
        self.number = number
        self.name = name
        self.method = method
        self.params = params
        self.expect_result = expect_result
        self.actual_result = actual_result
        self.response = response
        self.test_result = test_result





