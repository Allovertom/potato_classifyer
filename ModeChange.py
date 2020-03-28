# mode change class
import tkinter as tk
from picamera import PiCamera
from time import sleep
import datetime

class MChange:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (64,64)
    def text_print(self, tex):
        self.txt.delete(0,tk.END)
        self.txt.insert(tk.END,tex)
        print(tex)
        
    def take_pics(self, save_f = 0):
        dt_now = datetime.datetime.now().strftime('%Y_%m_%d_%H:%M:%S')
        path = "/home/pi/ドキュメント/potato_classfier/train/"
        tex = "しゃしんはほぞんされました。"
        if save_f == 0:#test
            path = path + "%s.jpg"
            tex = "trainフォルダに" + tex
        elif save_f == 1:#OK
            path = path + "/0_A/%s.jpg"
            tex = "A品フォルダに" + tex
        elif save_f == 2:#NG
            path = path + "/1_B/%s.jpg"
            tex = "B品フォルダに" + tex
        elif save_f == 3:#NoObject
            path = path + "/2_NoPotato/%s.jpg"
            tex = "芋なしフォルダに" + tex
        else:
            print("please set the number either 0 to 3.")
        self.camera.start_preview(fullscreen=False, window=(0, 0, 500, 500))
        sleep(1.7)
        try:
            self.camera.capture(path % dt_now)
        finally:
            self.camera.stop_preview()
        self.text_print(tex)
    def take_pics_A(self):
        self.take_pics(1)
    def take_pics_B(self):
        self.take_pics(2)
    def take_pict_No(self):
        self.take_pics(3)
    def learning(self):
        print("がくしゅう中")
    def select_mode(self):
        # ウィンドウを生成してそのウィンドウを操作するための値をrootに代入します。
        root = tk.Tk()
        # ウィンドウ名を指定します
        root.title('選択')
        # ウィンドウサイズを指定します。('x'は、小文字のエックスです。)
        root.geometry('400x400')
        
        #テキストボックスの定義
        self.txt = tk.Entry(width=50)
        self.txt.place(x=5, y=350)
        
        #保存先フォルダ
        #self.Path = '/home/pi/ドキュメント/potato_classfier/train'

        #ボタンの定義
        btnA = tk.Button(root,text="ためしどり", command=self.take_pics, width=12, height=3)
        btnB = tk.Button(root,text="A品さつえい", command=self.take_pics_A, width=12, height=3)
        btnC = tk.Button(root,text="B品さつえい", command=self.take_pics_B, width=12, height=3)
        btnD = tk.Button(root,text="何もないさつえい", command=self.take_pict_No, width=12, height=3)
        btnE = tk.Button(root,text="がくしゅう", command=self.learning, width=12, height=3)
        
        #ボタンの並びを定義
        btnA.grid(row=0, column=1)
        btnB.grid(row=1, column=1)
        btnC.grid(row=2, column=1)
        btnD.grid(row=3, column=1)
        btnE.grid(row=4, column=1)

        # ウィンドウを表示して制御するためのループに入ります。
        root.mainloop()

        

