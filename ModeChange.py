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
import os

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
    def learning(self, MName = "model.pickle" ):
        self.text_print("がくしゅう中。")
        #dt_now = datetime.datetime.now().strftime('%Y_%m_%d_%H:%M:%S')
        #MName = "model_" + dt_now + ".pickle"
        
        Path = '/home/pi/ドキュメント/potato_classfier/train/'
        pix = 64*64
        
        #make all jpg file list in the folder.フォルダ内jpgファイルリスト作成
        OK_L = glob.glob(Path + '0_A/*.jpg')
        NG_L = glob.glob(Path + '1_B/*.jpg')
        NoP_L = glob.glob(Path + '2_NoPotato/*.jpg')

        #X: one dimention white-black pixcel date, Y: teacher label.
        #X:一次元化された、ピクセル毎の階調データ。Y:正解ラベル。
        X_OK = self.Preprocess(OK_L)
        Y_OK = np.zeros(int(len(X_OK)/pix))#make teach data 0
        X_NG = self.Preprocess(NG_L)
        Y_NG = np.ones(int(len(X_NG)/pix))#make teach data 1
        X_NO = self.Preprocess(NoP_L)
        Y_NO = np.full(int(len(X_NO)/pix),2)#make teach data 2
        self.text_print("がくしゅう中。。")
        
        X = np.r_[X_OK, X_NG, X_NO]#concatinate all preprocessed pics.全前処理写真結合
        X = X.reshape([int(len(X)/pix),pix])#make array.行列化
        y = np.r_[Y_OK, Y_NG, Y_NO]#teacher label addition.正解ラベル付加
        
        #train test split.学習とテストセットに分割
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
        self.text_print("がくしゅう中。。。")

        clf = svm.SVC(kernel='linear')#introduce SVM classifier.SVMのオブジェクト化。
        clf.fit(X_train, y_train)#fitting. 学習。
        self.text_print("がくしゅうかんりょう。")

        pre = clf.predict(X_test)#テストデータで確認    
        ac_score = metrics.accuracy_score(y_test, pre)
        ac_score = round(ac_score*100, 1)
        self.text_print(MName + "のせいかいりつは"+str(ac_score)+"です。")#print score.精度表示       
        with open(MName, mode='wb') as fp:
            pickle.dump(clf, fp)#save model.モデル出力
    def Preprocess(self, files):
        size = [64, 64]
        array = np.empty([size[0]*size[1],0],int)
        for i, file in enumerate(files):
            img = Image.open(file).convert('L')#colored to white-black pic.白黒化。
            img = img.resize(size, Image.ANTIALIAS)
            #print(img.format, img.size, img.mode,img.getextrema())
            img_arr = np.asarray(img)
            array = np.append(array,img_arr.ravel())#one dimentionize.一次元化。
            #print(array.shape)
        return array
    def remove_f(self, path, recursive=True):
        for p in glob.glob(path, recursive=recursive):
            if os.path.isfile(p):
                os.remove(p)
    
    def judge(self, ModelFullName="model.pickle"):
        PickleName = ModelFullName#indicate trained model(pickle)
        FullPath = ['/home/pi/ドキュメント/potato_classfier/predict/1.jpg']
        #delete all jpg files in predict folder. predictフォルダ内のjpgファイル削除。
        del_files_path = '/home/pi/ドキュメント/potato_classfier/predict/*.jpg'
        self.remove_f(del_files_path)
        #print(FullPath)
        with open(PickleName, mode='rb') as fp:
            clf = pickle.load(fp)
        try:
            while True:
                #Take a pic and save to the predict folder.写真取ってpredictフォルダに保存
                self.camera.capture('/home/pi/ドキュメント/potato_classfier/predict/1.jpg')
                #preprocessing at indicated folder.指定フォルダの写真を前処理
                X_pred = self.Preprocess(FullPath)
                #predict 推定
                pred = clf.predict(X_pred)
                if pred[0] == 0:#OK
                    self.text_print("A品です。")
                    sleep(0.1) 
                elif pred[0] == 1:#NG
                    self.text_print("B品です。")
                    sleep(0.1)
                elif pred[0] == 2:#No Potato
                    self.text_print("いもがみつかりません。")
                    sleep(0.1)
                os.remove(FullPath[0])#remove the pic.判定した写真を削除。

        except KeyboardInterrupt:
            pass

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
        btnF = tk.Button(root,text="はんていする", command=self.judge, width=12, height=3)
        btnG = tk.Button(root,text="おわる", command=self.closeApp, width=12, height=3)
        
        
        #ボタンの並びを定義
        btnA.grid(row=0, column=1)
        btnB.grid(row=1, column=1)
        btnC.grid(row=2, column=1)
        btnD.grid(row=3, column=1)
        btnE.grid(row=4, column=1)
        btnF.grid(row=1, column=2)
        btnG.grid(row=4, column=2)



        # ウィンドウを表示して制御するためのループに入ります。
        root.mainloop()

        

