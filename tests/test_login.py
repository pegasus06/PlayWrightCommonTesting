import pytest
import allure

from conftest import pytest_runtest_makereport
from utils.config import Config
from data.test_data import TestData


@allure.epic("认证模块")
@allure.feature("用户登录")
class TestLogin:

    @allure.story("成功登录")
    @allure.title("使用有效凭据登录成功")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.login
    def test_successful_login(self, login_page, home_page):
        """测试成功登录"""
        with allure.step("导航到登录页面"):
            login_page.navigate()

        with allure.step("输入有效凭据"):
            login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)

        with allure.step("验证登录成功"):
            assert home_page.is_logout_visible(), "登出按钮应该可见"
            assert home_page.get_username() == TestData.VALID_USERNAME, "用户名应该匹配"

    @pytest_runtest_makereport
    @allure.story("登录失败")
    @allure.title("使用无效凭据登录失败")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.login
    def test_failed_login(self, login_page):
        """测试登录失败"""
        with allure.step("导航到登录页面"):
            login_page.navigate()

        with allure.step("输入无效凭据"):
            login_page.login(TestData.INVALID_USERNAME, TestData.INVALID_PASSWORD)

        with allure.step("验证错误消息"):
            error_message = login_page.get_error_message()
            assert "Invalid" in error_message, "应该显示无效凭据错误"

    @allure.story("表单验证")
    @allure.title("空用户名登录验证")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_username(self, login_page):
        """测试空用户名"""
        with allure.step("导航到登录页面"):
            login_page.navigate()

        with allure.step("输入空用户名和有效密码"):
            login_page.login("", TestData.VALID_PASSWORD)

        with allure.step("验证表单验证"):
            # 这里根据实际应用的表单验证来编写断言
            assert login_page.page.url == f"{Config.BASE_URL}/login", "应该停留在登录页面"