# encoding=utf-8
from appium import webdriver
from appium_api import AppiumTool
import time

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '4.4.2'
desired_caps['deviceName'] = 'Android Emulator'
desired_caps['appPackage'] = 'com.hunbohui.yingbasha'
desired_caps['appActivity'] = '.component.loading.LoadingActivity'
# desired_caps['app'] = 'C:/Users/Administrator/Desktop/ybs_1.5.3_edm.apk_1.5.3.apk'

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
time.sleep(10)
# 跳过导航
print(AppiumTool.get_current_activity(driver))
try:
    driver.find_element_by_id('com.hunbohui.yingbasha:id/tv_guide_skip').click()
except Exception as e:
    print(e)
time.sleep(5)
print(AppiumTool.get_current_activity(driver))
try:
    driver.find_element_by_id('com.hunbohui.yingbasha:id/tv_start').click()
except Exception as e:
    print(e)
time.sleep(5)
# 选择城市
print(AppiumTool.get_current_activity(driver))
time.sleep(10)
try:
    driver.find_element_by_name('北京').click()
except Exception as e:
    print(e)
time.sleep(10)
# 跳过登录
print(AppiumTool.get_current_activity(driver))
driver.find_element_by_id('com.hunbohui.yingbasha:id/title_bar_right_btn').click()
time.sleep(10)
print(AppiumTool.get_current_activity(driver))

# by.id
# driver.find_element_by_id('com.hunbohui.yingbasha:id/ll_nav').click()
# by.class
# driver.find_element_by_class_name('android.widget.LinearLayout').click()
# driver.find_element_by_name('活动').click()

driver.find_element_by_xpath("//android.widget.TextView[contains(@text, '活动')]").click()
print(driver.page_source)
