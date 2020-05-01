
import cv2
import numpy as np
import tkinter as tk
import PIL
import PIL.Image, PIL.ImageTk
from tkinter.ttk import *
from tkinter import *
import os

loop = False
loop2 = False
class Runner(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)
        self.frames = {}

        frame = StartPage(container, self)

        self.frames[StartPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        
class StartPage(tk.Frame):
 
    def __init__(self, window, controller, video_source=0):
        tk.Frame.__init__(self,window)
        self.video_source = video_source
        self.controller = controller
        cam_frame = tk.Frame(self)
        self.vid = MyVideoCapture(self.video_source)
        self.stop_camera()
        self.canvas = tk.Canvas(cam_frame, width = self.vid.width-3, height = self.vid.height-3,bg="black",bd=2)
        self.delay = 15
        self.canvas.pack(padx=5,pady=5)
        cam_frame.pack(side="left",anchor="nw")
        
        self.face_cascade = cv2.CascadeClassifier('Haarcascade\\haarcascade_frontalface_default.xml')
        self.center_coordinates = (int(self.vid.width//2),int(self.vid.height//2)) 
        self.radius = int(self.vid.height//3)
        self.font = cv2.FONT_HERSHEY_COMPLEX
        self.Blue = (0, 0, 255)
        self.Red =  (255,0,0)
        self.Green = (0,255,0)
        self.Black = (0,0,0)
        self.thickness = 2
        self.org = ((self.vid.width//2)-100, self.vid.height-25) 
        self.fontScale = 1
        
        
        self.start_camera()
        
    def update(self):
        global loop
        if loop:
            x,y,w,h = self.center_coordinates[0]-self.radius,self.center_coordinates[1]-self.radius,2*self.radius,2*self.radius
            self.ret, self.frame = self.vid.get_frame()
            frame2 = self.frame[y:y+h,x:x+w,:].copy()
            faces = self.face_cascade.detectMultiScale(frame2, 1.3, 5)
            if len(faces) == 1:
                fx,fy,fw,fh = faces[0]
                if fw > w//2 and fh > h//2:
                    self.frame = cv2.circle(self.frame, self.center_coordinates, self.radius,self.Green , self.thickness)
                else:
                    self.frame = cv2.circle(self.frame, self.center_coordinates,self.radius, self.Red, self.thickness)
            else:
                self.frame = cv2.circle(self.frame, self.center_coordinates, self.radius, self.Black, self.thickness)
            if self.ret:
                self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.frame))
                self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
                self.after(self.delay, self.update)
    
    def stop_camera(self):
        global loop
        if loop:
            loop = False
            self.vid.stop_video_capture()
            self.canvas.delete("all")
            
    def start_camera(self):
        global loop
        if not loop:
            loop = True
            self.vid.start_video_capture()
            self.update()
class MyVideoCapture:
    
    def __init__(self, video_source=0):
        self.video_source = video_source
        self.vid1 = cv2.VideoCapture(self.video_source)
        if not self.vid1.isOpened():
             raise ValueError("Unable to open video source", video_source)
        self.width = self.vid1.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid1.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
    def start_video_capture(self):
        if not self.vid1.isOpened():
            print("start_video_capture")
            self.vid1 = cv2.VideoCapture(self.video_source)
      
    def stop_video_capture(self):
        if self.vid1.isOpened():
            print("stop_video_capture")
            self.vid1.release()
                
    def get_frame(self):  
        if self.vid1.isOpened():
            ret, frame = self.vid1.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)

app = Runner()
app.mainloop()

