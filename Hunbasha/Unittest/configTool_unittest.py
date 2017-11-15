# encoding=utf-8
from Tool.Config.configTool import ConfigTool
import unittest


class ConfigTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_config(self):
        section = 'Hunbasha'
        option = 'base_url'
        data = ConfigTool.get(section, option)
        print(data)



if __name__ == '__main__':
    unittest.main()

