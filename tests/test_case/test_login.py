import os.path

import pytest
import allure

from config import settings
from utils.read_yml import ReadYaml


@allure.epic("认证模块")
@allure.feature("用户登录")
class TestLogin:

    @allure.story("成功登录")
    @allure.title("使用有效凭据登录成功")
    @pytest.mark.smoke
    @pytest.mark.parametrize("test_data", ReadYaml(os.path.join(settings.config.DATAS_DIR), "test_data.yml").read())
    def test_successful_login(self, login_page, home_page, test_data):
        """测试成功登录"""
        with allure.step("导航到登录页面"):
            login_page.navigate()

        with allure.step("输入有效凭据"):
            login_page.login(test_data["userName"], test_data["password"])

        with allure.step("验证登录成功"):
            assert home_page.page.title() == test_data["expect_value"], "应该显示主页标题"
