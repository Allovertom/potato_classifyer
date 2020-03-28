# mode change class
import tkinter as tk
from picamera import PiCamera
from time import sleep
import datetime
from PIL import Image
import numpy as np
import glob
from sklearn import svm, metrics
from sklearn.model_selection import train_test_split
import pickle

class MChange:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (64,64)
        self.camera.start_preview(fullscreen=False, window=(0, 0, 500, 500))
        sleep(1.7)
        self.camera.stop_preview()
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
            tex = "いもなしフォルダに" + tex
        else:
            print("please set the number either 0 to 3.")
        self.camera.start_preview(fullscreen=False, window=(0, 0, 500, 500))
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
        self.text_print("がくしゅう中。")
        ModelName = "model.pickle"
        Path = '/home/pi/ドキュメント/potato_classfier/train/'
        pix = 64*64
        
        OK_L = glob.glob(Path + '0_A/*.jpg')
        NG_L = glob.glob(Path + '1_B/*.jpg')
        NoP_L = glob.glob(Path + '2_NoPotato/*.jpg')
        
        X_OK = self.Preprocess(OK_L)
        Y_OK = np.zeros(int(len(X_OK)/pix))#make teach data 0
        X_NG = self.Preprocess(NG_L)
        Y_NG = np.ones(int(len(X_NG)/pix))#make teach data 1
        X_NO = self.Preprocess(NoP_L)
        Y_NO = np.full(int(len(X_NO)/pix),2)#make teach data 2
        self.text_print("がくしゅう中。。")
        
        X = np.r_[X_OK, X_NG, X_NO]#concatinate all preprocessed pics.全前処理写真結合
        X = X.reshape([int(len(X)/pix),pix])#make array.行列化
        y = np.r_[Y_OK, Y_NG, Y_NO]#teacher data addition.教師データ付加
        print(X.shape)
        print(y.shape)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
        self.text_print("がくしゅう中。。。")

        clf = svm.SVC(kernel='linear')#introduce SVM classifier.SVMのオブジェクト化。
        clf.fit(X_train, y_train)
        self.text_print("がくしゅうかんりょう。")

        pre = clf.predict(X_test)    
        ac_score = metrics.accuracy_score(y_test, pre)
        self.text_print("せいかいりつは"+str(ac_score)+"です。")#print score.精度表示       
        with open(ModelName, mode='wb') as fp:
            pickle.dump(clf, fp)#save model.モデル出力
    def Preprocess(self, files):
        size = [64, 64]
        array = np.empty([size[0]*size[1],0],int)
        print(array.shape)
        print(files)
        for i, file in enumerate(files):
            img = Image.open(file).convert('L')
            img = img.resize(size, Image.ANTIALIAS)
            print(img.format, img.size, img.mode,img.getextrema())
            img_arr = np.asarray(img)
            print("OneDimention"+str(img_arr.ravel().shape))
            array = np.append(array,img_arr.ravel())
            print(array.shape)
        return array
 
    def closeApp(self):
        tex = "終了します"
        self.text_print(tex)
        self.camera.close()
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
        btnF = tk.Button(root,text="おわる", command=self.closeApp, width=12, height=3)
        
        #ボタンの並びを定義
        btnA.grid(row=0, column=1)
        btnB.grid(row=1, column=1)
        btnC.grid(row=2, column=1)
        btnD.grid(row=3, column=1)
        btnE.grid(row=4, column=1)
        btnF.grid(row=4, column=2)


        # ウィンドウを表示して制御するためのループに入ります。
        root.mainloop()

        

