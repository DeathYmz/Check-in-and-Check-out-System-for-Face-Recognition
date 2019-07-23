import cv2
import os
import numpy as np
from PIL import Image #pillow
import pyttsx3
import  sys
import deathymzFace.connect as connect
import deathymzFace.baseConnect as baseConnect
import time
import json

def makeDir(engine):
    flag= 0
    if not os.path.exists("face_trainer"):
        print("创建预训练环境")
        engine.say('检测到第一次启动，未检测到环境，正在创建环境')
        engine.say('正在创建预训练环境')
        os.mkdir("face_trainer")
        engine.say('创建成功')
        engine.runAndWait()
        flag=1
    if not os.path.exists("Facedata"):
        print("创建训练环境")
        engine.say('正在创建训练环境')
        os.mkdir("Facedata")
        engine.say('创建成功')
        engine.runAndWait()
        flag=1
    if not os.path.exists("excel"):
        print("创建导出表环境")
        engine.say('正在创建导出表环境')
        os.mkdir("excel")
        engine.say('创建成功')
        engine.runAndWait()
        flag = 1
    return flag

def getFace(cap,path_id):
    # 调用笔记本内置摄像头，所以参数为0，如果有其他的摄像头可以调整参数为1，2
    #cap = cv2.VideoCapture(0)
    face_detector = cv2.CascadeClassifier(r'C:\projects\opencv-python\opencv\modules\objdetect\src\cascadedetect\haarcascades\haarcascade_frontalface_default.xml')
    #face_id = input('\n enter user id:')
    print('\n Initializing face capture. Look at the camera and wait ...')
    count = 0
    while True:
        # 从摄像头读取图片
        sucess, img = cap.read()
        # 转为灰度图片
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 检测人脸
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+w), (255, 0, 0))
            count += 1
            # 保存图像
            cv2.imwrite("Facedata/User." + str(path_id) + '.' + str(count) + '.jpg', gray[y: y + h, x: x + w])
            cv2.imshow('image', img)
        # 保持画面的持续。
        k = cv2.waitKey(1)
        if k == 27:   # 通过esc键退出摄像
            break
        elif count >= 100:  # 得到1000个样本后退出摄像
            break
    cv2.destroyAllWindows()

def getImagesAndLabels(path, detector):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]  # join函数的作用
    faceSamples = []
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L')  # convert it to grayscale
        img_numpy = np.array(PIL_img, 'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)
        for (x, y, w, h) in faces:
            faceSamples.append(img_numpy[y:y + h, x: x + w])
            ids.append(id)
    return faceSamples, ids


def trainFace():
    # 人脸数据路径
    path = 'Facedata'
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(r'C:\projects\opencv-python\opencv\modules\objdetect\src\cascadedetect\haarcascades\haarcascade_frontalface_default.xml')
    print('Training faces. It will take a few seconds. Wait ...')
    faces, ids = getImagesAndLabels(path, detector)
    recognizer.train(faces, np.array(ids))
    recognizer.write(r'face_trainer\trainer.yml')
    print("{0} faces trained. Exiting Program".format(len(np.unique(ids))))

def checkFace(cam,names,engine,sign_flag):
    sex = {"female":"女士","male":"先生"}
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('face_trainer/trainer.yml')
    cascadePath = r"C:\projects\opencv-python\opencv\modules\objdetect\src\cascadedetect\haarcascades\haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX
    idnum = 0
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)
    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH))
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            idnum, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            if confidence < 100:
                Name =connect.readName(idnum)  #connect 传入ID  学生信息表找到 返回 name
                Sex =connect.readSex(idnum)  #connect ID  学生信息表找到 返回 Sex
                StudentID =connect.readStudentID(idnum) #connect ID  学生信息表找到 返回 studentID
                #idnum = names[idnum]   #利用数据库 读取学生信息表  该id 对应的name
                confidence = "{0}%".format(round(100 - confidence))
                if sign_flag=='0':  #签到
                    say(engine, "欢迎         "+Name+ sex[Sex]+"          签到成功  ")
                    baseConnect.insertd(idnum,Name,StudentID,Sex)  #签到表中 插入签到信息
                    print("欢迎      "+Name+ sex[Sex] + "签到成功  ")
                else :
                    say(engine, "欢迎         "+Name+ sex[Sex]+"          签退成功  ")
                    baseConnect.insertt(idnum,Name,StudentID,Sex)  #签到表中 插入签退信息
                    print("欢迎      "+Name+ sex[Sex] + "签退成功  ")

                # cv2.imshow("img",img)
                # os.system("pause")
                return
            else:
                idnum = "unknown"
                confidence = "{0}%".format(round(100 - confidence))
            cv2.putText(img, str(idnum), (x + 5, y - 5), font, 1, (0, 0, 255), 1)
            cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (0, 0, 0), 1)
        cv2.imshow('camera', img)
        k = cv2.waitKey(10)
        if k == 27:
            break
    cam.release()
    cv2.destroyAllWindows()


def say(engine,str):
    engine.say(str)
    engine.runAndWait()

def admission():  #录入信息模块
    #names = {"yumengzhen":0,"dujuanjuan":1,"litingting":2}
    say(engine, "请输入您的学号           ")
    StudentID = input("请输入学号：")
    #  读取数据库信息表 取出Name 对应ID
    ID=connect.readIDbaseStudentID(StudentID)  #connect 传入name  学生信息表找到 返回 ID
    if ID==-1:#没有找到该学生插入学生信息
        while True:
            say(engine,"没有找到该学生信息 输人  0 注册  1重新输入")
            op=input("\n  没有找到该学生信息  输人数字 0 注册学生信息  1重新输入")
            if op=='0':
                Name,studentID,Sex=input("输入学生信息： Name studentID Sex").split()
                connect.insert(Name,studentID,Sex) #插入学生信息信息
            else:
                StudentID = input("请输入学号：")
            ID=connect.readIDbaseStudentID(StudentID)  #connect 传入name  学生信息表找到 返回 ID
            if ID!=-1 :
                break
    say(engine, "正在打开摄像头")
    cam = cv2.VideoCapture(0)
    say(engine, "注视摄像头，开始采集人脸数据")
    getFace(cam, ID)  # 实际传入的是id
    cam.release()


if __name__ == '__main__':
    names = {"yumengzhen":0,"dujuanjuan":1,"litingting":    2}
    password="123456" #密码
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 20)
    flag=makeDir(engine)
    #trainFace()
    while True:
        if flag==1 :
            flag = 0
            say(engine, "首次使用 没有人脸信息 ")
            say(engine, "是否要录入新的人脸信息      ")
            say(engine, "输入0 代表是 输入其他表示退出")
            value = input("0：是 or other：否")
            if value=='0':
                while True:
                    admission()
                    say(engine, "是否要继续录入新的人脸信息      ")
                    say(engine, "输入0 代表是 输入其他表示退出")
                    firstflag = input("0：是    其他：退出")
                    if firstflag != '0':
                        break
                say(engine, "采集完毕，开始训练")
                trainFace()
                say(engine, "训练完毕          ")

        #say(engine, "请选择登录方式    ")
        say(engine, "输入 0管理人员模式       1 进入签到/签退模式     2 退出学生签到系统 ")
        user=input("\n0:管理人员模式       1:进入签到/签退模式    2:退出学生签到系统\n")

        if user=='0':
            say(engine, "输入管理员密码    ")
            pd=input("\n输入管理员密码 :\n")
            count=1
            while True:
                if count==3:
                    say(engine," 输入密码错误超过3次 强制退出输入     ")
                    break

                if password == pd:
                    say(engine, "管理员模式    ")
                    #say(engine, "输入数字 0 导出签到表     1 导出个人签到表     2 导出时长表       3 导出信息表       4 录入人脸信息   5 退出")
                    op = input("\n0:导出所有同学签到表    1:导出个人签到表  2:导出所有人员时长表   3:导出学生信息表 4 录入人脸信息   5 退出\n")
                    if op == '0':
                        baseConnect.sign()#导出签到表
                        say(engine, "导出签到表成功    ")
                        print( " 导出签到表成功   " )
                        pass
                    elif op == '1':
                        say(engine,"输入导出学生的学号")
                        StudentID=input("输入导出学生的学号")
                        ID=connect.readIDbaseStudentID(StudentID)
                        if  ID==-1:
                            say(engine, "没有该学生信息  ")
                            print( "没有该学生信息  ")
                        else:
                            baseConnect.peoson_sign(StudentID)#导出个人签到表
                            Name =connect.readName(ID)  #connect 传入ID  学生信息表找到 返回 name
                            say(engine, "导出  "+Name+"   信息成功")
                            print( "导出  "+Name+"   信息成功")

                    elif op == '2':
                        baseConnect.total_time()#导出时长表
                        say(engine,"导出时长表成功     ")
                        print( "导出时长表成功     ")
                    elif op == '3':
                        #导出学生信息表
                        connect.find_student_all()
                        print("导出学生信息成功     ")
                    elif op == '4':
                        while True:
                            admission()
                            say(engine, "是否要继续录入新的人脸信息      ")
                            say(engine, "输入0 代表是 输入其他表示退出")
                            secondflag = input("0：是    其他：退出")
                            if secondflag != '0':
                                break
                        say(engine, "采集完毕，开始训练")
                        trainFace()
                        say(engine, "训练完毕          ")
                    elif op == '5':
                        say(engine, "已退出 管理员模式    ")
                        break
                    else:
                        say(engine, "输入形式错误  请重新输入      ")
                else:
                    say(engine, "输入密码错误     请重新输入 ")
                    pd = input("\n输入管理员密码 :\n")
                    count += 1;

        elif user=='1':
            say(engine, "欢迎进入学生系统签到/签退模式      ")
            sign_flag=0;
            while True:
                say(engine, "输入数字 0 签到     1 签退")
                sign_flag = input("\n0: 签到     1 签退\n")
                if sign_flag=='1' or sign_flag=='0' :
                    break
                else :
                    say(engine,"    请输入正确的输入形式")
            say(engine, "开始人脸识别")
            say(engine, "正在打开摄像头")
            cam = cv2.VideoCapture(0)
            checkFace(cam, names, engine,sign_flag)

        elif user=='2':
            say(engine, "信息已保存")
            say(engine, "再见")
            sys.exit(0)
        else:
            say(engine, "输入错误请重新输入      ")



