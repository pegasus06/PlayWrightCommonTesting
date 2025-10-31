import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """配置类"""
    # Base URL
    BASE_URL = os.getenv("BASE_URL", "192.168.10.196:8080")

    # Browser settings
    BROWSER = os.getenv("BROWSER", "chromium")
    HEADLESS = os.getenv("HEADLESS", "True").lower() == "true"
    SLOW_MO = int(os.getenv("SLOW_MO", "0"))

    # Timeout settings
    TIMEOUT = int(os.getenv("TIMEOUT", "30000"))
    NAVIGATION_TIMEOUT = int(os.getenv("NAVIGATION_TIMEOUT", "60000"))

    # Viewport
    VIEWPORT_WIDTH = int(os.getenv("VIEWPORT_WIDTH", "1920"))
    VIEWPORT_HEIGHT = int(os.getenv("VIEWPORT_HEIGHT", "1080"))

    # Test data
    USERNAME = os.getenv("USERNAME", "testuser")
    PASSWORD = os.getenv("PASSWORD", "Test1234!")

    # Allure settings
    ALLURE_RESULTS_DIR = "reports/allure-results"