# encoding=utf-8
import re
import requests
import threading


class HrefTest(object):

    @classmethod
    def get_hostsit_href(cls, url, headers):
        '''
           获取url页面所有href a标签
        :param url:       要抓取的url
        :param headers:   请求头
        :return:          所有符合的url 及标题
        '''
        try:
            response = requests.request('GET', url=url, headers=headers)
        except Exception as e:
            print('error-{url}    message-{e}'.format(url=url, e=e))
        else:
            # print(response.text)
            pattern = re.compile('<a.+href="(.*?)".{0}=?"?.*"?>(.*?)</a>')
            # pattern = re.compile('<a\b[^>]+\bhref="([^"]*)"[^>]*>([\s\S]*?)</a>')
            items = re.findall(pattern, response.text)
            return items

    @classmethod
    def get(cls, url, headers):
        '''
           get请求获取response
        :param url:       请求url
        :param headers:   请求头
        :return:          返回response对象
        '''
        return requests.request('GET', url, headers=headers)

    @classmethod
    def change_url(cls, url, url_base):

        if url.startswith('http'):
            final_url = url
        elif url.startswith('//'):
            final_url = 'http:' + url
        else:
            final_url = url_base + url

        return final_url

    @classmethod
    def check_url(cls, url):
        if url.startswith('http') or url.startswith('//') or url.startswith('/'):
            return True
        else:
            return False

    @classmethod
    def href_test(cls):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
        }
        lock = threading.RLock()
        error_lists = []
        url = 'http://bj.jiehun.com.cn'

        items = HrefTest.get_hostsit_href(url, headers)

        gl_num = len(items)

        def url_request(num):
            global gl_num
            gl_num = num
            while gl_num > 0:
                lock.acquire()
                item = items[gl_num - 1]
                print(item, gl_num)
                gl_num -= 1
                lock.release()

                url_href = item[0]
                if url_href.startswith('http'):
                    final_url = url_href
                elif url_href.startswith('//'):
                    final_url = 'http:' + url_href
                else:
                    final_url = url + url_href
                try:
                    response = HrefTest.get(final_url, headers=headers)
                except Exception as e:
                    error_dict = {'url': item[0], 'title': item[1], 'errMessage': e}
                    error_lists.append(error_dict)
                else:
                    if not response.status_code == 200:
                        error_dict = {'url': item[0], 'title': item[1]}
                        error_lists.append(error_dict)

        thread_list = []
        for i in range(15):
            t = threading.Thread(target=url_request(gl_num))
            thread_list.append(t)
            t.start()

        for t in thread_list:
            t.join()
        print(error_lists)


