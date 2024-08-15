# !/usr/bin/env python
# _*_ coding:UTF-8 _*_
"""
# @Project: comen_webtest_vte
# @File: test_login.py
# @Author: shichuhong
# @Date: 2024/4/18 19:19
"""
import sys
from telnetlib import EC
from time import sleep
import pandas as pd
import allure
import pytest
from selenium.webdriver.support.wait import WebDriverWait

from conf.settings import DATA_EXCEL_DIR
from page.login_page import LoginPage


class TestLogin:

    # def setup_class(self):
    #     self.login = LoginPage()

    # 使用fixture做前置后置处理器
    @pytest.fixture(scope="function")
    def login(self):
        self.login = LoginPage()
        yield self.login
        self.login.do_quit()

    # 全局跳过，变量名必须为pytestmark，不能修改
    pytestmark = pytest.mark.skipif(condition=sys.version_info < (3, 9), reason="python版本不低于3.9")
    # myskip = pytest.mark.skipif(condition=sys.version_info < (3, 9), reason="python版本不低于3.9")


    @allure.title("登录：输入错误的账号密码后，点击登录按钮")
    @pytest.mark.UserCenter
    @pytest.mark.run(order=1)
    # @myskip
    @pytest.mark.parametrize("username, password, tip", [["000371", "Aa123456!", "系统用户不存在"], ["00037", "111111", "密码错误"], ["00037", "Aa123456!", "验证码不能为空"]])
    def test_login_click(self, username, password, tip):
        login_tip = self.login.input_username_password(username, password).login_btn().get_tips()
        assert login_tip == tip, f"预期登录提示与实际不一致，预期提示为：{tip}，实际提示为：{login_tip}"


    @allure.epic("xhs")
    @allure.feature("登录")
    @allure.title("输入正确的账号密码，点击登录按钮")
    @pytest.mark.UserCenter
    @pytest.mark.run(order=3)
    @pytest.mark.parametrize("username, password, url", [["00037", "Aa123456!", "http://192.168.1.120:9800/home"]])
    def test_login_click_successfully(self, username, password, url):
        login_tip = self.login.input_username_password(username, password).input_verification_code().login_btn()
        sleep(2)
        now_url = login_tip.driver.current_url
        print("---------------------------")
        print(login_tip.driver.current_url)
        print("---------------------------")
        assert now_url == url, f"预期跳转页面与实际不一致，预期页面为：{url}，实际页面为：{now_url}"

    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # excel表格参数化
    def load_test_data(file_name):
            df = pd.read_excel(file_name, sheet_name='Sheet1', dtype={'username': str})
            # 将DataFrame转换为元组列表（list of tuples）
            return df.to_records(index=False).tolist()


    @allure.epic("xhs")
    @allure.feature("登录")
    @allure.title("输入错误的账号密码，按enter键")
    @pytest.mark.UserCenter
    @pytest.mark.run(order=2)
    @pytest.mark.skip(reason="跳过此方法")
    @pytest.mark.parametrize("username, password, tip", load_test_data(DATA_EXCEL_DIR + '/testcase_login.xlsx'))
    def test_login_enter(self, username, password, tip):
        login_tip = self.login.input_username_password(username, password).enter_login().get_tips()
        assert login_tip == tip, f"预期登录提示与实际不一致，预期提示为：{tip}，实际提示为：{login_tip}"


    @allure.epic("xhs")
    @allure.feature("登录")
    @allure.title("输入错误的账号密码，点击登录按钮")
    @pytest.mark.UserCenter
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("username, password, tip", load_test_data(DATA_EXCEL_DIR + '/testcase_login.xlsx'))
    def test_login_click(self, username, password, tip):
        login_tip = self.login.input_username_password(username, password).login_btn().get_tips()
        assert login_tip == tip, f"预期登录提示与实际不一致，预期提示为：{tip}，实际提示为：{login_tip}"


    # def teardown_class(self):
    #     self.login.do_quit()