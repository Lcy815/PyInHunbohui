# encoding: utf-8
import yaml
import os
import inspect


def get_current_path(module_name=None):
    '''
    获取当前模块所在路径
    :param module_name:  模块名
    :return:  路径
    '''
    if not module_name:
        module_name = get_current_path
    cur_module = inspect.getmodule(module_name)
    path = os.path.dirname(cur_module.__file__)
    return path

# 项目根目录 (如果修改了目录结构，这里也需要随之修改，..代表上层目录，../..代表上上层)
ROOT = os.path.abspath(os.path.join(get_current_path(get_current_path), '../..'))


class ConfigTool(object):
    @classmethod
    def get(cls, section, option, path='/Config/config.yml'):
        '''
        获取配置信息string
        :param section: 配置类
        :param option:  配置项
        :param path:    配置yml文件路径
        :return:        string格式信息
        '''
        file_path = ROOT + path
        config = yaml.load(open(file_path, 'r'))
        return str(config[section][option])

    @classmethod
    def getint(cls, section, option, path='/Config/config.yml'):
        '''
        获取配置信息int类型
        :param section: 配置类
        :param option:  配置项
        :param path:    配置yml文件路径
        :return:        string格式信息
        '''
        file_path = ROOT + path
        f = open(file_path)
        config = yaml.load(f)
        return int(config[section][option])

    @classmethod
    def get_case(cls, path):
        file_path = ROOT + path
        f = open(file_path)
        data = yaml.load(f)
        return data['TEST_CASE']

datas = ConfigTool.get_case('/Config/case_model.yml')
print(datas)



