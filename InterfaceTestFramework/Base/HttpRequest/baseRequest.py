# encoding=utf-8
import requests
import sys
import io
from Tool.Config.configTool import ConfigTool

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')

'''
    requests.request(method,url,**kwargs)
    method – 新建 Request 对象要使用的HTTP方法
    url – 新建 Request 对象的URL
    params – (可选) Request 对象的查询字符中要发送的字典或字节内容
    data – (可选) Request 对象的 body 中要包括的字典、字节或类文件数据
    json – (可选) Request 对象的 body 中要包括的 Json 数据
    headers – (可选) Request 对象的字典格式的 HTTP 头
    cookies – (可选) Request 对象的字典或 CookieJar 对象
    files – (可选) 字典，'name': file-like-objects (或{'name': ('filename', fileobj)}) 用于上传含多个部分的（类）文件对象
    auth – (可选) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
    timeout (浮点或元组) – (可选) 等待服务器数据的超时限制，是一个浮点数，或是一个(connect timeout, read timeout) 元组
    allow_redirects (bool) – (可选) Boolean. True 表示允许跟踪 POST/PUT/DELETE 方法的重定向
    proxies – (可选) 字典，用于将协议映射为代理的URL
    verify – (可选) 为 True 时将会验证 SSL 证书，也可以提供一个 CA_BUNDLE 路径
    stream – (可选) 如果为 False，将会立即下载响应内容
    cert – (可选) 为字符串时应是 SSL 客户端证书文件的路径(.pem格式)，如果是元组，就应该是一个(‘cert’, ‘key’) 二元值对
'''


class RequestHttp(object):
    @classmethod
    def get(cls, name, config_section='Http', param=None):
        try:
            host = ConfigTool.get(config_section, 'Host')
            url = host + name
            response = requests.get(url, params=param)
            print(response.url)
            return response.json()
        except Exception as e:
            print('错误：%s' % e)

    @classmethod
    def post(cls, name, config_section='Http', data=None):
        try:
            host = ConfigTool.get(config_section, 'Host')
            url = host + '/' + name
            response = requests.post(url, data=data)
            return response.json()
        except Exception as e:
            print('错误：%s' % e)

params={
"city_id" : "110900",
"access_token" : "",
"client_guid" : 3232235777,
"client_timestamp" : 1509415724,
"app_id" : 10011,
"client_version" : "1.0.1",
"app_usign" : "avdjMd3Lx930nKrZTSeQE/caSSw=",
}
print(RequestHttp.get('/common/channel/hunlifuwu/index', param=params))
