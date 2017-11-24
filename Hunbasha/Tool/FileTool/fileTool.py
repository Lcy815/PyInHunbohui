# encoding=utf-8
import os
import filecmp


class FileTool:

    @classmethod
    def is_exists(cls, file_path):
        '''
           判断文件是否存在
        :param file_path: 文件路径
        :return:  Bool
        '''
        return os.path.exists(file_path)

    @classmethod
    def is_file_exists(cls, file_path):
        '''
           判断文件夹是否存在
        :param file_path:  文件路径
        :return:  Bool
        '''
        return os.path.isfile(file_path)

    @classmethod
    def create_file(cls, file_path):
        '''
           创建空文件
        :param file_path: 文件路径
        :return:  None
        '''
        if not FileTool.is_exists(file_path):
            with open(file_path, 'w') as f:
                print(f)
        else:
            print('Error: %s already exists' % file_path)

    @classmethod
    def write_append_file(cls, file_path, text):
        '''
           追加写入
        :param file_path: 文件路径
        :param text:  写入文本
        :return: None
        '''
        with open(file_path, 'a') as f:
            f.write(text)

    @classmethod
    def write_cover_file(cls, file_path, text):
        '''
           覆盖写入
        :param file_path: 文件路径
        :param text:  写入文本
        :return:  None
        '''
        with open(file_path, 'w') as f:
            f.write(text)

    @classmethod
    def read_file(cls, file_path):
        '''
           文件读取
        :param file_path: 文件路径
        :return:  读取文本
        '''
        with open(file_path, 'r') as f:
            text = f.read()
        if text:
            return str(text)
        else:
            print('Error: %s is empty' % file_path)

    @classmethod
    def diff_file(cls, a_file, b_file):
        '''
           比较两个文件
        :param a_file:  a文件路径
        :param b_file:  b文件路径
        :return:  相同True   不相同False
        '''
        return filecmp.cmp(a_file, b_file)



# path = 'E:\\apiLog\\error.txt'
# a_path = 'E:\\apiLog\\a.txt'
# b_path = 'E:\\apiLog\\b.txt'
# a = FileTool()
# print(a.is_exists(path))
# print(a.read_file(path))
#
# print(a.diff_file(a_path, b_path))