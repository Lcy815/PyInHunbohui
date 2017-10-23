# encoding=utf-8
import requests
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')


class RequestHttp(object):
    @classmethod
    def request_data(cls, method, url, **param):
        try:
            response = requests.request(method, url, params=param)
            return response.json()
        except Exception as e:
            print('error：%s' % e)


print(RequestHttp.request_data('GET', 'http://www.baidu.com'))

