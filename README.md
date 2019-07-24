# Check-in-and-Check-out-System-for-Face-Recognition
基于python的人脸识别签到/签退系统

# 简介：
人脸识别签到签退系统，使用摄像头采集数据，后根据本地数据训练，在调用摄像头识别人脸并且辨别身份。
将签到/签退信息保存到数据库中，可以导出签到信息等excel表。

# 环境：
开发平台Windows python3.7.3
project interpret:
numpy
opencv-contrib-python
pymssql
pandas
pyttsx3

# 使用说明：
直接运行demo.py
demo.py会调用connect.py baseConnect.py  

数据库使用的是sql server 此处用到（需要建立）两个表：
学生信息表(ID (int), name (char), StudentID(int), Sex(char)), 
签到表(ID(int), Name(char) StudentID(int), Sex(char), starttime(text), stoptime(text), count(text), flag(int))
以及数据库里面连接需要使用自己的库名和密码

在首次使用时：
会创建环境：三个文件夹：face_trainer， Facedata，excel 分别存储训练后的结果 人脸照片库 导出信息表

其他步骤按照语音播报进行
只有使用的人脸分类器.xml可以直接写上地址也可以放在运行后提示存放的路径中。


# 其他：
·还想继续扩充语音播报开别的线程来执行写可以中止
·加上c/s架构
·关于数据库的安全性也还有待改进
