# -*- coding: utf-8 -*-
from picamera import PiCamera
import RPi.GPIO as GPIO
from time import sleep
from PIL import Image
import numpy as np
import os
import glob
import pickle
import shutil
import random
    
    
    
def Preprocess(i,SaveP):
    size = [64, 64]
    array = np.empty([size[0]*size[1],0],int)
    print(array.shape)
    FullPath = glob.glob('/home/pi/ドキュメント/potato_classfier/predict/*.jpg')
    print(FullPath)
    #Preprocessing
    img = Image.open(FullPath[0]).convert('L')
    img = img.resize(size, Image.ANTIALIAS)
    print(img.format, img.size, img.mode,img.getextrema())
    #Make one dimention array
    img_arr = np.asarray(img)
    print("OneDimention"+str(img_arr.ravel().shape))
    if SaveP:
        os.remove(FullPath[0])
    else:#saving pics for re-training the model.再学習のために写真保存
        shutil.move(FullPath[0],'/home/pi/ドキュメント/potato_classfier/predict/done/%s.jpg' % i)
    return img_arr.ravel(), img


PickleName = "model_1.pickle"#indicate trained model(pickle)
SavePics = 0
with open(PickleName, mode='rb') as fp:
    clf = pickle.load(fp)

camera = PiCamera()
#camera.rotation = 180#if camera is upside down カメラが上下反対の場合
camera.resolution = (64,64)

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)#0:OK:Green
GPIO.setup(24, GPIO.OUT)#1:NG(NotGood):Red
GPIO.setup(23, GPIO.OUT)#2:NoPotato:Yellow

i = 0

try:
    while True:
        #Take a pic and save to indicated folder.写真取って指定フォルダに保存
        i += 1
        camera.capture('/home/pi/ドキュメント/potato_classfier/predict/%s.jpg' % i)
        #preprocessing at indicated folder.指定フォルダの写真を前処理
        X_pred, img = Preprocess(i, SavePics)
        #predict 推定
        pred = clf.predict(X_pred)
        #change duty ratio.デューティー比変更
        if pred[0] == 0:#OK
            print("Green: OK")
            GPIO.output(25, GPIO.HIGH)
            sleep(0.3) 
        elif pred[0] == 1:#NG
            print("Red: NG")
            GPIO.output(24, GPIO.HIGH)
            sleep(0.3)
        elif pred[0] == 2:#No Potato
            print("Yellow: No Potato")
            GPIO.output(23, GPIO.HIGH)
            sleep(0.3)

        GPIO.output(25, GPIO.LOW)
        GPIO.output(24, GPIO.LOW)
        GPIO.output(23, GPIO.LOW)
        #save preprocessed pic前処理後写真を保存
        if SavePics:
            pass
        else:#collect preprocessed pics with pred number.再学習用写真（推定値付き）保存
            rand = random.randint(0,100000)
            img.save('/home/pi/ドキュメント/potato_classfier/train/'
                     +str(i)+'_'+str(int(pred[0]))+
                     '_'+str(rand)+'.jpg')

except KeyboardInterrupt:
    pass
GPIO.cleanup()

