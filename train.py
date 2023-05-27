from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import numpy as np


class Train:
    def __init__(self,root):
        self.root=root
        self.root.geometry("640x580+0+0")
        self.root.title("Face Recognition System")


        btn_train=Button(self.root,text="Train Model",command=self.train_classifier,font=("times new roman",12,"bold"),bg="blue",fg="black")
        btn_train.place(x=10,y=50,width=600,height=40)



    def train_classifier(self):
        data_dir=("data")
        path= [os.path.join(data_dir,file) for file in os.listdir(data_dir)]

        faces=[]
        ids=[]

        for image in path:
            img=Image.open(image).convert("L")
            imageNp=np.array(img,'uint8')
            id=int(os.path.split(image)[1].split('.')[1])

            faces.append(imageNp)
            ids.append(id)
            cv2.imshow("Training",imageNp)
            cv2.waitKey(1)==13
        ids=np.array(ids)

        #========= Train classifier and save===========
        clf=cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces,ids)
        clf.write("classifier.xml")
        cv2.destroyAllWindows()
        messagebox.showinfo("Result","Training data set completed",parent=self.root)


if __name__ == "__main__":
    root=Tk()
    obj=Train(root)
    root.mainloop()