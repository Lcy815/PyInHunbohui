# encoding=utf-8
from appium import webdriver
from appium_api import AppiumTool

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '4.4.2'
desired_caps['deviceName'] = 'Android Emulator'
desired_caps['appPackage'] = 'com.hunbohui.yingbasha'
desired_caps['appActivity'] = '.component.loading.LoadingActivity'
desired_caps['app'] = 'C:/Users/Administrator/Desktop/ybs_1.5.3_edm.apk_1.5.3.apk'

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
# 跳过导航
print(AppiumTool.get_current_activity(driver))
driver.find_element_by_id('com.hunbohui.yingbasha:id/tv_guide_skip').click()
print(AppiumTool.get_current_activity(driver))
driver.find_element_by_id('com.hunbohui.yingbasha:id/tv_start').click()
# 选择城市
print(AppiumTool.get_current_activity(driver))
driver.find_element_by_name('北京').click()
# 跳过登录
print(AppiumTool.get_current_activity(driver))
driver.find_element_by_id('com.hunbohui.yingbasha:id/title_bar_right_btn').click()
print(AppiumTool.get_current_activity(driver))
driver.find_element_by_id('com.hunbohui.yingbasha:id/ll_nav').click()
