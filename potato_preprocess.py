#from picamera import PiCamera
from PIL import Image
import numpy as np
import glob
from sklearn import svm, metrics
from sklearn.model_selection import train_test_split
import pickle

ModelName = "model.pickle"#As you wish.

def main():
    Path = '/home/pi/ドキュメント/potato_classfier/train/'
    
    Reuse_L = glob.glob(Path + '0_reuse/*.jpg')
    S_L = glob.glob(Path + '1_S/*.jpg')
    M_L = glob.glob(Path + '2_M/*.jpg')
    L_L = glob.glob(Path + '3_L/*.jpg')
    
    X_R = Preprocess(Reuse_L)
    Y_R = np.ones(int(len(X_R)/784))#make teach data
    X_S = Preprocess(S_L)
    Y_S = np.full(int(len(X_S)/784),2)#make teach data
    X_M = Preprocess(M_L)
    Y_M = np.zeros(int(len(X_M)/784))#make teach data
    X_L = Preprocess(L_L)
    Y_L = np.full(int(len(X_L)/784),3)#make teach data
    
    X = np.r_[X_R, X_S, X_M, X_L]#concatinate all preprocessed pics.全前処理写真結合
    X = X.reshape([int(len(X)/784),784])#make array.行列化
    y = np.r_[Y_R, Y_S, Y_M, Y_L]#teacher data addition.教師データ付加
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
    size = [28,28]
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

if __name__ == '__main__':
    main()


