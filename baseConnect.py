import pymssql as py
import time
import pandas as pd

server = "DESKTOP-G8THN71"# 连接服务器地址
user = "sa" # 连接帐号
password = "" # 连接密码
conn = py.connect(server, user, password, "student_message")  #获取连接
cursor = conn.cursor() # 获取光标

def insertd(idnum,Name,StudentID,Sex):    # 签到
    conn = py.connect(server, user, password, "student_message")  # 获取连接
    timenow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    cursor = conn.cursor()
    cursor.execute("INSERT INTO qiandao VALUES (%d, %s,%d,%s, %s, %s, %s,%d )", (idnum,Name,StudentID,Sex,timenow, '0', '0', 0))
    conn.commit()
    # 必须调用 commit() 来保持数据的提交
def insertt(idnum,Name,StudentID,Sex):    # 签退
    conn = py.connect(server, user, password, "student_message")  # 获取连接
    cursor = conn.cursor()
    cursor.execute("SELECT starttime FROM qiandao WHERE ID=%s and flag=%d",(idnum,0))
    starttimeget = cursor.fetchone()
    sat = str(tuple(starttimeget))
    timenow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    timeArray = time.strptime(sat, "('%Y-%m-%d %H:%M:%S',)")
    timeStamp = int(time.mktime(timeArray))
    timecout = time.time() - timeStamp
    m, s = divmod(timecout, 60)
    h, m = divmod(m, 60)
    timepass = str(h) + '小时  ' + str(m) + '分钟 ' + str(s) + '秒'
    print(timepass)
    cursor.executemany("INSERT INTO qiandao VALUES (%d, %s,%d,%s, %s, %s, %s,%d )",
        [(idnum,Name,StudentID,Sex,'0', timenow, timepass, 1)])
    conn.commit()

def peoson_sign(StudentID):# 导出学生信息表_按照学号
    conn = py.connect(server, user, password, "student_message")  # 获取连接
    cursor = conn.cursor()
    sql = "select * from qiandao where StudentID=" + str(StudentID)
    df = pd.read_sql(sql, conn)
    df.to_excel(r'E:\01STUDY\20190701\work\openVersion\excel\studentID_sign.xlsx',index=False)
    print('ok')
    conn.commit()

#peoson_sign(2016002105)

def sign():# 导出签到表
    conn = py.connect(server, user, password, "student_message")  # 获取连接
    cursor = conn.cursor()
    sql = "select * from qiandao"
    df = pd.read_sql(sql, conn)
    df.to_excel(r'E:\01STUDY\20190701\work\openVersion\excel\sign_all.xlsx', index=False)
    print('ok')
    conn.commit()
#sign()

def total_time():# 导出时长表#sign()
    conn = py.connect(server, user, password, "student_message")  # 获取连接
    cursor = conn.cursor()
    sql = "select * from qiandao where convert(nvarchar(max),count) != convert(nvarchar(max),0)"
    df = pd.read_sql(sql, conn)
    df.to_excel(r'E:\01STUDY\20190701\work\openVersion\excel\total_time.xlsx', index=False)
    print('ok')
    conn.commit()

#
# if __name__=='__main':
#     sign()
#     #peoson_sign(2016002105)

conn.close()




