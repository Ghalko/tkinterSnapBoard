from Tkinter import *

class TSB(object):
	def __init__(self, parent, spacing=100):
		self.canvas = Canvas(parent)
		self.space = spacing
		pass

	def snap(self, x, y):
		outx = self.canvas.canvasx(x, gridspacing=self.space)
		outy = self.canvas.canvasy(y, gridspacing=self.space)
		return (x,y)

	def add_window(self, window):
		self.canvas.create_window(window=window)



if __name__ == '__main__':
