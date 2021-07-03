#!/usr/bin/pytohn
# -*- coding: UTF-8 -*-
global face_feature_known_list #存放註冊過的人臉特徵
face_feature_known_list = []

global face_name_known_list #存放註冊過的人臉名子
face_name_known_list = []

global current_frame_face_feature_list #存放當前人臉128D Feature
current_frame_face_feature_list = []

global current_frame_face_name_list #當前人臉名子
current_frame_face_name_list = []

global current_frame_face_name_position_list #存放當前人臉框框要顯示名子的座標位置
current_frame_face_name_position_list = []

global InterruptCamera
InterruptCamera = 0 #0=> Normal, 1=> Interrupt

global RecoCap
