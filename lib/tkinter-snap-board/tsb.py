from Tkinter import *

class TSB(Frame):
	"""tkinter snap board - ref:
	http://stackoverflow.com/questions/6740855/board-drawing-code-to-move-an-oval/6789351#6789351
	"""
	def __init__(self, master=None, spacing=150, size=5, buff=10):
		self.m = master
		self.f = Frame.__init__(self, master)
		self.h = spacing
		self.w = int(spacing * 1.33)
		self.size = size
		self.buff = buff
		self.canvas = Canvas(self.f, width=self.w*size,
												 height=self.h*size)
		self.canvas.pack(fill="both", expand=True)
		self._drag_data = {"x": 0, "y": 0, "grab": None}
		self._create_token("white", cell=[1,1])
		self._create_token("black", cell=[2,2])
		self.canvas.tag_bind("token", "<ButtonPress-1>", self.OnTokenButtonPress)
		self.canvas.tag_bind("token", "<ButtonRelease-1>", self.OnTokenButtonRelease)
		self.canvas.tag_bind("token", "<B1-Motion>", self.OnTokenMotion)
		self.show_grid()
		self.testframe = Frame(self.f, bd=1, relief=RAISED)
		self.testframe2 = Frame(self.f, bd=1, relief=RAISED)
		self.add_window(self.testframe, cell=[1,1])
		self.add_window(self.testframe2, cell=[2,2])
		#self.remove_grid()

	def snap_grab(self, mx, my):
		"""Snaps grab portion into cell"""
		x1, y1, x2, y2 = tuple(self._drag_data["orig_coords"])
		if len(self.canvas.find_overlapping(mx-1, my-1, mx+1, my+1)) <= 1:
			x1, y1 = self.calculate_snap(mouse=[mx,my])
			x2 = x1 + self.w
			y2 = y1 + self.h
		self.canvas.coords(self._drag_data["grab"], x1, y1, x2, y2)

	def snap_window(self):
		"""Snaps window into cell following its grab"""
		if self._drag_data["window"] is not None:
			coords = self.canvas.coords(self._drag_data["grab"])
			newx = coords[0] + self.w / 2
			newy = coords[1] + (self.buff + self.h) / 2
			self.canvas.coords(self._drag_data["window"],
							   newx, newy)

	def calculate_snap(self, mouse=None, cell=None):
		if cell is not None:
			newx = cell[0] * self.w
			newy = cell[1] * self.h
		else:
			newx = int(mouse[0]/self.w) * self.w
			newy = int(mouse[1]/self.h) * self.h
		return newx, newy

	def show_grid(self):
		for x in range(self.size+1):
			dx = x * self.w
			for y in range(self.size+1):
				dy = y * self.h
				self.canvas.create_oval(dx-2, dy-2, dx+2, dy+2,
										outline="black", fill="black",
										tags="grid")

	def remove_grid(self):
		self.canvas.delete("grid")

	def add_window(self, window, size=[1,1], cell=None, mouse=None):
		newx, newy = self.calculate_snap(cell=cell, mouse=mouse) #grid point
		print newx, newy
		newh = self.h - self.buff #to show grab
		newy = newy + self.buff + (newh / 2) #to show grab
		newx = newx + (self.w / 2)
		self.canvas.create_window(newx, newy, window=window,
								  height=newh, width=self.w,
								  tags="window")

	def _create_token(self, color, cell=None, mouse=None):
		'''Create a token at the given coordinate in the given color'''
		x, y = self.calculate_snap(cell=cell, mouse=mouse)
		print x, y
		self.canvas.create_rectangle(x, y, x+self.w, y+self.h,
									 outline=color, fill=color,
									 tags="token")

	def OnTokenButtonPress(self, event):
		'''Being drag of an object'''
		# record the item and its location
		self._drag_data["grab"] = self.canvas.find_closest(event.x, event.y)[0]
		self._drag_data["orig_coords"] = self.canvas.coords(self._drag_data["grab"])
		x1, y1, x2, y2 = tuple(self._drag_data["orig_coords"])
		print self.canvas.find_enclosed(x1-1, y1-1, x2+1, y2+1)
		try:
			self._drag_data["window"] = self.canvas.find_enclosed(x1-1, y1-1, x2+1, y2+1)[1]
		except:
			self._drag_data["window"] = None
		self._drag_data["x"] = event.x
		self._drag_data["y"] = event.y
		print self._drag_data
		

	def OnTokenButtonRelease(self, event):
		'''End drag of an object'''
		#check for overlapping tokens
		self.snap_grab(event.x, event.y)
		self.snap_window()
		# reset the drag information
		self._drag_data["grab"] = None
		self._drag_data["window"] = None
		self._drag_data["x"] = 0
		self._drag_data["y"] = 0
		self._drag_data["orig_coords"] = []

	def OnTokenMotion(self, event):
		'''Handle dragging of an object'''
		# compute how much this object has moved
		delta_x = event.x - self._drag_data["x"]
		delta_y = event.y - self._drag_data["y"]
		# move the object the appropriate amount
		self.canvas.move(self._drag_data["grab"], delta_x, delta_y)
		# record the new position
		self._drag_data["x"] = event.x
		self._drag_data["y"] = event.y


if __name__ == '__main__':
	root = Tk()
	app = TSB(root)
	app.mainloop()