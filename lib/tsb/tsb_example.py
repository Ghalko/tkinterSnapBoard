from Tkinter import *
from tsb import TSB

class Example(Frame):
	"""docstring for Example"""
	def __init__(self, master):
		self.f = Frame.__init__(self, master)
		self.master = master
		self.tsb = TSB(master)
		menubar = Menu(self.f)
		# create a pulldown menu, and add it to the menu bar
		filemenu = Menu(menubar, tearoff=0)
		filemenu.add_command(label="Exit", command=self.exit)
		menubar.add_cascade(label="File", menu=filemenu)
		menubar.add_command(label='Toggle', command=self.tsb.toggle_mode)
		self.master.config(menu=menubar)
		testframe = Frame(self.f, bd=1, relief=RAISED)
		Label(testframe, text="Hello World!").pack()
		testframe2 = Frame(self.f, bd=1, relief=RAISED)
		self.tsb.add_window(testframe, cell=[1,1])
		self.tsb.add_window(testframe2, cell=[2,2])

	def exit(self):
		pass

if __name__ == '__main__':
	root = Tk()
	app = Example(root)
	app.mainloop()