import os


class PytestUtil:
    """
    以下是os.environ.get('PYTEST_CURRENT_TEST')输出的字符串，可供参考：
    tests/test_case/manager/test_registration_information.py::TestRegistrationInformation::test_login_manager[user_login0] (call)
    """

    @staticmethod
    def get_test_method_name():
        """
        返回当前运行中的用例方法名，不包含参数后缀。
        例如：test_login_manager
        """
        return os.environ.get('PYTEST_CURRENT_TEST').split('::')[-1].split('[')[0].split(' ')[0]

    @staticmethod
    def get_test_class_name():
        """
        返回当前运行中的用例所在的测试类名class
        """
        return os.environ.get('PYTEST_CURRENT_TEST').split('::')[1]

    @staticmethod
    def get_test_case_name():
        """
        返回当前运行中的用例名，包含参数后缀。
        例如：test_login_manager[user_login0]
        """
        return os.environ.get('PYTEST_CURRENT_TEST').split('::')[-1].split(' ')[0]

    @staticmethod
    def get_test_directory():
        """
        返回当前运行中的用例所在的目录。
        例如：buyers、manager。
        """
        return os.environ.get('PYTEST_CURRENT_TEST').split('/')[2]


if __name__ == '__main__':
    s = 'tests/test_case/manager/test_registration_information.py::' \
        'TestRegistrationInformation::test_login_manager[user_login0] (call)'
    print(f'-----------------{os.sep}')
    print(s.split('/')[2])
    print(s.split('::')[-1].split('[')[0])
