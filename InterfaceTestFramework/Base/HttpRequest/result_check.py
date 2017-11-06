# encoding=utf-8
from Base.HttpRequest.baseRequest import RequestHttp
from Tool.Logger.logTool import LogTool


class CheckResult(object):

    @classmethod
    def is_exist(cls, json_data, except_data):
        '''
           检查返回数据是否包含所期望的值
        :param json_data:   返回的response对象
        :param except_data: 期望得到的值(字典形式，当所有键值对均被json包含才会返回True)
        :return:            返回布尔值True or False
        '''
        LogTool.info('Check {except_data} is_exist {json_data} '.format(except_data=except_data, json_data=json_data))

        result = 0
        for key, value in except_data.items():
            item = "'{key}': '{value}'".format(key=key, value=value)
            LogTool.debug('Check {item} whether or not exist'.format(item=item))
            if str(item) in str(json_data.json()):
                LogTool.info('Value: {item} is exist in json data'.format(item=item))
                result += 1
            else:
                LogTool.error('Value： {item} is not Exist !!'.format(item=item))
        if result == len(except_data):
            LogTool.info('All inspections passed in this TestCase')
            return True
        else:
            LogTool.error("This test case didn't go through'")
            return False


# params={
# "city_id" : "110900",
# "access_token" : "",
# "client_guid" : 3232235777,
# "client_timestamp" : 1509415724,
# "app_id" : 10011,
# "client_version" : "1.0.1",
# "app_usign" : "avdjMd3Lx930nKrZTSeQE/caSSw=",
# }
# data = RequestHttp.get('/common/channel/hunlifuwu/index', param=params)
# except_data = {'err': 'hapn.ok', 'title': '喜铺'}
# print(CheckResult.is_exist(data, except_data))

