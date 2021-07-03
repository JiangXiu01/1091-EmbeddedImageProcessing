#!/usr/bin/pytohn
# -*- coding: UTF-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
import threading
import os
import time
import shutil
from tkinter import messagebox
import parameter
import VideoCapture
import VideoFaceReco

class SampleApplication(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self) #self =>指向class
        self._frame = None
        #----------版面配置---------- #初始版面大小
        self.winfo_toplevel().title("智慧型門鎖系統")
        self.geometry('800x600')
        self.resizable(0,0) #鎖定大小
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class): #傳入新的頁面funtion
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy() #破壞舊框架DK3
        self._frame = new_frame
        self._frame.pack() #將該funtion 放入框架


class StartPage(tk.Frame): #首頁
    def EXIT():
        thread = threading.Thread(target = EXIT())
        thread.daemon = 1
        thread.start()
        self.quit

    def __init__(self, master): #master對於Frame來說, 可以說是他的子控制元件
        tk.Frame.__init__(self, master)
        #框架
        TitleFrame = tk.Frame(self, bg='gray80', height=60, width=800).grid(row=0,column=0, sticky = tk.N)
        StartPageFrame1 = tk.Frame(self, bg='gray80', height=175, width=800).grid(row=1,column=0, sticky = tk.N)
        StartPageFrame2 = tk.Frame(self, bg='gray80', height=100, width=800).grid(row=2,column=0, sticky = tk.N)
        StartPageFrame3 = tk.Frame(self, bg='gray80', height=30, width=800).grid(row=3,column=0, sticky = tk.N)
        StartPageFrame4 = tk.Frame(self, bg='gray80', height=235, width=800).grid(row=4,column=0, sticky = tk.N)

        #TitleLabel
        TitelLabel = tk.Label(self, bg = 'gray80', text = '選單頁面', font = ('微軟正黑體', 28))
        TitelLabel.grid(row=0,column=0, sticky=tk.N + tk.E + tk.S + tk.W)


        #辨識模式
        DetectionButton = tk.Button(self, text='辨識模式', font=('微軟正黑體', 20), command = lambda : master.switch_frame(RecognitionMode))
        DetectionButton.grid(ipadx=30,ipady=7,row=2,column=0, padx=160, sticky=tk.N + tk.E)# padx=160, pady=200,

        #使用者登錄
        LearningButton = tk.Button(self, text='登錄模式', font=('微軟正黑體', 20),  command = lambda : master.switch_frame(UserLogin))
        LearningButton.grid(ipadx=30,ipady=7, row=2,column=0, padx=160, sticky=tk.N + tk.W)

        #結束
        ExitButton = tk.Button(self, text='結束', font=('微軟正黑體', 20), command = self.quit)
        ExitButton.grid(row=4,column=0, padx=60, sticky=tk.E)


class UserLogin(tk.Frame): #UserLogin
    def Cancel(self, master):
        if(parameter.RecoCap.isOpened()): parameter.RecoCap.release()
        print('delete: ', './Sample/' + str(self.InputUserName.get()) + '/')
        if(os.path.isdir('./Sample/' + str(self.InputUserName.get()))):
            shutil.rmtree('./Sample/' + str(self.InputUserName.get()))
        time.sleep(1)
        master.switch_frame(StartPage)


    def GetCSV(self, master):
        if(parameter.RecoCap.isOpened()): parameter.RecoCap.release()
        thread = threading.Thread(target = VideoCapture.FacialFeatureCollection())
        thread.daemon = 1
        thread.start()
        master.switch_frame(StartPage)

    def GetUsername(self, master):
        print('UserName=> ', str(self.InputUserName.get()))
        UserSampleFolder = './Sample/' + str(self.InputUserName.get())
        print(str(self.InputUserName.get()))
        if (str(self.InputUserName.get()) == ''):
            tk.messagebox.showwarning('提示訊息', '請輸入使用者名稱')
            print('請輸入使用者名稱')
        else:
            if not (os.path.exists(UserSampleFolder)):
                os.makedirs(UserSampleFolder)
                #Video Label
                self.VideoLabel = tk.Label(self)
                self.VideoLabel.grid(row=1, column=0, sticky=tk.N)
                #執行
                thread = threading.Thread(target = VideoCapture.Capture, args = (self.VideoLabel, str(self.InputUserName.get()),))
                thread.daemon = 1
                thread.start()
            else:
                #照片 Label
                self.VideoLabel = tk.Label(self)
                self.VideoLabel.grid(row=1, column=0, sticky=tk.N)
                #執行機器學習模組
                thread = threading.Thread(target = VideoCapture.Capture, args = (self.VideoLabel, str(self.InputUserName.get()),))
                thread.daemon = 1
                thread.start()


    def __init__(self, master): #master對於Frame來說, 可以說是他的子控制元件
        tk.Frame.__init__(self, master)
        #框架
        TitleFrame = tk.Frame(self, bg='gray80', height=60, width=800).grid(row=0,column=0, sticky = tk.N)
        StartPageFrame1 = tk.Frame(self, bg='gray80', height=470, width=800).grid(row=1,column=0, sticky = tk.N)
        StartPageFrame2 = tk.Frame(self, bg='gray80', height=70, width=800).grid(row=2,column=0, sticky = tk.N)

        #TitleLabel
        TitelLabel = tk.Label(self, bg = 'gray80', text = '使用者設定', font = ('微軟正黑體', 28))
        TitelLabel.grid(row=0,column=0, sticky=tk.N + tk.E + tk.S + tk.W)


        #用戶名輸入
        InPutTypeLabel = tk.Label(self, bg = 'gray80', text = '用戶名', font = ('微軟正黑體', 16))
        InPutTypeLabel.grid(row=2,column=0, padx=40, pady=15, sticky=tk.N + tk.W)
        self.InputUserName = tk.StringVar(self)
        MLModelNameEntry = tk.Entry(self, textvariable = self.InputUserName)
        MLModelNameEntry.grid(row=2, column=0, ipadx=40, ipady=10, padx=120, pady=10, sticky = tk.N + tk.W)

        #登錄
        LoginButton = tk.Button(self, text='登錄', font=('微軟正黑體', 14), command = lambda : UserLogin.GetUsername(self, master))
        LoginButton.grid(row=2, column=0, ipadx=10, ipady=2, padx=360, pady=4, sticky=tk.N + tk.E) ##tk.W=左對齊, tk.E=右對齊, tk.N=上對齊, tk.S=下對齊

        #下一位
        ContinuanceButton = tk.Button(self, text='下一位', font=('微軟正黑體', 14), command = lambda : master.switch_frame(UserLogin))
        ContinuanceButton.grid(row=2, column=0, ipadx=10, ipady=2, padx=260, pady=4, sticky=tk.N + tk.E)

        #完成
        OKButton = tk.Button(self, text='完成', font=('微軟正黑體', 14), command = lambda : UserLogin.GetCSV(self, master))
        OKButton.grid(row=2, column=0, ipadx=10, ipady=2, padx=180, pady=4, sticky=tk.N + tk.E)

        #取消
        CancelButton = tk.Button(self, text='取消', font=('微軟正黑體', 14), command = lambda : UserLogin.Cancel(self, master))
        CancelButton.grid(row=2, column=0, ipadx=10, ipady=2, padx=20, pady=4, sticky=tk.N + tk.E)

class RecognitionMode(tk.Frame):
    def Cancel(self, master):
        #parameter.InterruptCamera = 1
        if(parameter.RecoCap.isOpened()): parameter.RecoCap.release()
        time.sleep(1)
        master.switch_frame(StartPage)

    def Recognition(self, master):
        self.VideoLabel = tk.Label(self)
        self.VideoLabel.grid(row=1, column=0, sticky=tk.N)
        thread = threading.Thread(target = VideoFaceReco.FaceCapture, args = (self.VideoLabel,))
        thread.daemon = 1
        thread.start()

    def __init__(self, master): #master對於Frame來說, 可以說是他的子控制元件
        tk.Frame.__init__(self, master)
        #框架
        TitleFrame = tk.Frame(self, bg='gray80', height=60, width=800).grid(row=0,column=0, sticky = tk.N)
        StartPageFrame1 = tk.Frame(self, bg='gray80', height=470, width=800).grid(row=1,column=0, sticky = tk.N)
        StartPageFrame2 = tk.Frame(self, bg='gray80', height=70, width=800).grid(row=2,column=0, sticky = tk.N)

        #TitleLabel
        TitelLabel = tk.Label(self, bg = 'gray80', text = '辨識模式', font = ('微軟正黑體', 28))
        TitelLabel.grid(row=0,column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        RecognitionMode.Recognition(self, master)

        #取消
        CancelButton = tk.Button(self, text='取消', font=('微軟正黑體', 14), command = lambda : RecognitionMode.Cancel(self, master))
        CancelButton.grid(row=2, column=0, ipadx=10, ipady=2, padx=20, pady=4, sticky=tk.N + tk.E)


if __name__ == "__main__":
    App = SampleApplication()
    App.mainloop()