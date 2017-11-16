# encoding=utf-8
from Tool.Config.configTool import ConfigTool
# from Tool.Email.emailTool import MailTool
from Hunbasha.indexTest import HunIndex
from Tool.Log.logTool import LogTool
from Tool.hrefTool import HrefTest
import time


class MainTest:

    def __init__(self):
        self.error_list = []
        self.sum_execute = 0
        self.result = None
        self.result_list = []
        self.execute_time = 0

    @staticmethod
    def get_checkurl():
        return ConfigTool.get('Hunbasha', 'check_items')

    @staticmethod
    def save_log():
        save_path = ConfigTool.get('Log', 'Save_path')
        path = ConfigTool.get('Log', 'Path')

        src = open(path, 'r')
        current_time = str(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()))
        dst = open('%s%s_test.txt' % (save_path, current_time), 'w')

        dst.write(src.read())

        src.close()
        dst.close()

    def check_result(self, case):
        print('error', case.error_list)
        self.result_list.clear()
        for error in case.error_list:
            if 'jiehun' in str(error):
                self.result_list.append(error)
        self.result = ' %s \n execute_time:%d s \n 遍历页面：%s \n 遍历url:%s \n 错误url: %s \n' % (case.describe,
                                                                                      case.execute_time, case.url,
                                                                                      str(len(case.execute_items)),
                                                                                      self.result_list)
        return self.result

    def execute_test(self):
        url_items = self.get_checkurl()
        print(url_items)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
        }
        index_url = 'https://bj.jiehun.com.cn'
        index_items = HrefTest.get_hostsit_href(index_url, headers)
        for item in url_items:
            url = item['url']
            describe = item['describe']
            LogTool.info('begin check page title:{title}, url:{url}'.format(title=describe, url=url))
            case = HunIndex(url, item['is_checkIndex'], index_items)
            case.run()
            LogTool.info('------------------------------------- -----------------------------------')
            # print('%s execute time:%d s' % (describe, int(case.stop_time-case.start_time)))
            case.execute_time = int(case.stop_time-case.start_time)
            case.describe = describe
            self.error_list.extend(case.error_list)
            self.sum_execute += len(case.items)
            self.execute_time += case.execute_time
            print(self.check_result(case))

if __name__ == '__main__':
    a = MainTest()
    # 执行测试
    a.execute_test()
    print('总执行时间：%d' % a.execute_time)
    # a.save_log()

10.38

