# encoding=utf-8

import time
import io
import threading

import sys

from Tool.hrefTool import HrefTest
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')


class Href(object):
    gl_num = 0

    def __init__(self, url_base, header):
        '''
        :param url_base:  要抓取页面的url
        :param headers:
        '''
        self.url = url_base
        self.header = header
        self.error = self.execute(url_base, header)

    @classmethod
    def change_url(cls, url, url_base):

        if url.startswith('http'):
            final_url = url
        elif url.startswith('//'):
            final_url = 'http:' + url
        else:
            final_url = url_base + url

        return final_url

    @staticmethod
    def execute(url_base, header):
        items = HrefTest.get_hostsit_href(url_base, header)
        global gl_num
        gl_num = len(items)
        lock = threading.RLock()
        error_lists = []

        def url_request():
            global gl_num
            while gl_num > 0:
                lock.acquire()
                item = items[gl_num - 1]
                gl_num -= 1
                lock.release()

                print(item, gl_num, threading.current_thread().getName())
                url_href = item[0]
                final_url = Href.change_url(url_href, url_base)
                try:
                    response = HrefTest.get(final_url, headers=headers)
                except Exception as e:
                    error_lists.append(item)
                else:
                    if not response.status_code == 200:
                        error_lists.append(item)


        thread_list = []
        for i in range(15):
            t = threading.Thread(target=url_request)
            thread_list.append(t)
            t.start()

        for t in thread_list:
            t.join()

        return error_lists

start_time = time.time()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
}
sum_error = []
# 主站 一级页面      所有url
index_url = 'https://bj.jiehun.com.cn'
index_items = HrefTest.get_hostsit_href(index_url, headers)
# 执行测试 查看页面s
a = Href(index_url, headers)
sum_error.extend(a.error)
# 每个secondary 次级页面  url
for index_item in index_items:
    print('站点是：', index_item[0])
    second_url = Href.change_url(index_item[0], index_url)
    # 二级扫描只扫描婚博会相关 jiehun  hunbasha  yingbasha jiabasha
    if 'jiehun' in second_url or 'hunbasha' in second_url or 'yingbasha' in second_url or 'jiabasha' in second_url:
        secondary_items = HrefTest.get_hostsit_href(second_url, headers)
        # 将与主站重复url 剔除   出错url剔除
        delete_repeat = [item for item in secondary_items if item not in index_items]
        # 将出错url剔除
        delete_error = [item for item in delete_repeat if item not in sum_error]
        b = Href(second_url, headers)
        sum_error.extend(b.error)

endtime = int(time.time() - start_time)
print('00000000000000000000000000000000000000000000000')
print(endtime)

