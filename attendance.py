from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import numpy as np


class Attendance:
    def __init__(self,root):
        self.root=root
        self.root.geometry("640x580+0+0")
        self.root.title("Face Recognition System")

        main_fram=Frame(self.root,bd=2,bg="white")
        main_fram.place(x=0,y=0,width=640,height=580)

        table_frame=Frame(main_fram,bd=2,bg="white",relief=RIDGE)
        table_frame.place(x=5,y=10,width=620,height=560)

        scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(table_frame,orient=VERTICAL)

        self.student_table=ttk.Treeview(table_frame,columns=("date","time","uid","name","branch"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("date",text="Date")
        self.student_table.heading("time",text="Time")
        self.student_table.heading("uid",text="User Id")
        self.student_table.heading("name",text="Name")
        self.student_table.heading("branch",text="Branch")

        self.student_table["show"]="headings"

        self.student_table.column("date",width=30)
        self.student_table.column("time",width=30)
        self.student_table.column("uid",width=30)
        self.student_table.column("name",width=50)
        self.student_table.column("branch",width=50)

        self.student_table.pack(fill=BOTH,expand=1)
        self.fetch_data()



    def fetch_data(self):
        conn=mysql.connector.connect(host="localhost",port=8889,username="test",password="Test@123",database="face_recogniser")
        my_cursor=conn.cursor()
        my_cursor.execute("select date,time,uid,name,department as branch from attendance order by date DESC, time DESC")
        data=my_cursor.fetchall()

        if len(data)!=0:
            self.student_table.delete(*self.student_table.get_children())
            for i in data:
                self.student_table.insert("",END,values=i)
            conn.commit()
        conn.close()

if __name__ == "__main__":
    root=Tk()
    obj=Attendance(root)
    root.mainloop()