#!/usr/bin/pytohn
# -*- coding: UTF-8 -*-
import dlib
import cv2
import numpy as np
import imutils
import math
import time
import os
import csv
import tkinter as tk
import sys
import parameter
import PIL
from PIL import ImageTk
from PIL import Image

detector = dlib.get_frontal_face_detector() #取得預設的臉部偵測器
predictor = dlib.shape_predictor('./Dlib_Model/shape_predictor_68_face_landmarks.dat') #根據shape_predictor方法載入68個特徵點模型，此方法為人臉表情識別的偵測器
face_rec_model_path = "./Dlib_Model/dlib_face_recognition_resnet_model_v1.dat" #128維向量嵌入模型

facerec = dlib.face_recognition_model_v1(face_rec_model_path)


def Capture(VideoLabel, InputUserName,):
    #parameter.InterruptCamera == 0
    parameter.RecoCap = cv2.VideoCapture(0)
    if not parameter.RecoCap.isOpened():
        print("Cannot open camera")
        exit()

    UPCount = 0
    DownCount = 0
    LeftCount = 0
    RightCount = 0
    MidCount = 0
    MidShoot = 0

    UPset = False
    Downset = False
    Leftset = False
    Rightset = False
    Midset = False

    Direction = 1

    while (parameter.RecoCap.isOpened()):
        ret, frame = parameter.RecoCap.read()
        ret, frame_blank = parameter.RecoCap.read()
        frame = cv2.flip(frame, 1) #影像水平反轉
        frame_blank = cv2.flip(frame_blank, 1) #影像水平反轉
        frame = imutils.resize(frame, height=460)
        frame_blank = imutils.resize(frame, height=460)
        #size = frame.shape #==>(460, 613, 3) 213
        #print(size)
        cv2.rectangle(frame, (166, 90), (447, 370), (0, 0, 255), 2, cv2.LINE_AA) #ROI方框
        cv2.circle(frame, (306, 230), 3, (0, 0, 255), 4) #中間點
        cv2.putText(frame, str('(166, 90)'), (166, 90), cv2.FONT_HERSHEY_DUPLEX, 0.5, ( 255, 255, 255), 1, cv2. LINE_AA)
        cv2.putText(frame, str('(166, 370)'), (166, 370), cv2.FONT_HERSHEY_DUPLEX, 0.5, ( 255, 255, 255), 1, cv2. LINE_AA)
        cv2.putText(frame, str('(166, 370)'), (447, 370), cv2.FONT_HERSHEY_DUPLEX, 0.5, ( 255, 255, 255), 1, cv2. LINE_AA)
        cv2.putText(frame, str('((166, 90)'), (447, 90), cv2.FONT_HERSHEY_DUPLEX, 0.5, ( 255, 255, 255), 1, cv2. LINE_AA)

        if (ret == True):
            #face_rects, scores, idx = detector.run(frame, 0)#偵測人臉
            face_rects = detector(frame, 0)#偵測人臉
            #print('face_rects=> ' , len(face_rects))
            
            for i, d in enumerate(face_rects):
                x1 = d.left()
                y1 = d.top()
                x2 = d.right()
                y2 = d.bottom()
                #text = " %2.2f ( %d )" % (scores[i], idx[i])
                #print('x1=> ', x1, '  y1=> ', y1, '  x2=> ', x2, '  y2=> ', y2)
                if(156 < x1 and x2 < 457 and 80 < y1 and y2 < 380):
                    x1y1 = x1, y1
                    x2y2 = x2, y2
                    x1y2 = x1, y2
                    x2y1 = x2, y1
                    cv2.rectangle(frame, (x1, y1), (x2, y2), ( 0, 255, 0), 4, cv2.LINE_AA) #繪製出偵測人臉的矩形範圍
                    cv2.putText(frame, str(x1y1), (x1, y1), cv2.FONT_HERSHEY_DUPLEX, 0.5, ( 255, 255, 255), 1, cv2. LINE_AA) #左上
                    cv2.putText(frame, str(x1y2), (x1, y2), cv2.FONT_HERSHEY_DUPLEX, 0.5, ( 255, 255, 255), 1, cv2. LINE_AA) #左下
                    cv2.putText(frame, str(x2y2), (x2, y2), cv2.FONT_HERSHEY_DUPLEX, 0.5, ( 255, 255, 255), 1, cv2. LINE_AA) #右下
                    cv2.putText(frame, str(x2y1), (x2, y1), cv2.FONT_HERSHEY_DUPLEX, 0.5, ( 255, 255, 255), 1, cv2. LINE_AA) #右上
                #標上人臉偵測分數與人臉方向子偵測器編號
                #cv2.putText(frame, text, (x1, y1), cv2. FONT_HERSHEY_DUPLEX, 0.7, ( 255, 255, 255), 1, cv2. LINE_AA)
                #各參數依次是：照片/添加的文字/左上角坐標/字體/字體大小/顏色/字體粗細

                    landmarks_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #給68特徵點辨識取得一個轉換顏色的frame
                    shape = predictor(landmarks_frame, d)
                    for FaceKeyPoints in range(68):
                        #.circle(frame_blank,(shape.part(FaceKeyPoints).x,shape.part(FaceKeyPoints).y), 3,( 0, 0, 255), 2)
                        #cv2.putText(frame_blank, str(FaceKeyPoints),(shape.part(FaceKeyPoints).x,shape.part(FaceKeyPoints).y),cv2. FONT_HERSHEY_COMPLEX, 0.5,( 255, 0, 0), 1)
                        #print('FaceKeyPoints==> ', FaceKeyPoints)
                        '''
                        #27 左眉毛
                        cv2.circle(frame,(shape.part(21).x,shape.part(21).y), 3,( 0, 0, 255), 2)
                        cv2.putText(frame, str(21),(shape.part(21).x,shape.part(21).y),cv2. FONT_HERSHEY_COMPLEX, 0.5,( 255, 0, 0), 1)
                        #27 鼻子最上
                        cv2.circle(frame,(shape.part(27).x,shape.part(27).y), 3,( 0, 0, 255), 2)
                        cv2.putText(frame, str(27),(shape.part(27).x,shape.part(27).y),cv2. FONT_HERSHEY_COMPLEX, 0.5,( 255, 0, 0), 1)
                        #30 鼻子中間
                        cv2.circle(frame,(shape.part(30).x,shape.part(30).y), 3,( 0, 0, 255), 2)
                        cv2.putText(frame, str(30),(shape.part(30).x,shape.part(30).y),cv2. FONT_HERSHEY_COMPLEX, 0.5,( 255, 0, 0), 1)
                        #02 左臉
                        cv2.circle(frame,(shape.part(2).x,shape.part(2).y), 3,( 0, 0, 255), 2)
                        cv2.putText(frame, str(2),(shape.part(2).x,shape.part(30).y),cv2. FONT_HERSHEY_COMPLEX, 0.5,( 255, 0, 0), 1)
                        #print(str(2), '  ', shape.part(2).x,shape.part(2).y, '   ', str(30), '  ', shape.part(30).x,shape.part(30).y)
                        #14 左臉
                        cv2.circle(frame,(shape.part(14).x,shape.part(14).y), 3,( 0, 0, 255), 2)
                        cv2.putText(frame, str(14),(shape.part(14).x,shape.part(30).y),cv2. FONT_HERSHEY_COMPLEX, 0.5,( 255, 0, 0), 1)
                        #58 嘴下
                        cv2.circle(frame,(shape.part(58).x,shape.part(58).y), 3,( 0, 0, 255), 2)
                        cv2.putText(frame, str(58),(shape.part(58).x,shape.part(58).y),cv2. FONT_HERSHEY_COMPLEX, 0.5,( 255, 0, 0), 1)
                        #09 下巴
                        cv2.circle(frame,(shape.part(8).x,shape.part(8).y), 3,( 0, 0, 255), 2)
                        cv2.putText(frame, str(8),(shape.part(8).x,shape.part(8).y),cv2. FONT_HERSHEY_COMPLEX, 0.5,( 255, 0, 0), 1)
                        '''

                        if(Direction == 1):
                            print('看中間')
                            #中看判斷
                            LookMiddleX = 306 - shape.part(30).x
                            LookMiddley = 230 - shape.part(30).y
                            LookMiddle_distance = math.sqrt(LookMiddleX**2 + LookMiddley**2)
                            #print('distance=> ', LookMiddle_distance)
                            if(LookMiddle_distance <= 20):
                                cv2.putText(frame, 'Very good! Please wait to take pictures.', (170, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
                                print('中間')
                                MidCount += 1
                                print(MidCount)
                                if(MidCount >= 800 and Midset == False):
                                    time.sleep(2)
                                    cv2.imwrite('./Sample/' + InputUserName + '/' + InputUserName + '_Mid_' + str(MidShoot) + '.jpg', frame_blank)
                                    MidShoot += 1
                                    if (MidShoot >= 20): Midset = True
                                    Direction = 2
                            else:
                                cv2.putText(frame, 'Align your face in the middle.', (170, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)

                        if(Direction == 2):
                            print('看左邊')
                            #左看判斷
                            LookLeftX = shape.part(30).x - shape.part(2).x
                            LookLefty = shape.part(30).y - shape.part(2).y
                            LookLeft_distance = math.sqrt(LookLeftX**2 + LookLefty**2)
                            #print('distance=> ', LookLeft_distance , '中間x=> ', shape.part(30).x, '  左邊X=> ', shape.part(2).x)
                            if(LookLeft_distance <= 35):
                                cv2.putText(frame, 'Very good! Please wait to take pictures.', (170, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
                                print('左看')
                                LeftCount += 1
                                print(LeftCount)
                                if(LeftCount >= 1000 and Leftset == False):
                                    time.sleep(1)
                                    cv2.imwrite('./Sample/' + InputUserName + '/' + InputUserName + '_Left.jpg', frame_blank)
                                    Leftset = True
                                    Direction = 3
                            else:
                                cv2.putText(frame, 'Please look at the left.', (170, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)

                        if(Direction == 3):
                            print('看下')
                            #下看判斷
                            LookDownX = shape.part(58).x - shape.part(9).x
                            LookDowny = shape.part(58).y - shape.part(9).y
                            LookDown_distance = math.sqrt(LookDownX**2 + LookDowny**2)
                            #print('distance=> ', LookDown_distance , '下巴=> y= ', shape.part(9).y, '  嘴下 y= ', shape.part(58).y)
                            if(LookDown_distance <= 35):
                                cv2.putText(frame, 'Very good! Please wait to take pictures.', (170, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
                                print('下看')
                                DownCount += 1
                                print(DownCount)
                                if(DownCount >= 1000 and Downset == False):
                                    time.sleep(1)
                                    cv2.imwrite('./Sample/' + InputUserName + '/' + InputUserName + '_Down.jpg', frame_blank)
                                    Downset = True
                                    Direction = 4
                            else:
                                cv2.putText(frame, 'Please look at the below.', (170, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)

                        if(Direction == 4):
                            print('看右邊')
                            #右看判斷
                            LookRightX = shape.part(14).x - shape.part(30).x
                            LookRighty = shape.part(14).y - shape.part(30).y
                            LookRight_distance = math.sqrt(LookRightX**2 + LookRighty**2)
                            #print('distance=> ', LookRight_distance , '中間x=> ', shape.part(30).x, '  左邊X=> ', shape.part(14).x)
                            if(LookRight_distance <= 35):
                                cv2.putText(frame, 'Very good! Please wait to take pictures.', (170, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
                                print('右看')
                                RightCount += 1
                                print(RightCount)
                                if(RightCount >= 1000 and Rightset == False):
                                    time.sleep(1)
                                    cv2.imwrite('./Sample/' + InputUserName + '/' + InputUserName + '_Right.jpg', frame_blank)
                                    Rightset = True
                                    Direction = 5
                            else:
                                cv2.putText(frame, 'Please look at the right.', (170, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)

                        if(Direction == 5):
                            print('看上')
                            #上看判斷
                            LookUPX = shape.part(21).x - shape.part(27).x
                            LookUPy = shape.part(21).y - shape.part(27).y
                            LookUP_distance = math.sqrt(LookUPX**2 + LookUPy**2)
                            #print('distance=> ', LookUP_distance , '鼻上y=> ', shape.part(21).y, '  左眉y=> ', shape.part(27).y)
                            if(LookUP_distance <= 18):
                                cv2.putText(frame, 'Very good! Please wait to take pictures.', (170, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
                                print('上看')
                                UPCount += 1
                                print(UPCount)
                                if(UPCount >= 1000 and UPset == False):
                                    time.sleep(1)
                                    cv2.imwrite('./Sample/' + InputUserName + '/' + InputUserName + '_UP.jpg', frame_blank)
                                    UPset = True
                                    Direction = 6
                            else:
                                cv2.putText(frame, 'Please look at the above.', (170, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)

                        #if(UPset == True and Downset == True and Rightset == True and Midset == True):
                            #KeyPointDetection(InputUserName)
                            #break;
            frameTK = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frameTK = ImageTk.PhotoImage(image = PIL.Image.fromarray(frameTK))
            VideoLabel.config(image = frameTK)
            VideoLabel.image = frameTK
        else:
            break
    #parameter.InterruptCamera = 0
    parameter.RecoCap.release()
    cv2.destroyAllWindows()

def Return_128d_features(path_img):
    img_rd = cv2.imread(path_img)
    faces = detector(img_rd, 1)

    # 因為有可能截下來的人臉再去檢測，檢測不出來人臉了, 所以要確保是 檢測到人臉的人臉圖像拿去算特徵
    if len(faces) != 0:
        shape = predictor(img_rd, faces[0])
        face_descriptor = facerec.compute_face_descriptor(img_rd, shape)
    else:
        face_descriptor = 0
    return face_descriptor

# 返回 personX 的 128D 特徵均值
# Input: path_face_personX <class 'str'>
# Output: features_mean_personX <class 'numpy.ndarray'>
def Return_features_mean_personX(path_face_personX):
    features_list_personX = []
    photos_list = os.listdir(path_face_personX)
    if photos_list:
        for i in range(len(photos_list)):
            # 調用 Return_128d_features() 得到 128D 特徵
            features_128d = Return_128d_features(path_face_personX + "/" + photos_list[i])
            # 遇到沒有檢測出人臉的圖片跳過
            if features_128d == 0:
                i += 1
            else:
                features_list_personX.append(features_128d)

    # 計算 128D 特徵的均值
    # personX 的 N 張圖像 x 128D -> 1 x 128D
    if features_list_personX:
        features_mean_personX = np.array(features_list_personX).mean(axis=0)
        print(features_mean_personX)
    else:
        features_mean_personX = np.zeros(128, dtype=int, order='C')

    return features_mean_personX

def FacialFeatureCollection():
    Person_Feature_Directory_List = os.listdir("./Sample/")
    Count = 0
    PersonDirectory = []
    for Person in Person_Feature_Directory_List: #掃描特徵目錄
        if not Person[-4:] in ['.csv']:
            print("./Sample/" + Person)
            PersonDirectory.append(Person)
            Count += 1
    print(PersonDirectory[0])
    
    with open("Sample/FacialFeatures_ALL.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        features_mean_personX = Return_features_mean_personX("./Sample/" + PersonDirectory[0] + "/")
        writer.writerow(features_mean_personX)
        for PersonName in PersonDirectory:
            print("./Sample/" + PersonName + "/")
            features_mean_personX = Return_features_mean_personX("./Sample/" + PersonName + "/")
            writer.writerow(features_mean_personX)
    return "OK"

if __name__ == '__main__':
    FacialFeatureCollection()