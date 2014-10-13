from Tkinter import *

class TSB(Frame):
	"""tkinter snap board - ref:
	http://stackoverflow.com/questions/6740855/board-drawing-code-to-move-an-oval/6789351#6789351
	"""
	def __init__(self, master=None, spacing=150, size=5, buff=5):
		self.m = master
		self.f = Frame.__init__(self, master)
		self.h = spacing
		self.w = spacing * 1.33
		self.size = size
		self.buff = buff
		self.canvas = Canvas(self.f, width=self.w*size,
												 height=self.h*size)
		self.canvas.pack(fill="both", expand=True)
		self._drag_data = {"x": 0, "y": 0, "item": None}
		self._create_token((self.w, self.h), "white")
		self._create_token((self.w*2, self.h*2), "black")
		self.canvas.tag_bind("token", "<ButtonPress-1>", self.OnTokenButtonPress)
		self.canvas.tag_bind("token", "<ButtonRelease-1>", self.OnTokenButtonRelease)
		self.canvas.tag_bind("token", "<B1-Motion>", self.OnTokenMotion)
		self.show_snap()
		self.testframe = Frame(self.f, bd=1, relief=RAISED)
		self.add_window(self.testframe)
		self.remove_snap()

	def snap(self):
		coords = self.canvas.coords(self._drag_data["item"])
		dx = coords[2] - coords[0]
		dy = coords[3] - coords[1]
		newx = int(coords[0]/self.w) * self.w
		newy = int(coords[1]/self.h) * self.h
		self.canvas.coords(self._drag_data["item"], newx, newy, newx+dx, newy+dy)
		if self._drag_data["window"] is not None:
			self.canvas.coords(self._drag_data["window"], newx+(self.w/2), newy+(self.h/2)+(self.buff/2))

	def show_snap(self):
		for x in range(self.size):
			dx = x * self.w
			for y in range(self.size):
				dy = y * self.h
				self.canvas.create_oval(dx-2, dy-2, dx+2, dy+2,
																outline="black", fill="black",
																tags="grid")

	def remove_snap(self):
		self.canvas.delete("grid")

	def add_window(self, window, size=[1,1]):
		self.canvas.create_window(self.w+(self.w/2),
															self.h+(self.h/2)+(self.buff/2),
															window=window,
															height=self.h-(self.buff),
															width=self.w-(2*self.buff), tags="window")
		#get cursor position xmouse, ymouse

	def _create_token(self, coord, color):
		'''Create a token at the given coordinate in the given color'''
		(x,y) = coord
		self.canvas.create_rectangle(x, y, x+self.w, y+self.h,
																 outline=color, fill=color,
																 tags="token")

	def OnTokenButtonPress(self, event):
		'''Being drag of an object'''
		# record the item and its location
		self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
		self._drag_data["orig_coords"] = self.canvas.coords(self._drag_data["item"])
		x1, y1, x2, y2 = tuple(self._drag_data["orig_coords"])
		try:
			self._drag_data["window"] = self.canvas.find_enclosed(x1, y1, x2, y2)[0]
		except:
			self._drag_data["window"] = None
		self._drag_data["x"] = event.x
		self._drag_data["y"] = event.y
		

	def OnTokenButtonRelease(self, event):
		'''End drag of an object'''
		#check for overlapping tokens
		if len(self.canvas.find_overlapping(event.x-1, event.y-1, event.x+1, event.y+1)) > 1:
			x1, y1, x2, y2 = tuple(self._drag_data["orig_coords"])
			self.canvas.coords(self._drag_data["item"], x1, y1, x2, y2)
		self.snap()
		# reset the drag information
		self._drag_data["item"] = None
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
		self.canvas.move(self._drag_data["item"], delta_x, delta_y)
		# record the new position
		self._drag_data["x"] = event.x
		self._drag_data["y"] = event.y


if __name__ == '__main__':
	root = Tk()
	app = TSB(root)
	app.mainloop()