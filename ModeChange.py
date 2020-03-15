# mode change class
import tkinter as tk

class MChange:
    def __init__(self):
        pass
    def learning(self):
        pass
    def take_pics_and_judge(self):
        pass
    def select_mode(self):
        # ウィンドウを生成してそのウィンドウを操作するための値をrootに代入します。
        root = tk.Tk()
        # ウィンドウ名を指定します
        root.title('選択')
        # ウィンドウサイズを指定します。('x'は、小文字のエックスです。)
        root.geometry('225x70')


        #ボタンの定義
        ButtonA = tk.Button(root,text="学習モード", command=self.learning, width=12, height=3)
        ButtonB = tk.Button(root,text="撮影&判定モード", command=self.take_pics_and_judge, width=12, height=3)
        #ボタンの並びを定義
        ButtonA.grid(row=0, column=0)
        ButtonB.grid(row=0, column=1)

        # ウィンドウを表示して制御するためのループに入ります。
        root.mainloop()
    def hi():
        print("hi, there")
    

        

