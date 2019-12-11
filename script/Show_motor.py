#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
from std_msgs.msg import Float32MultiArray
import traceback
import cv2
from PIL import ImageTk
from PIL import Image
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
matplotlib.use('TkAgg')
import Tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import Tkinter as tk
import time

class Page(tk.Frame):
	def __init__(self, *args, **kwargs):
		tk.Frame.__init__(self, *args, **kwargs)
	def show(self):
		self.lift()

class Page1(Page):
	def __init__(self, *args, **kwargs):
		self.counter = 20
		self.bdata = np.array([0,0,0,0,0,0,0,0])
		self.ddata = np.array([0,0,0,0,0,0,0,0])
		self.fdata = np.array([0,0,0,0,0,0,0,0])
		self.tdata = np.array([0,0,0,0,0,0,0,0])
		Page.__init__(self, *args, **kwargs)
		self.fig =Figure(figsize=(10,5), dpi=100)
		self.ax_b = self.fig.add_subplot(141)
		self.ax_d = self.fig.add_subplot(142)
		self.ax_f = self.fig.add_subplot(143)
		self.ax_t = self.fig.add_subplot(144)
		self.canvas = FigureCanvasTkAgg(self.fig,master = self)
		#self.canvas.show()
		self.canvas.get_tk_widget().grid(row=1 ,column=1)
		rospy.Subscriber("/force/balance", Float32MultiArray, self.balance_update,queue_size=1)
		rospy.Subscriber('/force/depth', Float32MultiArray, self.depth_update,queue_size=1)
		rospy.Subscriber('/force/forward', Float32MultiArray, self.forward_update,queue_size=1)
		rospy.Subscriber('/force/total', Float32MultiArray, self.total_update,queue_size=1)
		self.label = tk.Label(self,text='1')
		self.label.grid(row = 2,column =1)
		self.label.after(25, self.rebar)

	def balance_update(self,data):
		self.bdata = np.array(data.data)
	def depth_update(self,data):
		self.ddata = np.array(data.data)
	def forward_update(self,data):
		self.fdata = np.array(data.data)
	def total_update(self,data):
		self.tdata = np.array(data.data)
	def rebar(self):
		self.ax_b.cla()
		self.ax_d.cla()
		self.ax_f.cla()
		self.ax_t.cla()
		x = range(1,9)
		self.ax_b.barh(x,self.bdata,label= 'balance',color = 'orange')
		self.ax_b.set_title("balance")
		self.ax_d.barh(x,self.ddata,label= 'depth')
		self.ax_d.set_title("depth")
		self.ax_f.barh(x,self.fdata,label= 'forward')
		self.ax_f.set_title("forward")
		self.ax_t.barh(x,self.tdata,label= 'total',color ='black')
		self.ax_t.set_title("total")
		self.ax_b.set_xlim((-100,100))
		self.ax_d.set_xlim((-100,100))
		self.ax_f.set_xlim((-100,100))
		self.ax_t.set_xlim((-100,100))
		self.canvas.draw()
		self.label.after(10, self.rebar)


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Motor show", command=p1.lift())

        b1.pack(side="left")

def GUI():
	rospy.init_node('Show_motor', anonymous=True)
	root = tk.Tk()
	main = MainView(root)
	main.pack(side="top", fill="both", expand=True)
	root.wm_geometry("1500x1000")
	root.mainloop()
if __name__ == "__main__":
	try:
		GUI()
	except Exception as e:
	    exstr = traceback.format_exc()
	    print(exstr)
