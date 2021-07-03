#!/usr/bin/pytohn
# -*- coding: UTF-8 -*-
import dlib
import numpy as np
import cv2
import imutils
import pandas as pd
import os
import time
import logging
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
import PIL
import PIL.Image
from PIL import ImageTk
import math
import parameter

detector = dlib.get_frontal_face_detector() #Dlib人臉檢測器
predictor = dlib.shape_predictor('Dlib_Model/shape_predictor_68_face_landmarks.dat') #人臉landmark特徵點檢測器
face_reco_model = dlib.face_recognition_model_v1("Dlib_Model/dlib_face_recognition_resnet_model_v1.dat")#人臉識別模型，提取 128D 的特徵

def FacialFeatureReader():
    if os.path.exists("./Sample/FacialFeatures_ALL.csv"):
        csv_read = pd.read_csv("./Sample/FacialFeatures_ALL.csv")
        print(csv_read.shape[0])
        for i in range(csv_read.shape[0]): #逐列讀取
            features_someone_arr = []
            print('===', i)
            for j in range(0, 128): #逐行讀取
                if csv_read.iloc[i][j] == '': #若特徵值為空
                    features_someone_arr.append('0')
                else:
                    features_someone_arr.append(csv_read.iloc[i][j])
                    print(csv_read.iloc[i][j])
            parameter.face_feature_known_list.append(features_someone_arr)
            parameter.face_name_known_list.append("Person_"+str(i+1))
        return 1
    else:
        print("'FacialFeatures_ALL.csv' not found!")
        return 0

def return_euclidean_distance(feature_1, feature_2):
    feature_1 = np.array(feature_1)
    feature_2 = np.array(feature_2)
    dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
    return dist



def FaceCapture(VideoLabel,):
    FacialFeatureReader() #載入人臉資料
    RangeCount = 0 #人臉到定位delay計數
    SuccessCount = 0 #辨識成功delay計數
    Failure = 0 #辨識失敗次數
    FailureCount = 0 #辨識失敗封鎖計數
    IdentificationStatus = False #辨識次數
    
    parameter.RecoCap = cv2.VideoCapture(0)
    if not parameter.RecoCap.isOpened():
        print("Cannot open camera")
        exit()

    while (parameter.RecoCap.isOpened()):
        ret, frame = parameter.RecoCap.read()
        frame = cv2.flip(frame, 1) #影像水平反轉
        frame = imutils.resize(frame, height=460)
        frame_blank = imutils.resize(frame, height=460)
        #size = frame.shape #==>(460, 613, 3) 213
        #print(size)
        if(IdentificationStatus == False): cv2.rectangle(frame, (166, 90), (447, 370), (0, 0, 255), 1, cv2.LINE_AA) #ROI方框
        if(IdentificationStatus == True): cv2.rectangle(frame, (166, 90), (447, 370), (0, 255, 0), 1, cv2.LINE_AA) #ROI方框
        cv2.circle(frame, (306, 230), 3, (0, 0, 255), 2) #中間點
        #cv2.putText(frame, str('(166, 90)'), (166, 90), cv2.FONT_HERSHEY_DUPLEX, 0.5, ( 255, 255, 255), 1, cv2. LINE_AA)
        #cv2.putText(frame, str('(166, 370)'), (166, 370), cv2.FONT_HERSHEY_DUPLEX, 0.5, ( 255, 255, 255), 1, cv2. LINE_AA)
        #cv2.putText(frame, str('(166, 370)'), (447, 370), cv2.FONT_HERSHEY_DUPLEX, 0.5, ( 255, 255, 255), 1, cv2. LINE_AA)
        #cv2.putText(frame, str('((166, 90)'), (447, 90), cv2.FONT_HERSHEY_DUPLEX, 0.5, ( 255, 255, 255), 1, cv2. LINE_AA)
        
        parameter.current_frame_face_feature_list = [] #存放當前人臉128D Feature
        parameter.current_frame_face_name_list = [] #當前人臉名子
        parameter.current_frame_face_name_position_list = [] #存放當前人臉框框要顯示名子的座標位置
        
        if (ret == True):
            face_rects = detector(frame, 0)#偵測人臉
            for i, d in enumerate(face_rects):
                x1 = d.left()
                y1 = d.top()
                x2 = d.right()
                y2 = d.bottom()
                
                if(156 < x1 and x2 < 457 and 80 < y1 and y2 < 380 and IdentificationStatus == False and FailureCount < 6):
                    landmarks_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #給68特徵點辨識取得一個轉換顏色的frame
                    shape = predictor(landmarks_frame, d)
                    cv2.putText(frame, 'Face recognition...', (170, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
                    RangeCount += 1
                    print('RangeCount=> ', RangeCount)
                    if(RangeCount >= 20):
                        if(KeyPointComparison(frame, face_rects) == True):
                            print('識別成功!!')
                            IdentificationStatus = True
                        else:
                            FailureCount += 1 #失敗計數
                            print('失敗計數=> ', FailureCount)
                        
                        RangeCount = 0
                #elif(IdentificationStatus == False):
                    #cv2.putText(frame, 'Please move your face to the red area.', (170, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
                
            if(IdentificationStatus == True): #成功後delay一下再繼續辨識
                SuccessCount += 1
                print('SuccessCount=> ', SuccessCount)
                cv2.putText(frame, 'Recognition success.', (170, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
                if(SuccessCount >= 20):
                    IdentificationStatus = False
                    SuccessCount = 0
            if(FailureCount >= 5): #失敗五次
                cv2.putText(frame, 'You have reached the error limit!', (170, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                FailureCount += 1
                print('FailureCount==> ', FailureCount)
                if(FailureCount >= 150):
                    print('FailureCount==> ', FailureCount)
                    FailureCount = 0
            
            frameTK = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frameTK = ImageTk.PhotoImage(image = PIL.Image.fromarray(frameTK))
            VideoLabel.config(image = frameTK)
            VideoLabel.image = frameTK
        else:
            break
    parameter.RecoCap.release()
    cv2.destroyAllWindows()
            

def KeyPointComparison(frame, face_rects):
    Result = False
    #獲取當前捕獲到的圖像的所有人臉的特徵
    for i in range(len(face_rects)):
        shape = predictor(frame, face_rects[i])
        parameter.current_frame_face_feature_list.append(face_reco_model.compute_face_descriptor(frame, shape)) #Get當前人臉128D feature

    #遍歷捕獲到的圖像中所有的人臉
    for k in range(len(face_rects)):
        parameter.current_frame_face_name_list.append("unknown")
        parameter.current_frame_face_name_position_list.append(tuple([face_rects[k].left(), int(face_rects[k].bottom() + (face_rects[k].bottom() - face_rects[k].top()) / 4)]))

        #對於某張人臉，遍歷所有存儲的人臉特徵
        current_frame_e_distance_list = []
        for i in range(len(parameter.face_feature_known_list)):
            # 如果 person_X 數據不為空
            if str(parameter.face_feature_known_list[i][0]) != '0.0':
                e_distance_tmp = return_euclidean_distance(parameter.current_frame_face_feature_list[k], parameter.face_feature_known_list[i])
                current_frame_e_distance_list.append(e_distance_tmp)
            else:
                #空數據 person_X
                current_frame_e_distance_list.append(999999999)
        #尋找出最小的歐式距離匹配
        similar_person_num = current_frame_e_distance_list.index(min(current_frame_e_distance_list))
        
        if min(current_frame_e_distance_list) < 0.4:
            parameter.current_frame_face_name_list[k] = parameter.face_name_known_list[similar_person_num]
            print('正確')
            Result = True
        else:
            print('失敗')
            Result = False
            
        for kk, d in enumerate(face_rects):
            #繪製矩形框
            cv2.rectangle(frame, tuple([d.left(), d.top()]), tuple([d.right(), d.bottom()]), (0, 255, 255), 2)
    return Result

if __name__ == '__main__':
    FaceCapture()