import os
import smtplib
import zipfile
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import settings


class MailSender:
    def __init__(self, sender_email, sender_password, smtp_server, port):
        self.sender_email = sender_email  # 发件人邮箱地址
        self.sender_password = sender_password  # 发件人邮箱密码
        self.smtp_server = smtp_server  # 邮箱服务器地址
        self.port = port

    def send_email(self, to_emails, subject, message, attachment=None, directory=None):
        """
        发送邮件方法
        :param to_emails: 收件人邮箱地址，支持多个收件人，用逗号分隔
        :param subject: 邮件主题
        :param message: 邮件内容
        :param attachment: 邮件附件地址，支持多个附件，用逗号分隔
        :param directory: 需要压缩为zip格式的文件夹路径
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = to_emails
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'html'))
            # 添加附件
            if attachment:
                attachments = attachment.split(",")
                for file in attachments:
                    with open(file, 'rb') as f:
                        part = MIMEApplication(f.read())
                        part.add_header('Content-Disposition', 'attachment', filename=file.split("/")[-1])
                        msg.attach(part)
            # 压缩文件夹为zip格式
            zip_name = None
            if directory:
                zip_name = directory.split(os.sep)[-1] + ".zip"
                zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        zipf.write(os.path.join(root, file),
                                   os.path.relpath(os.path.join(root, file), os.path.join(directory, '..')))
                zipf.close()
                with open(zip_name, 'rb') as f:
                    part = MIMEApplication(f.read())
                    part.add_header('Content-Disposition', 'attachment', filename=zip_name)
                    msg.attach(part)
            # 发送邮件
            server = smtplib.SMTP(self.smtp_server, self.port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, to_emails.split(','), msg.as_string())
            server.quit()
            my_log.info(f"邮件发送成功,主题：{subject} ")
            # 删除zip文件
            if directory:
                os.remove(zip_name)
                print("zip文件删除成功 ", zip_name)
        except Exception as e:
            my_log.info(f"邮件发送失败,主题：{subject} ")
            my_log.info(e)


def create_bat_file(file_path, report_name):
    content = """@echo off 
if "%1" == "h" goto begin 
mshta vbscript:createobject("wscript.shell").run("%~nx0 h",0)(window.close)&&exit 
:begin
cd ..
allure open {}
"""
    content = content.format(report_name)
    with open(os.path.join(file_path, '双击查看报告.bat'), 'w') as bat_file:
        bat_file.write(content)


def send_email(num_tests, num_passed, num_skipped, num_failed, failure_rate):
    # 读取配置文件
    sender_email = conf.get('email_param', 'sender_email')
    sender_password = conf.get('email_param', 'sender_password')[5:-5]
    print(sender_password)
    smtp_server = conf.get('email_param', 'smtp_server')
    port = conf.get('email_param', 'port')
    to_emails = conf.get('email_param', 'to_emails')
    subject = conf.get('email_param', 'subject') + datetime.now().strftime('%Y%m%d-%H%M%S')
    # 实例化MailSender对象
    mail_sender = MailSender(sender_email, sender_password, smtp_server, port)
    # 在report创建bat文件,用于打开allure报告
    create_bat_file(REPORT_DIR, 'report')
    # 发送邮件
    message = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>UI自动化测试报告</title>
    <style>
        table {{
            font-family: arial, sans-serif;
            border-collapse: collapse;
            width: auto;
            border: 1px solid black;
        }}
        th {{
            text-align: center;
            padding: 8px;
            color: black;
        }}
        tr {{
            background-color: #f2f2f2;
        }}
        td:nth-child(1) {{
            background-color: #1bd0d6;
            color: black;
            text-align: center;
            padding: 8px;
            font-weight: bold;
        }}
        td:nth-child(2) {{
            background-color: #7ef542;
            color: black;
            text-align: center;
            padding: 8px;
            font-weight: bold;
        }}
        td:nth-child(3) {{
            background-color: #aeb8b9ad;
            color: black;
            text-align: center;
            padding: 8px;
            font-weight: bold;
        }}
        td:nth-child(4) {{
            background-color: #f54242;
            color: white;
            text-align: center;
            padding: 8px;
            font-weight: bold;
        }}
        td:last-child {{
            text-align: center;
            color: black;
            background-color: #f2f211f0;
            font-weight: bold;
        }}
        .div {{
            margin-top:10px;
            margin-bottom:0px
        }}
    </style>
</head>
<body>
<h2>UI自动化测试报告</h2>
<table>
    <thead>
    <tr>
        <th style="background-color: #1bd0d6;">用例总数</th>
        <th style="background-color: #7ef542;">成功用例数</th>
        <th style="background-color: #aeb8b9ad;">跳过用例数</th>
        <th style="background-color: #f54242;">失败用例数</th>
        <th style="background-color: #f2f211f0;">失败率</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>{num_tests}</td>
        <td>{num_passed}</td>
        <td>{num_skipped}</td>
        <td>{num_failed}</td>
        <td>{failure_rate}%</td>
    </tr>
    </tbody>
</table>
<div>
    <br>
    <strong>
        <span>请下载附件output.zip，以获取详细测试报告</span>
    </strong>
    <br>
    <div class="div">
        <em>
            <span>☆☆ 按照以下步骤，可打开详细测试报告：</span>
        </em>
        <p>
            <small>
                <span>1、在电脑本地安装allure工具；</span><br>
                <span>2、进入附件output目录，打开report文件夹；</span><br>
                <span>3、双击程序“双击查看报告.bat”，稍等片刻即可查看报告。</span><br>
            </small>
        </p>
    </div>
    <div class="div">
        <em>
            <span>☆☆ 如需播放测试用例追踪文件（trace.zip），请前往如下网页：</span>
            <a href="https://trace.playwright.dev/" target="_blank">https://trace.playwright.dev/</a>
        </em>
        <p>
            <small>
                <span>在该页面中点击“Select file”按钮，进入output/trace_viewer/目录，选择对应用例文件夹中的trace.zip文件即可。</span>
            </small>
        </p>
    </div>
</div>
</body>
</html>
    """
    # attachment = "file1.txt, file2.jpg"  # 附件地址，用逗号分隔
    mail_sender.send_email(to_emails=to_emails, subject=subject, message=message,
                           # attachment=attachment,
                           directory=settings.OUTPUT_DIR  # 需要压缩的文件夹地址，可选
                           )


if __name__ == '__main__':
    send_email(100, 90, 3, 7, 7)
