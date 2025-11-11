import datetime
import hashlib


class Md5Util:
    def __init__(self, salt='!@#$%^wertyRFGH'):
        self.salt = salt

    def md5(self, text):
        hl = hashlib.md5()
        hl.update(text.encode(encoding='utf8'))
        md5 = hl.hexdigest()
        return md5

    def md5_salt(self, text):
        s = self.md5(text)
        print('md5=', s)
        return self.md5(s + self.salt)


if __name__ == '__main__':
    str = '504bda95eb584f81a02c91a4c0016c11$10f8db24cca63ceb0ca0a9744ab25016'
    mima = '888888'
    password_sjk = str.split('$')[0]
    salt = str.split('$')[1]
    start_time = datetime.datetime.now()
    md5 = Md5Util(salt)
    py_psw = md5.md5_salt(mima)
    end_time = datetime.datetime.now()
    # print(start_time)
    # print(end_time)
    print('加密时间：',end_time-start_time)
    print('数据库的密码', password_sjk)
    print('代码产的密码', py_psw)
    print('是否正确:', py_psw == password_sjk)
