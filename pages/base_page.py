import logging
import os

from playwright.sync_api import Page, expect
from config.config import Config


class BasePage:
    """所有页面的基类"""

    def __init__(self, page: Page):
        self.page = page
        self.timeout = Config.TIMEOUT
        self.logger = logging.getLogger(__name__)

    def goto(self, url: str) -> None:
        """导航到指定URL"""
        self.page.goto(url, wait_until="networkidle")

    def wait_for_page_load(self, timeout: int = 30000) -> None:
        """等待页面加载"""
        self.page.wait_for_load_state("load", timeout=timeout)

    def find_element(self, selector: str, timeout: int = 10000):
        """查找单个元素，带显式等待"""
        try:
            self.logger.debug(f"查找元素:{selector}")
            element = self.page.locator(selector)
            element.wait_for(state="visible", timeout=timeout)
            return element
        except TimeoutError:
            self.logger.error(f"元素未找到: {selector}")
            raise

    def find_elements(self, selector: str, timeout: int = 10000):
        """查找多个元素"""
        try:
            self.logger.debug(f"查找多个元素: {selector}")
            elements = self.page.locator(selector)
            elements.wait_for(state="visible", timeout=timeout)
            return elements
        except TimeoutError:
            self.logger.error(f"元素未找到: {selector}")
            return None

    def click(self, selector: str):
        """点击元素"""
        self.logger.debug(f"点击元素: {selector}")
        self.page.click(selector)

    def fill(self, selector: str, value: str) -> None:
        """填充输入框"""
        self.find_element(selector).clear()
        self.logger.debug(f"填充输入框: {selector}, 值: {value}")
        self.page.fill(selector, value)

    def get_text(self, selector: str) -> str:
        """获取元素文本"""
        return self.page.text_content(selector)

    def select_option(self, selector: str, value: str, timeout: int = 10000) -> None:
        """选择下拉框选项"""
        self.logger.info(f"在下拉框 {selector} 中选择: {value}")
        self.select_option(selector, value)

    def press_key(self, selector: str, key: str, timeout: int = 10000) -> None:
        """在元素上按下键盘按键"""
        self.logger.info(f"在元素 {selector} 上按下按键: {key}")
        self.press_key(selector, key, timeout)

    def wait_for_selector(self, selector: str, state="visible", timeout=None):
        """等待元素"""
        timeout = timeout or self.timeout
        self.page.wait_for_selector(selector, state=state, timeout=timeout)

    def wait_for_url(self, url: str):
        """等待URL"""
        self.page.wait_for_url(url)

    def take_screenshot(self, name: str):
        """截图"""
        self.page.screenshot(path=f"reports/screenshots/{name}.png")

    def get_by_role(self, role: str, name: str = None):
        """通过角色定位元素"""
        return self.page.get_by_role(role, name=name)

    def get_by_text(self, text: str):
        """通过文本定位元素"""
        return self.page.get_by_text(text)

    def get_by_placeholder(self, text: str):
        """通过占位符定位元素"""
        return self.page.get_by_placeholder(text)

    def expect(self, locator):
        """返回expect对象"""
        return expect(locator)

    def assert_element_visible(self, selector: str, timeout: int = 10000) -> None:
        """断言元素可见"""
        self.logger.info(f"断言元素可见: {selector}")
        element = self.find_element(selector, timeout)
        expect(element).to_be_visible()

    def assert_element_contains_text(self, selector: str, expected_text: str, timeout: int = 10000) -> None:
        """断言元素包含指定文本"""
        self.logger.info(f"断言元素 {selector} 包含文本: {expected_text}")
        element = self.find_element(selector, timeout)
        expect(element).to_contain_text(expected_text)

    def assert_url_contains(self, expected_text: str) -> None:
        """断言当前URL包含指定文本"""
        current_url = self.page.url
        self.logger.info(f"断言URL包含 '{expected_text}'，当前URL: {current_url}")
        assert expected_text in current_url, f"URL不包含预期文本。当前URL: {current_url}"

    def is_element_present(self, selector: str, timeout: int = 5000) -> bool:
        """检查元素是否存在（不抛出异常）"""
        try:
            self.page.locator(selector).first.wait_for(state="visible", timeout=timeout)
            return True
        except TimeoutError:
            return False


def switch_to_frame(self, selector: str, timeout: int = 10000) -> None:
    """切换到iframe框架"""
    self.logger.info(f"切换到iframe: {selector}")
    frame = self.page.frame_locator(selector)
    return frame


def switch_to_new_tab(self, timeout: int = 10000) -> None:
    """切换到新打开的标签页"""
    self.logger.info("切换到新标签页")
    self.page.wait_for_event("popup", timeout=timeout)
    # 获取所有页面，最后一个是最新打开的
    all_pages = self.page.context.pages
    new_page = all_pages[-1]
    new_page.bring_to_front()
    self.page = new_page


def close_current_tab(self) -> None:
    """关闭当前标签页并切换回主标签页"""
    self.logger.info("关闭当前标签页")
    all_pages = self.page.context.pages
    if len(all_pages) > 1:
        self.page.close()
        self.page = all_pages[-2]  # 切换回前一个标签页
        self.page.bring_to_front()


def close_current_tab(self) -> None:
    """关闭当前标签页并切换回主标签页"""
    self.logger.info("关闭当前标签页")
    all_pages = self.page.context.pages
    if len(all_pages) > 1:
        self.page.close()
        self.page = all_pages[-2]  # 切换回前一个标签页
        self.page.bring_to_front()


def execute_script(self, script: str, *args):
    """执行JavaScript脚本"""
    self.logger.debug(f"执行JavaScript: {script}")
    return self.page.evaluate(script, *args)


def scroll_to_element(self, selector: str, timeout: int = 10000) -> None:
    """滚动到指定元素"""
    self.logger.info(f"滚动到元素: {selector}")
    element = self.find_element(selector, timeout)
    element.scroll_into_view_if_needed()


def scroll_to_bottom(self) -> None:
    """滚动到页面底部"""
    self.logger.info("滚动到页面底部")
    self.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def upload_file(self, file_input_selector: str, file_path: str, timeout: int = 10000) -> None:
    """上传文件"""
    self.logger.info(f"上传文件: {file_path} 到元素: {file_input_selector}")
    element = self.find_element(file_input_selector, timeout)
    element.set_input_files(file_path)


def download_file(self, download_selector: str, download_dir: str = "downloads", timeout: int = 30000) -> str:
    """下载文件并返回文件路径"""
    self.logger.info(f"下载文件，触发元素: {download_selector}")

    with self.page.expect_download(timeout=timeout) as download_info:
        self.click(download_selector, timeout=5000)

    download = download_info.value
    os.makedirs(download_dir, exist_ok=True)
    file_path = os.path.join(download_dir, download.suggested_filename)
    download.save_as(file_path)

    self.logger.info(f"文件已下载: {file_path}")
    return file_path
