import os

import pytest
import allure
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from config.config import Config
from pages.login_page import LoginPage
from pages.home_page import HomePage

load_dotenv()

pageobject = None


@pytest.fixture(scope="session")
def browser():
    clear_output()
    """浏览器实例"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=Config.HEADLESS,
            slow_mo=Config.SLOW_MO
        )
        yield browser
        browser.close()


@pytest.fixture
def context(browser):
    """浏览器上下文"""
    context = browser.new_context(
        viewport={
            "width": Config.VIEWPORT_WIDTH,
            "height": Config.VIEWPORT_HEIGHT
        },
        ignore_https_errors=True
    )

    # 监听网络请求
    context.on("response", lambda response:
    allure.attach(
        f"Response: {response.url} - {response.status}",
        name="Network",
        attachment_type=allure.attachment_type.TEXT
    ) if response.status >= 400 else None
               )

    yield context
    context.close()


@pytest.fixture
def page(context):
    """页面实例"""
    page = context.new_page()
    page.set_default_timeout(Config.TIMEOUT)
    page.set_default_navigation_timeout(Config.NAVIGATION_TIMEOUT)

    # 监听控制台错误
    page.on("console", lambda msg:
    allure.attach(
        f"Console {msg.type}: {msg.text}",
        name="Console",
        attachment_type=allure.attachment_type.TEXT
    ) if msg.type == "error" else None
            )

    yield page
    page.close()


@pytest.fixture
def login_page(page):
    """登录页面实例"""
    return LoginPage(page)


@pytest.fixture
def home_page(page):
    """首页实例"""
    return HomePage(page)


@pytest.fixture
def logged_in_page(login_page, home_page):
    """已登录的页面"""
    login_page.navigate()
    login_page.login_with_default_credentials()
    return home_page


# Hook 函数
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """获取每个用例状态的钩子函数，失败时自动记录日志和截图"""
    outcome = yield
    rep = outcome.get_result()

    # 只处理测试主体执行阶段的失败
    if rep.when == "call" and rep.failed:
        _log_failure(item, rep)
        _capture_screenshot(item)


def _log_failure(item, rep):
    """记录失败日志到文件"""
    failures_log = os.path.join(Config.logs, "failures.log")
    try:
        with open(failures_log, "a", encoding="utf-8") as f:
            case_info = _get_case_info(item)
            f.write(f"{rep.nodeid}{case_info}\n")
    except Exception as e:
        print(f"记录失败日志异常: {e}")


def _get_case_info(item):
    """获取用例额外信息"""
    if "CaseData" in item.fixturenames:
        case_data = item.funcargs["CaseData"]
        return f" ({case_data})"
    return ""


def _capture_screenshot(item):
    """捕获失败截图"""
    if not hasattr(pageobject, "screenshot"):
        return

    try:
        with allure.step('添加失败截图...'):
            case_id = item.funcargs["CaseData"].get("用例编号", "unknown")
            filename = f"{case_id}_失败截图.png"
            path = os.path.join(Config.test_screenshot_dir, filename)

            screenshot_file = pageobject.screenshot(path=path)
            allure.attach(
                screenshot_file,
                "失败截图",
                allure.attachment_type.PNG
            )
    except Exception as e:
        print(f"截图失败: {e}")
