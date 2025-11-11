import os


class Config:

    def get_path(path: str = None) -> str:
        root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        if path:
            if "/" in path:
                path = path.split("/")
            elif "\\" in path:
                path = path.split("\\")
            else:
                path = [path]
            return os.path.join(root_path, *path)
        else:
            return root_path

    # 项目根目录
    ITEM_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 状态存储文件目录
    AUTH_DIR = os.path.join(ITEM_DIR, 'auth')

    # 配置文件目录
    CONF_DIR = os.path.join(ITEM_DIR, 'config')

    # 元素定位文件目录
    PAGES_DIR = os.path.join(ITEM_DIR, 'pages')

    # 运行日志目录
    LOG_DIR = os.path.join(ITEM_DIR, 'logs')

    # 自动化产出目录
    OUTPUT_DIR = os.path.join(ITEM_DIR, 'output')

    # 失败截图目录
    FAIL_IMG_DIR = os.path.join(OUTPUT_DIR, 'images', 'fail')

    # 成功截图目录
    PASS_IMG_DIR = os.path.join(OUTPUT_DIR, 'images', 'pass')

    # 测试报告目录
    REPORT_DIR = os.path.join(OUTPUT_DIR, 'report')

    # 测试结果目录
    RESULT_DIR = os.path.join(OUTPUT_DIR, 'result')

    # 测试用例追踪文件目录
    TRACE_VIEWER_DIR = os.path.join(OUTPUT_DIR, 'trace_viewer')

    # 测试用例录屏目录
    VIDEO_DIR = os.path.join(OUTPUT_DIR, 'video')

    # 测试用例目录
    CASES_DIR = os.path.join(ITEM_DIR, 'tests', 'test_case')

    # 测试数据目录
    DATAS_DIR = os.path.join(ITEM_DIR, 'tests', 'test_datas')


config = Config()
if __name__ == '__main__':
    import os


    def create_all_directories():
        # 获取所有目录变量
        directories = [
            config.AUTH_DIR, config.CONF_DIR, config.PAGES_DIR, config.LOG_DIR,
            config.FAIL_IMG_DIR, config.PASS_IMG_DIR, config.REPORT_DIR, config.RESULT_DIR,
            config.TRACE_VIEWER_DIR, config.VIDEO_DIR, config.CASES_DIR, config.DATAS_DIR
        ]

        for dir_path in directories:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
                print(f"✓ 目录已创建: {dir_path}")
            else:
                print(f"○ 目录已存在: {dir_path}")


    # 执行创建
    create_all_directories()
