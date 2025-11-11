from .base_page import BasePage
from config.config import Config


class LoginPage(BasePage):
    """登录页面"""
    __LOGIN_PAGE = "/login"
    # 定位器
    __USERNAME_INPUT = "#userName"
    __PASSWORD_INPUT = "#password"
    __LOGIN_BUTTON = "#login"
    __ERROR_MESSAGE = "#name"
    __USERNAME_LABEL = "#userName-value"

    def __init__(self, page):
        super().__init__(page)
        self.url = f"{Config.BASE_URL}{self.__LOGIN_PAGE}"

    def navigate(self):
        """导航到登录页面"""
        self.goto(self.url)

    def login(self, username: str, password: str):
        """执行登录操作"""
        self.fill(self.__USERNAME_INPUT, username)
        self.fill(self.__PASSWORD_INPUT, password)
        self.click(self.__LOGIN_BUTTON)

    def get_error_message(self) -> str:
        """获取错误消息"""
        return self.get_text(self.__ERROR_MESSAGE)

    def get_username_text(self) -> str:
        """获取用户名文本"""
        return self.get_text(self.__USERNAME_LABEL)

    def is_login_successful(self) -> bool:
        """检查登录是否成功"""
        try:
            self.wait_for_selector(self.__USERNAME_LABEL, timeout=5000)
            return True
        except:
            return False
