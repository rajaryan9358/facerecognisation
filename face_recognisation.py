from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
from time import strftime
from datetime import datetime
import cv2
import os
import numpy as np


class FaceRecognisation:
    def __init__(self,root):
        self.root=root
        self.root.geometry("640x580+0+0")
        self.root.title("Face Recognition System")


        btn_recognise=Button(self.root,text="Recognise Face",command=self.face_recog,font=("times new roman",12,"bold"),bg="blue",fg="black")
        btn_recognise.place(x=10,y=50,width=600,height=40)

    
    def face_recog(self):
        def draw_boundary(img,classifier,scaleFactor,minNeighbors,color,text,clf):
            gray_image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            features=classifier.detectMultiScale(gray_image,scaleFactor,minNeighbors)

            coord=[]

            for (x,y,w,h) in features:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
                id,predict=clf.predict(gray_image[y:y+h,x:x+w])
                confidence=int((100*(1-predict/300)))

                conn=mysql.connector.connect(host="localhost",port=8889,username="test",password="Test@123",database="face_recogniser")
                my_cursor=conn.cursor()

                my_cursor.execute("select name from students where uid="+str(id))
                n=my_cursor.fetchone()
                n="+".join(n)

                my_cursor.execute("select branch from students where uid="+str(id))
                b=my_cursor.fetchone()
                b="+".join(b)

                # n="Aryan"
                # b="CSE"


                if confidence>77:
                    cv2.putText(img,f"UID:{id}",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"Name:{n}",(x,y-30),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"Branch:{b}",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    self.mark_attendance(id,n,b)
                else:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
                    cv2.putText(img,"Unknown Face",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                
                coord=[x,y,w,h]
            return coord

        def recognise(img,clf,faceCascade):
            coord=draw_boundary(img,faceCascade,1.2,10,(255,255,255),"Face",clf)
            return img

        faceCascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf=cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        cap=cv2.VideoCapture(1)

        while True:
            ret,img=cap.read()

            if ret:
                print("Frame not empty")
                img=recognise(img,clf,faceCascade)
                cv2.imshow("Welcome to face recognisation",img)
            else:
                print("Frame is empty")    


            if cv2.waitKey(1)==13:
                break
        cap.release()
        cv2.destroyAllWindows()    

    def mark_attendance(self,i,n,b):
        now=datetime.now()
        d1=now.strftime("%Y-%m-%d")
        dtString=now.strftime("%H:%M:%S")

        conn=mysql.connector.connect(host="localhost",port=8889,username="test",password="Test@123",database="face_recogniser")
        my_cursor=conn.cursor()
        my_cursor.execute("select * from attendance where uid="+str(i)+" and date='"+str(d1)+"'")
        data=my_cursor.fetchall()

        if len(data)==0:
            my_cursor.execute("insert into attendance(uid,name,department,date,time,status) values (%s,%s,%s,%s,%s,%s)",(str(i),n,b,d1,dtString,"Present"))

        conn.commit()
        conn.close()

if __name__ == "__main__":
    root=Tk()
    obj=FaceRecognisation(root)
    root.mainloop()