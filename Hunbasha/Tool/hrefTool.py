# encoding=utf-8
import re
import requests
import threading
import sys
import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')


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
            return []
        else:
            # print(response.text)
            # pattern = re.compile('<a.*href="(.*?)".{0}=?"?.*"?>(.*?)</a>')
            pattern = re.compile('href="(.*?)"{1}.?.{0,10}?=?"?.*"?>(.+)?</a>')
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

if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
        'Host': 'bj.jiehun.com.cn',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    a = HrefTest.get_hostsit_href(
        'https://bj.jiehun.com.cn/', headers)




