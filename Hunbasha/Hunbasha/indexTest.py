# encoding=utf-8
from queue import Queue
import queue
from Tool.hrefTool import HrefTest
import threading
import time
from Tool.Log.logTool import LogTool

index_url = 'https://bj.jiehun.com.cn'


class HunIndex:
    def __init__(self, url, is_checkIndex, index_items):
        self.url_queue = Queue()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
        }
        self.thread_stop = False
        self.items = HrefTest.get_hostsit_href(url, self.headers)
        if is_checkIndex:
            self.index_items = index_items
        self.start_time = time.time()
        self.stop_time = None
        self.error_list = []
        self.url = url
        self.is_checkIndex = is_checkIndex
        self.execute_items = []
        self.sum_url = 0

    def get_index_urlitem(self):
        LogTool.info('开始获取页面url,当前页面：{url}'.format(url=self.url))
        if self.is_checkIndex:
            self.execute_items.extend([item for item in self.items if item not in self.index_items])
        else:
            self.execute_items.extend(self.items)
        for item in list(set(self.execute_items)):
            if HrefTest.check_url(item[0]):
               item1 = (HrefTest.change_url(item[0], index_url), item[1])
               self.url_queue.put(item1, block=True, timeout=5)
        self.sum_url = self.url_queue.qsize()
        LogTool.info('页面url获取完成，共{sum_url}个url'.format(sum_url=self.url_queue.qsize()))

    def _parse_url(self, item):
        try:
            LogTool.info('检查url: %s, 标题：%s' % (str(item[0]), str(item[1])))
            response = HrefTest.get(item[0], self.headers)
        except Exception as e:
            LogTool.error('请求失败，url=%s, error_messge:%s' % (str(item[0]), e))
            print('error-%s, message-%s' % (item[0], e))
            error = list(item)
            print('error', list(item))
            error.append('error_message=%s' % e)
            error.append('所在页面：%s' % self.url)
            self.error_list.append(error)
        else:
            if not response.status_code == 200:
                LogTool.error('请求失败，url=%s, error_code:%s' % (str(item[0]), response.status_code))
                print('error-%s error_code:%s' % (item[0], response.status_code))
                error = list(item)
                error.append('error_message=%s' % response.status_code)
                error.append('所在页面：%s' % self.url)
                print('----：', error)
                self.error_list.append(error)
            else:
                LogTool.info('请求成功，测试通过，url=%s,title=%s' % (str(item[0]), str(item[1])))
                print('success-%s' % item[0])
                pass

    def parse_url(self):
        while not self.thread_stop:
            try:
                item = self.url_queue.get(timeout=5)
            except queue.Empty:
                self.thread_stop = True
                break
            self._parse_url(item)
            self.url_queue.task_done()

    def run(self):
        thread_list = []
        t_url = threading.Thread(target=self.get_index_urlitem)
        thread_list.append(t_url)
        for i in range(35):
            t_parse = threading.Thread(target=self.parse_url)
            thread_list.append(t_parse)
        for t in thread_list:
            t.setDaemon(True)
            t.start()
        for q in [self.url_queue]:
            q.join()
        self.stop_time = time.time()

if __name__ == '__main__':
    page_url = 'https://bj.jiehun.com.cn/hunshasheying/storelists?source=BJIndexFL_1_1&ordersrc=BJIndexFL_1_1'
    hun = HunIndex(page_url, True)
    hun.run()
    sum_time = int(hun.stop_time - hun.start_time)
    print(sum_time)


