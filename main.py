from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from student import Student
from train import Train
from face_recognisation import FaceRecognisation
from attendance import Attendance

class Face_recognition_system:
    def __init__(self,root):
        self.root=root
        self.root.geometry("640x580+0+0")
        self.root.title("Face Recognition System")

        title_lbl=Label(self.root,text="Face recognition attendance system",font=("times new roman",35,"bold"),bg="black",fg="red")
        title_lbl.place(x=0,y=0,width=640,height=45)

        btnStudent=Button(self.root,text="Students",command=self.student_details,cursor="hand2")
        btnStudent.place(x=100,y=80,width=180,height=100)

        btnDetector=Button(self.root,text="Face Recognisation",command=self.recognise_window,cursor="hand2")
        btnDetector.place(x=100,y=200,width=180,height=100)

        btnTrain=Button(self.root,text="Train data",command=self.training_window,cursor="hand2")
        btnTrain.place(x=300,y=80,width=180,height=100)

        btnAttendance=Button(self.root,text="Attendance",command=self.attendance_window,cursor="hand2")
        btnAttendance.place(x=300,y=200,width=180,height=100)

    
    def student_details(self):
        self.new_window=Toplevel(self.root)
        self.app=Student(self.new_window)

    def training_window(self):
        self.new_window=Toplevel(self.root)
        self.app=Train(self.new_window)

    def recognise_window(self):
        self.new_window=Toplevel(self.root)
        self.app=FaceRecognisation(self.new_window)
    
    def attendance_window(self):
        self.new_window=Toplevel(self.root)
        self.app=Attendance(self.new_window)

if __name__ == "__main__":
    root=Tk()
    obj=Face_recognition_system(root)
    root.mainloop()