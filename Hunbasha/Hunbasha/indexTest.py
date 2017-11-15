# encoding=utf-8
from queue import Queue
import queue
from Tool.hrefTool import HrefTest
import threading
import time
from Tool.Log.logTool import LogTool

index_url = 'https://bj.jiehun.com.cn'


class HunIndex:
    def __init__(self, url):
        self.url_queue = Queue()
        self.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        self.thread_stop = False
        self.items = HrefTest.get_hostsit_href(url, self.headers)
        self.start_time = time.time()
        self.stop_time = None
        self.error_list = []
        self.url = url

    def get_index_urlitem(self):
        LogTool.info('开始获取页面url,当前页面：{url}'.format(url=self.url))
        for item in self.items:
            # if HrefTest.check_url(item[0]):
            self.url_queue.put(item, block=True, timeout=5)
        LogTool.info('页面url获取完成，共{sum_url}个url'.format(sum_url=len(self.items)))

    def _parse_url(self, item):
        try:
           LogTool.info('检查url: %s, 标题：%s' % (item[0], item[1]))
           response = HrefTest.get(HrefTest.change_url(item[0], index_url), self.headers)
        except Exception as e:
            LogTool.error('请求失败，url=%s, error_messge:%s' % (item[0], e))
            # print('error-%s, message-%s' % (item[0], e))
            self.error_list.append(item)
        else:
            if not response.status_code == 200:
                LogTool.error('请求失败，url=%s, error_code:%s' % (item[0], response.status_code))
                # print('error-%s' % item[0])
                self.error_list.append(item)
            else:
                LogTool.info('请求成功，测试通过，url=%s,title=%s' % (item[0], item[1]))
                # print('success-%s' % item[0])
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
        for i in range(30):
            t_parse = threading.Thread(target=self.parse_url)
            thread_list.append(t_parse)
        for t in thread_list:
            t.setDaemon(True)
            t.start()
        for q in [self.url_queue]:
            q.join()
        self.stop_time = time.time()

if __name__ == '__main__':
    hun = HunIndex(index_url)
    hun.run()
    sum_time = int(hun.stop_time - hun.start_time)
    print(sum_time)


