from .base_page import BasePage
from utils.config import Config


class HomePage(BasePage):
    """首页"""

    # 定位器
    LOGOUT_BUTTON = "//button[text()='Log out']"
    USERNAME_LABEL = "#userName-value"
    SEARCH_BOX = "#searchBox"
    SEARCH_BUTTON = "//button[@type='submit']"

    def __init__(self, page):
        super().__init__(page)
        self.url = f"{Config.BASE_URL}/profile"

    def navigate(self):
        """导航到首页"""
        self.goto(self.url)

    def logout(self):
        """执行登出操作"""
        self.click(self.LOGOUT_BUTTON)

    def search(self, keyword: str):
        """搜索操作"""
        self.fill(self.SEARCH_BOX, keyword)
        self.page.press(self.SEARCH_BOX, "Enter")

    def get_username(self) -> str:
        """获取用户名"""
        return self.get_text(self.USERNAME_LABEL)

    def is_logout_visible(self) -> bool:
        """检查登出按钮是否可见"""
        try:
            self.wait_for_selector(self.LOGOUT_BUTTON, timeout=5000)
            return True
        except:
            return False