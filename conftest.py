import pytest
import allure
from playwright.sync_api import sync_playwright
from utils.config import Config
from pages.login_page import LoginPage
from pages.home_page import HomePage


@pytest.fixture(scope="session")
def browser():
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
def pytest_runtest_makereport(item, call):
    """测试报告钩子"""
    if call.when == "call" and call.excinfo is not None:
        # 获取 page 对象
        page = None
        for fixture_name in item.fixturenames:
            if "page" in fixture_name:
                page = item.funcargs[fixture_name]
                break

        if page:
            # 截图并附加到报告
            screenshot = page.screenshot()
            allure.attach(
                screenshot,
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG
            )