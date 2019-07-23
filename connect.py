import pymssql as py
import pandas as pd
# 连接数据库，创建学生表，进行表查询，表录入
server = "DESKTOP-G8THN71"# 连接服务器地址
user = "sa"# 连接帐号
password = ""# 连接密码
conn = py.connect(server, user, password, "student_message")  #获取连接
cursor = conn.cursor() # 获取光标

# 创建表
# cursor.execute("""
# IF OBJECT_ID('students', 'U') IS NOT NULL
#     DROP TABLE students
# CREATE TABLE students (
#     ID INT NOT NULL,
#     name VARCHAR(100),
#     StudentID INT,
#     Sex VARCHAR(100)
#     )
# """)
# commit() 提交动作
# conn.commit()

def insert(Name, studentID, Sex):
    count_students = 0
    conn = py.connect(server, user, password, "student_message")  # 获取连接
    cursor =conn.cursor()
    cursor.execute('  select count(ID) from students')
    for row in cursor:
        count_students = row[0]
        print(row[0])
    cursor.executemany(
        "INSERT INTO students VALUES (%d, %s, %d,%s)",
        [(count_students+1, Name, studentID, Sex)])
# 你必须调用 commit() 来保持你数据的提交如果你没有将自动提交设置为true
    conn.commit()
# 导出学生信息表
def find_student_all():
    conn = py.connect(server, user, password, "student_message")  # 获取连接
    cursor =conn.cursor()
    sql = "select * from students"
    df = pd.read_sql(sql, conn)
    df.to_excel(r'E:\01STUDY\20190701\work\openVersion\excel\all.xlsx',index=False)
    print('ok')
    conn.commit()
def readName(idnum):
    Name = -1
    conn = py.connect(server, user, password, "student_message")  # 获取连接
    cursor =conn.cursor()
    cursor.execute('  select Name from students where ID='+str(idnum))
    for row in cursor:
        if row[0]!=[]:
            Name = row[0]
    conn.commit()
    return Name
def readIDbaseStudentID(StudentID):
    ID = -1
    conn = py.connect(server, user, password, "student_message")  # 获取连接
    cursor =conn.cursor()
    cursor.execute('  select ID from students where StudentID='+str(StudentID))
    for row in cursor:
        if row[0]!=[]:
            ID = row[0]
    conn.commit()
    conn.close()
    return ID
def readSex(idnum):
    Sex = -1
    conn = py.connect(server, user, password, "student_message")  # 获取连接
    cursor =conn.cursor()
    cursor.execute('  select Sex from students where ID='+str(idnum))

    for row in cursor:
        if row[0]!=[]:
            Sex = row[0]
    conn.commit()
    return Sex
def readID(name):
    ID = -1
    conn = py.connect(server, user, password, "student_message")  # 获取连接
    cursor =conn.cursor()
    cursor.execute('  select ID from students where name='+'\''+str(name)+'\'')
    for row in cursor:
        if row[0]!=[]:
            ID = row[0]
    conn.commit()
    return ID
def readStudentID(idnum):
    StudentID = -1
    conn = py.connect(server, user, password, "student_message")  # 获取连接
    cursor =conn.cursor()
    cursor.execute('  select StudentID from students where ID='+str(idnum))
    for row in cursor:
        if row[0]!=[]:
            StudentID = row[0]
    conn.commit()
    return StudentID
conn.close()
#
# # 注：在任何时候，在一个连接下，一次正在执行的数据库操作只会出现一个cursor对象