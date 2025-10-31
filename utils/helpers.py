import allure
import pytest
from allure_commons import fixture
from playwright.sync_api import Page


@fixture
def take_screenshot(page: Page, name: str):
    """截图并附加到Allure报告"""
    screenshot = page.screenshot()
    allure.attach(
        screenshot,
        name=name,
        attachment_type=allure.attachment_type.PNG
    )


def log_response(response):
    """记录网络响应"""
    allure.attach(
        f"URL: {response.url}\nStatus: {response.status}\nHeaders: {response.headers}",
        name="Network Response",
        attachment_type=allure.attachment_type.TEXT
    )
