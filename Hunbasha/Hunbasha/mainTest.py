# encoding=utf-8
from Tool.Config.configTool import ConfigTool
# from Tool.Email.emailTool import MailTool
from Hunbasha.indexTest import HunIndex
from Tool.Log.logTool import LogTool
import time


class MainTest:

    def __init__(self):
        self.error_list = []
        self.sum_execute = 0
        self.result = None

    def get_checkurl(self):
        return ConfigTool.get('Hunbasha', 'check_items')

    def save_log(self):
        save_path = ConfigTool.get('Log', 'Save_path')
        path = ConfigTool.get('Log', 'Path')

        src = open(path, 'r')
        current_time = str(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()))
        dst = open('%s%s_test.txt' % (save_path, current_time), 'w')

        dst.write(src.read())

        src.close()
        dst.close()

    def check_result(self, case):
        # for error in case.error_list:
        #     if 'jiehun' in error:


        result = ' %s \n execute_time:%d s \n 遍历页面：%s \n 遍历url:%s \n 错误url: %s \n' % (case.describe, case.execute_time, case.url, str(len(case.items)), case.error_list)
        return result



    def execute_test(self):
        url_items = self.get_checkurl()
        for item in url_items:
            url = item['url']
            describe = item['describe']
            LogTool.info('begin check page title:{title}, url:{url}'.format(title=describe, url=url))
            case = HunIndex(url)
            case.run()
            LogTool.info('------------------------------------------------------------------------')
            # print('%s execute time:%d s' % (describe, int(case.stop_time-case.start_time)))
            case.execute_time = int(case.stop_time-case.start_time)
            case.describe = describe
            self.error_list.extend(case.error_list)
            self.sum_execute += len(case.items)

            print(self.check_result(case))

if __name__ == '__main__':
    a = MainTest()
    # 执行测试
    a.execute_test()
    # a.save_log()



