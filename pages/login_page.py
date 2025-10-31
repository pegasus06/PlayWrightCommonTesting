from .base_page import BasePage
from utils.config import Config


class LoginPage(BasePage):
    """登录页面"""

    # 定位器
    USERNAME_INPUT = "#userName"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login"
    ERROR_MESSAGE = "#name"
    USERNAME_LABEL = "#userName-value"

    def __init__(self, page):
        super().__init__(page)
        self.url = f"{Config.BASE_URL}/login"

    def navigate(self):
        """导航到登录页面"""
        self.goto(self.url)

    def login(self, username: str, password: str):
        """执行登录操作"""
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def login_with_default_credentials(self):
        """使用默认凭据登录"""
        self.login(Config.USERNAME, Config.PASSWORD)

    def get_error_message(self) -> str:
        """获取错误消息"""
        return self.get_text(self.ERROR_MESSAGE)

    def get_username_text(self) -> str:
        """获取用户名文本"""
        return self.get_text(self.USERNAME_LABEL)

    def is_login_successful(self) -> bool:
        """检查登录是否成功"""
        try:
            self.wait_for_selector(self.USERNAME_LABEL, timeout=5000)
            return True
        except:
            return False