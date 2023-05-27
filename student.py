from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
from datetime import datetime


class Student:
    def __init__(self,root):
        self.root=root
        self.root.geometry("640x580+0+0")
        self.root.title("Face Recognition System")

        self.var_uid=IntVar()
        self.var_student_name=StringVar()
        self.var_branch_name=StringVar()

        main_fram=Frame(self.root,bd=2,bg="white")
        main_fram.place(x=0,y=0,width=640,height=580)

        left_fram=LabelFrame(main_fram,bd=2,relief=RIDGE,text="Student Details",font=("times new roman",12,"bold"),fg="black",bg="white")
        left_fram.place(x=10,y=10,width=320,height=580)

        StudentNameLabel=Label(left_fram,text="Student Name - ",font=("times new roman",12,"bold"),fg="black",bg="white")
        StudentNameLabel.grid(row=0,column=0,padx=10,sticky=W)

        student_name_entry=ttk.Entry(left_fram,textvariable=self.var_student_name,width=20,font=("times new roman",13,"bold"),foreground="black",background="white")
        student_name_entry.grid(row=1,column=0,padx=10,sticky=W)

        BranchNameLabel=Label(left_fram,text="Branch Name - ",font=("times new roman",12,"bold"),fg="black",bg="white")
        BranchNameLabel.grid(row=2,column=0,padx=10,sticky=W)

        branch_name_entry=ttk.Entry(left_fram,textvariable=self.var_branch_name,width=20,font=("times new roman",13,"bold"),foreground="black",background="white")
        branch_name_entry.grid(row=3,column=0,padx=10,sticky=W)

        btn_frame=Frame(left_fram,bd=0,relief=RIDGE,bg="white")
        btn_frame.place(x=20,y=120,width=280,height=50)

        btnSave=Button(btn_frame,width=10,text="Save",command=self.add_data,font=("times new roman",13,"bold"),bg="blue")
        btnSave.grid(row=0,column=0)

        btnDelete=Button(btn_frame,width=10,text="Delete",command=self.delete_data,font=("times new roman",13,"bold"),bg="blue")
        btnDelete.grid(row=0,column=1)


        student_detail_frame=Frame(left_fram,bd=2,relief=RIDGE,bg="white")
        student_detail_frame.place(x=10,y=200,width=300,height=300)

        lbl_uid_ph=Label(student_detail_frame,text="UID",width=20,font=("times new roman",12,"bold"),bg="white",fg="gray")
        lbl_uid_ph.grid(row=0,column=0,padx=0,pady=0)

        self.lbl_uid=Label(student_detail_frame,text="",width=20,font=("times new roman",12,"bold"),bg="white",fg="black")
        self.lbl_uid.grid(row=1,column=0,padx=0,pady=0)

        lbl_student_ph=Label(student_detail_frame,text="Student Name",width=20,font=("times new roman",12,"bold"),bg="white",fg="gray")
        lbl_student_ph.grid(row=0,column=1,padx=0,pady=0)

        self.lbl_student=Label(student_detail_frame,text="",width=20,font=("times new roman",12,"bold"),bg="white",fg="black")
        self.lbl_student.grid(row=1,column=1,padx=0,pady=0)

        lbl_branch_ph=Label(student_detail_frame,text="Branch Name",width=20,font=("times new roman",12,"bold"),bg="white",fg="gray")
        lbl_branch_ph.grid(row=2,column=0,padx=0,pady=0)

        self.lbl_branch=Label(student_detail_frame,text="",width=20,font=("times new roman",12,"bold"),bg="white",fg="black")
        self.lbl_branch.grid(row=3,column=0,padx=0,pady=0)

        btn_take_photo=Button(student_detail_frame,text="Take Photo",command=self.generate_dataset,font=("times new roman",12,"bold"),bg="blue",fg="black")
        btn_take_photo.place(x=10,y=90,width=250,height=30)

        self.lbl_last_update=Label(student_detail_frame,text="last updated on 08-05-2023",font=("times new roman",12,"bold"),bg="white",fg="black")
        self.lbl_last_update.place(x=10,y=140,width=250,height=20)


        right_frame=LabelFrame(main_fram,bd=2,bg="white",relief=RIDGE,text="Student Details",font=("times new roman",12,"bold"),fg="black")
        right_frame.place(x=330,y=10,width=320,height=580)

        table_frame=Frame(right_frame,bd=2,bg="white",relief=RIDGE)
        table_frame.place(x=5,y=10,width=300,height=530)

        scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(table_frame,orient=VERTICAL)

        self.student_table=ttk.Treeview(table_frame,columns=("uid","student","branch"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("uid",text="User ID")
        self.student_table.heading("student",text="Student Name")
        self.student_table.heading("branch",text="Branch Name")

        self.student_table["show"]="headings"

        self.student_table.column("uid",width=70)
        self.student_table.column("student",width=150)
        self.student_table.column("branch",width=150)

        self.student_table.pack(fill=BOTH,expand=1)
        self.student_table.bind("<ButtonRelease-1>",self.get_cursor)
        self.fetch_data()


    def add_data(self):
        if self.var_student_name.get()=="" or self.var_branch_name.get()=="":
            messagebox.showerror("Error","Enter student name and branch",parent=self.root)
        else:
            try:
                conn=mysql.connector.connect(host="localhost",port=8889,username="test",password="Test@123",database="face_recogniser")
                my_cursor=conn.cursor()
                my_cursor.execute("insert into students(name,branch) values (%s,%s)",(self.var_student_name.get(),self.var_branch_name.get()))
                conn.commit()
                self.fetch_data()
                self.var_branch_name.set("")
                self.var_student_name.set("")
                conn.close()
                messagebox.showinfo("Success","Student details added",parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due to :{str(es)}",parent=self.root)    

    def fetch_data(self):
        conn=mysql.connector.connect(host="localhost",port=8889,username="test",password="Test@123",database="face_recogniser")
        my_cursor=conn.cursor()
        my_cursor.execute("select * from students")
        data=my_cursor.fetchall()

        if len(data)!=0:
            self.student_table.delete(*self.student_table.get_children())
            for i in data:
                self.student_table.insert("",END,values=i)
            conn.commit()
        conn.close()


    def get_cursor(self,tt):
        print(tt)
        cursor_focus=self.student_table.focus()
        content=self.student_table.item(cursor_focus)
        data=content["values"]

        self.lbl_uid.config(text=str(data[0]))
        self.lbl_student.config(text=data[1])
        self.lbl_branch.config(text=data[2])
        self.lbl_last_update.config(text="Last updated at "+data[3])

    def delete_data(self):
        if self.lbl_uid['text']=="":
            messagebox.showerror("Error","Student not selected",parent=self.root)
        else:
            try:
                delete=messagebox.askyesno("Student Delete Page","Are you sure want to delete?",parent=self.root)
                if delete>0:
                    conn=mysql.connector.connect(host="localhost",port=8889,username="test",password="Test@123",database="face_recogniser")
                    my_cursor=conn.cursor()
                    sql="delete from students where uid=%s"
                    val=(self.lbl_uid['text'])
                    my_cursor.execute(sql,[val])
                else:
                    if not delete:
                        return
                    
                conn.commit()
                self.reset_data()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Delete","Successfully deleted student details",parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due to :{str(es)}",parent=self.root)

    def reset_data(self):
        self.lbl_uid.config(text="")
        self.lbl_student.config(text="")
        self.lbl_branch.config(text="")

    def generate_dataset(self):
        if self.lbl_uid['text']=="":
            messagebox.showerror("Error","Select student",parent=self.root)
        else:
            try:
                uid=self.lbl_uid['text']
                face_classifier=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

                def face_cropped(img):
                    gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces=face_classifier.detectMultiScale(gray,1.3,5)

                    for(x,y,w,h) in faces:
                        face_cropped=img[y:y+h,x:x+w]
                        return face_cropped

                cap=cv2.VideoCapture(1)
                img_id=0
                while True:
                    ret,my_frame=cap.read()
                    if face_cropped(my_frame) is not None:
                        img_id+=1
                        face=cv2.resize(face_cropped(my_frame),(450,450),interpolation = cv2.INTER_AREA)
                        face=cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
                        file_name_path="data/user."+str(uid)+"."+str(img_id)+".jpg"
                        cv2.imwrite(file_name_path,face)
                        cv2.putText(face,str(img_id),(50,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),2)
                        cv2.imshow("Cropped Face",face)

                        if cv2.waitKey(1)==13 or int(img_id)==100:
                            break

                cap.release()
                cv2.destroyAllWindows()
                conn=mysql.connector.connect(host="localhost",port=8889,username="test",password="Test@123",database="face_recogniser")
                my_cursor=conn.cursor()
                my_cursor.execute("update students set sample_taken_at=%s where uid=%s",(str(datetime.now()),self.lbl_uid['text']))
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Result","Student image captured successfully")
            except Exception as es:
                    messagebox.showerror("Error",f"Due to :{str(es)}",parent=self.root)




if __name__ == "__main__":
    root=Tk()
    obj=Student(root)
    root.mainloop()