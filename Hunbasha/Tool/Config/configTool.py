# encoding=utf-8
import yaml
import os
import inspect


def get_current_path(module_name=None):
    '''
       获取当前模块路径
    :param module_name: 模块名
    :return:  返回路径
    '''
    if not module_name:
        module_name = get_current_path
    cur_module = inspect.getmodule(module_name)
    path = os.path.dirname(cur_module.__file__)
    return path

# 项目根目录
ROOT = os.path.abspath(os.path.join(get_current_path(get_current_path), '../..'))
print(ROOT)


class ConfigTool(object):

    @classmethod
    def get(cls, section, option, path='/Config/config.yml'):
        '''
           读取yaml文件
        :param section:  配置类
        :param option:   配置项
        :param path:     配置文件路径
        :return:         读取的数据
        '''
        file_path = ROOT + path
        config = yaml.load(open(file_path, 'r'))
        return config[section][option]


