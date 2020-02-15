import Tkinter as tk
from std_msgs.msg import Int32MultiArray
window = tk.Tk()
window.title("haha")
window.geometry("800x900")

def insert_point():
	global var
	var=int(e.get())
	print(type(var))
	print(var)
	countdown(var)
def countdown(remaining = None):
	global label
	global var
	if remaining is not None:
		var = remaining
	if var <= 0.1:
		label.configure(text="time's up!")
	else:
		label.configure(text=str(var))
		var = var - 0.1
		label.after(100, countdown)


if __name__ == "__main__":
	window.wm_geometry("1200x600")
	var = 0
	e= tk.Entry(window)
	e.pack()
	label = tk.Label(window, text="", width=10)
	label.pack()
	b1 = tk.Button(window,text="insert point",width=18,height=2,command=insert_point)
	b1.pack()
	window.mainloop()