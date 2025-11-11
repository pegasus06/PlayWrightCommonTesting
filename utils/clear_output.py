import datetime
import os

from config.settings import config


def clear_folder(folder_path):
    print(f'开始检查文件--{folder_path}')
    if not os.path.exists(folder_path):
        return
    # 如果文件夹为空，则直接删除并退出
    if not os.listdir(folder_path):
        os.rmdir(folder_path)
        print("Removed empty folder: ", folder_path)
        return
    # 遍历文件夹中的文件
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        # 判断是否是文件夹
        if os.path.isdir(file_path):
            # 如果是文件夹，递归遍历子文件夹
            clear_folder(file_path)
        else:
            # 如果是文件，获取文件修改时间
            modify_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).date()
            # 获取当前日期-过期天数前的日期
            days = int(os.getenv().get('logs_and_output_expired_days', 'expired_days'))
            threshold_date = datetime.datetime.now().date() - datetime.timedelta(days=days)
            # 判断是否需要清理
            if modify_time < threshold_date:
                os.remove(file_path)
                print("Removed: ", file_path)
                # 删除文件后检查父文件夹是否为空
                if not os.listdir(folder_path):
                    os.rmdir(folder_path)
                    print("Removed empty folder: ", folder_path)


def clear_output():
    # 在项目启动时调用清理函数,需清理的目录包括：日志、HAR、失败截图、成功截图。
    clear_folder(config.LOG_DIR)
    clear_folder(config.FAIL_IMG_DIR)
    clear_folder(config.PASS_IMG_DIR)
