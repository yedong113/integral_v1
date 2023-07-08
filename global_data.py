import sys


class GlobalData:
    def __init__(self):
        self.userid = None
        self.username = None
        self.student_info = []

    def __str__(self):
        stu_str = ""
        for item in self.student_info:
            stu_str = stu_str + "学生姓名:" + item[1] + "\n"
            stu_str = stu_str + "性别:" + item[2] + "\n"
            stu_str = stu_str + "生日:" + item[3] + "\n"
            stu_str = stu_str + "学校:" + item[5] + "\n"
            stu_str = stu_str + "班级:" + item[4]
        return f'账号ID: {self.userid},账号: {self.username} \n[学生信息:]\n{stu_str}'


global_data = GlobalData()
