# encoding=utf-8

import  requests
from Base.HttpRequest.baseRequest import *


class ApiRequest(object):

    @classmethod
    def api_request(cls, case_model):
        if case_model.method == 'GET':
            return RequestHttp.get(case_model.name, param=case_model.params)
        elif case_model.method == 'POST':
            return RequestHttp.post(case_model.name, data=case_model.params)





