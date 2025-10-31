#!/usr/bin/env python3
import subprocess
import sys
import os


def run_tests():
    """运行测试并生成报告"""

    # 创建报告目录
    os.makedirs("reports/screenshots", exist_ok=True)
    os.makedirs("reports/allure-results", exist_ok=True)

    # 运行测试
    commands = [
        # 运行所有测试
        ["pytest", "tests/", "-v", "--alluredir=reports/allure-results"],

        # 运行冒烟测试
        # ["pytest", "tests/", "-m", "smoke", "-v"],

        # 并行运行测试
        # ["pytest", "tests/", "-n", "auto", "-v"],
    ]

    for cmd in commands:
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd)
        if result.returncode != 0:
            print("Tests failed!")
            sys.exit(result.returncode)

    print("All tests completed successfully!")


if __name__ == "__main__":
    run_tests()