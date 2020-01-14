#from picamera import PiCamera
from PIL import Image
import numpy as np
import glob
from sklearn import svm, metrics
from sklearn.model_selection import train_test_split
import pickle

ModelName = "model_1.pickle"#As you wish.


def main():
    Path = '/home/pi/ドキュメント/potato_classfier/train/'
    
    OK_L = glob.glob(Path + '0_OK/*.jpg')
    NG_L = glob.glob(Path + '1_NG/*.jpg')
    NoP_L = glob.glob(Path + '3_NoPotato/*.jpg')
    
    X_OK = Preprocess(OK_L)
    Y_OK = np.zeros(int(len(X_OK)/784))#make teach data
    X_NG = Preprocess(NG_L)
    Y_NG = np.ones(int(len(X_NG)/784))#make teach data
    X_NO = Preprocess(NoP_L)
    Y_NO = np.full(int(len(X_N0)/784),2)#make teach data
    
    
    X = np.r_[X_OK, X_NG, X_NO]#concatinate all preprocessed pics.全前処理写真結合
    X = X.reshape([int(len(X)/784),784])#make array.行列化
    y = np.r_[Y_OK, Y_NG]#teacher data addition.教師データ付加
    print(X.shape)
    print(y.shape)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    clf = svm.SVC(kernel='linear')
    clf.fit(X_train, y_train)
    pre = clf.predict(X_test)    
    ac_score = metrics.accuracy_score(y_test, pre)
    print(ac_score)#print score.精度表示

    with open(ModelName, mode='wb') as fp:
        pickle.dump(clf, fp)#save model.モデル出力


def Preprocess(files):
    size = [64, 64]
    array = np.empty([size[0]*size[1],0],int)
    print(array.shape)
    print(files)
    for i, file in enumerate(files):
        img = Image.open(file).convert('L')
        img = img.resize(size, Image.ANTIALIAS)
        print(img.format, img.size, img.mode,img.getextrema())
        img.save(file)
        img_arr = np.asarray(img)
        print("OneDimention"+str(img_arr.ravel().shape))
        array = np.append(array,img_arr.ravel())
        print(array.shape)
    return array
#
#def TakePics():s
#    camera = PiCamera()
#    camera.resolution = (64,64)
#    camera.capture('/home/pi/ドキュメント/potato_classfier/predict/%s.jpg' % i)
#    X_pred, img = Preprocess(i, 0)
#    #predictフォルダにあるファイルを前処理（白黒）
#    #trainフォルダに保存

if __name__ == '__main__':
#    main()
    #Path ='C:/Users/nari/Documents/03_ラズパイ/potato_classifyer/'
    
    #OK_L = glob.glob('0_OK/*.jpg')
    #X_OK = Preprocess(OK_L)
    OK_L = glob.glob('1_NG/*.jpg')
    X_OK = Preprocess(OK_L)


