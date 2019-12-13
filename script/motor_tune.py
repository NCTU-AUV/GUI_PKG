#!/usr/bin/env python
# license removed for brevity
import numpy as np
import rospy
from std_msgs.msg import Float32MultiArray
import time
import traceback
import Tkinter as tk
import ttk
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats
import math
import rosparam
import threading
import yaml
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

class Main():
    def __init__(self):
        self.tdata = np.array([0,0,0,0,0,0,0,0])
        rospy.init_node('motor_tune',anonymous=True)
        self.force_pub = rospy.Publisher('/force/total',Float32MultiArray,queue_size=10)
        self.win = tk.Tk()
        self.win.title('Dummy motor')
        self.win.wm_geometry("1500x1500")
        scale_frame = tk.Frame(self.win)
        scale_frame.grid(row = 1 ,column = 1)
        ################################################################################
        #                               motor simulate                                 #
        ################################################################################
        self.m =[]
        for i in range(8):
            self.m.append(tk.Scale(scale_frame,from_=-40,to=49,orient=tk.HORIZONTAL,length=400,showvalue=1,tickinterval=20,resolution=0.01,command=self.print_selec_value))
            self.m[i].set(0)
            self.m[i].grid(row=i,column=1)
        tk.Button(scale_frame,  text='Zero gogo!', command=self.set_zero).grid(row = 1 ,column = 2)
        self.win.after(20,self.motor_up)
        self.win.mainloop()
    def print_selec_value(self,data):
        pass
    def set_zero(self):
        for i in range(8):
            self.m[i].set(0)
    def motor_up(self):
        for i in range(8):
            self.tdata[i]=self.m[i].get()
        force_data = Float32MultiArray(data = self.tdata)
        self.force_pub.publish(force_data)
        self.win.after(20,self.motor_up)
if __name__ == "__main__":
    try:
        Main()
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
