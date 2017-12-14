# encoding=utf-8
# from Tool.Config.configTool import ConfigTool
# # from Tool.Email.emailTool import MailTool
# from Hunbasha.indexTest import HunIndex
# from Tool.Log.logTool import LogTool
# from Tool.hrefTool import HrefTest

import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import Tool.hrefTool
import Tool.Log.logTool
import Tool.Config.configTool
import Hunbasha.indexTest
import time
import Tool.Email.emailTool
import Tool.FileTool.fileTool


class MainTest:

    def __init__(self):
        '''
        @:param error_list   错误列表
        @:param sum_execute  实际总的执行检测url数
        @:param resut        最终结果
        @:param result_list  每个频道页检测结果
        @:param execute_time 执行时间
        '''
        self.error_list = []
        self.sum_execute = 0
        self.result = None
        self.result_list = []
        self.execute_time = 0
        self.update = True

    @staticmethod
    def get_checkurl():
        return Tool.Config.configTool.ConfigTool.get('Hunbasha', 'check_items')

    @staticmethod
    def save_log():
        '''
            保存日志文件
        :return:  None
        '''
        save_path = Tool.Config.configTool.ConfigTool.get('Log', 'Save_path')
        path = Tool.Config.configTool.ConfigTool.get('Log', 'Path')

        src = open(path, 'r')
        current_time = str(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()))
        dst = open('%s%s_test.txt' % (save_path, current_time), 'w')

        dst.write(src.read())

        src.close()
        dst.close()

    def save_error(self):
        '''
           保存错误信息，与上次的错误信息校对，如果相同则不保存，如果有变动，则保存新的错误信息
        :return:
        '''
        error_path = Tool.Config.configTool.ConfigTool.get('Error_file', 'Path')
        if Tool.FileTool.fileTool.FileTool.is_exists(error_path):
            text = Tool.FileTool.fileTool.FileTool.read_file(error_path)
            # 如果错误文档为空并且错误链接列表为空，不需要更新错误信息
            if not text and len(self.error_list) == 0:
                self.update = False
                return
            # 如果最新错误列表为空，不需要更新错误信息
            elif len(self.error_list) == 0:
                self.update = False
                return
            # 如果最新错误列表不为空，错误文本为空，则更新文本
            elif not text and len(self.error_list) > 0:
                Tool.FileTool.fileTool.FileTool.write_cover_file(error_path, str(self.error_list))
                return
            # 如果都不为空，判断最新错误与错误文档是否有不同，如有不同，则更新文本
            for error in self.error_list:
                if error[0] not in text:
                    Tool.FileTool.fileTool.FileTool.write_cover_file(error_path, str(self.error_list))
                    return
            self.update = False
        else:
            Tool.FileTool.fileTool.FileTool.write_cover_file(error_path, str(self.error_list))

    def check_result(self, case):
        '''
           筛选结果，只筛选jiehun相关
        :param case:  执行case
        :return:      None
        '''
        print('error', case.error_list)
        self.result_list.clear()
        for error in case.error_list:
            if 'jiehun' in str(error):
                self.result_list.append(error)
        self.result = ' %s \n execute_time:%d s \n 遍历页面：%s \n 遍历url:%s \n 错误url: %s \n' % (case.describe,
                                                                                      case.execute_time, case.url,
                                                                                      str(case.sum_url),
                                                                                      self.result_list)
        return self.result

    def execute_test(self, index_items):
        '''
           执行测试
        :param index_items:   首页url items
        :return:  None
        '''
        url_items = self.get_checkurl()
        print(url_items)

        for item in url_items:
            url = item['url']
            describe = item['describe']
            Tool.Log.logTool.LogTool.info('begin check page title:{title}, url:{url}'.format(title=describe, url=url))
            case = Hunbasha.indexTest.HunIndex(url, item['is_checkIndex'], index_items)
            case.run()
            Tool.Log.logTool.LogTool.info('------------------------------------- -----------------------------------')
            # print('%s execute time:%d s' % (describe, int(case.stop_time-case.start_time)))
            case.execute_time = int(case.stop_time-case.start_time)
            case.describe = describe
            if case.error_list:
                self.error_list.extend(case.error_list)
            if case.items:
                self.sum_execute += len(case.items)
            self.execute_time += case.execute_time
            print(self.check_result(case))

if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
    }
    index_url = 'https://bj.jiehun.com.cn'
    index_items = Tool.hrefTool.HrefTest.get_hostsit_href(index_url, headers)
    a = MainTest()
    # 执行测试
    a.execute_test(index_items)
    print('总执行时间：%d' % a.execute_time)
    # a.save_log()
    a.save_error()
    print(a.update)
    # 如果错误文本有更新，发送邮件提醒
    if a.update:
        email_text = ''
        for error in a.error_list:
            email_text += '%s \n' % error
        Tool.Email.emailTool.MailTool.send_text_mail(email_text, '错误信息')



