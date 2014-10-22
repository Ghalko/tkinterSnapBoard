from Tkinter import *
from snapWindow import WindowHandler as wh

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
		self.canvas.tag_bind("token", "<ButtonPress-1>",
							 self.OnTokenButtonPress)
		self.canvas.tag_bind("token", "<ButtonRelease-1>",
							 self.OnTokenButtonRelease)
		self.canvas.tag_bind("token", "<B1-Motion>",
							 self.OnTokenMotion)
		self.mode = None
		self.wlist = wh()
		self.toggle_mode(mode="stay")

	def snap_grab(self, mx, my):
		"""Snaps grab portion into cell"""
		x1, y1, x2, y2 = tuple(self._drag_data["orig_coords"])
		if len(self.canvas.find_overlapping(mx-1, my-1, mx+1, my+1)) <= 1:
			x1, y1 = self._calculate_snap(mouse=[mx,my])
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
			x, y = self._calculate_cell((newx, newy))
			self.wlist.replace([x,y])

	def _calculate_snap(self, mouse=None, cell=None):
		if cell is not None:
			newx = cell[0] * self.w
			newy = cell[1] * self.h
		else:
			newx = int(mouse[0]/self.w) * self.w
			newy = int(mouse[1]/self.h) * self.h
		return newx, newy

	def _calculate_cell(self, coords):
		x, y = coords
		col = int(x/self.w)
		row = int(y/self.h)
		return col, row

	def show_grid(self):
		for x in range(self.size+1):
			dx = x * self.w
			for y in range(self.size+1):
				dy = y * self.h
				self.canvas.create_oval(dx-2, dy-2, dx+2, dy+2,
										outline="black", fill="black",
										tags="grid")
				if x != self.size and y != self.size and [x,y] in self.wlist:
					color = "#" + hex(0xDDDDFF - (x+y) * 0x111111)[-6:]
					size = self.wlist.get_size([x,y])
					self._create_token(color, size=size, cell=[x,y])

	def remove_grid(self):
		self.canvas.delete("grid")
		self.canvas.delete("token")

	def add_window(self, window, size=[1,1], cell=None, mouse=None):
		newx, newy = self._calculate_snap(cell=cell, mouse=mouse) #grid point
		newh = (size[1] * self.h) - self.buff #to show grab
		neww = size[0] * self.w
		newy = newy + self.buff + (newh / 2) #to show grab
		newx = newx + (neww / 2)
		self.canvas.create_window(newx, newy, window=window,
								  height=newh, width=neww,
								  tags="window")
		x, y = self._calculate_cell((newx, newy))
		self.wlist.add_window([x,y], size)

	def _create_token(self, color, size=[1,1], cell=None, mouse=None):
		'''Create a token at the given coordinate in the given color'''
		x, y = self._calculate_snap(cell=cell, mouse=mouse)
		self.canvas.create_rectangle(x, y, x+(self.w*size[0]),
									 y+(self.h*size[1]),
									 outline=color, fill=color,
									 tags="token")

	def OnTokenButtonPress(self, event):
		'''Being drag of an object'''
		# record the item and its location
		self._drag_data["grab"] = self.canvas.find_closest(event.x, event.y)[0]
		self._drag_data["orig_coords"] = self.canvas.coords(self._drag_data["grab"])
		x1, y1, x2, y2 = tuple(self._drag_data["orig_coords"])
		try:
			win = list(self.canvas.find_enclosed(x1-1, y1-1, x2+1, y2+1))
			win.remove(self._drag_data["grab"])
			self._drag_data["window"] = win[0]
		except:
			self._drag_data["window"] = None
		self._drag_data["x"] = event.x
		self._drag_data["y"] = event.y
		#remove window from list
		x, y = self._calculate_cell((event.x, event.y))
		if [x,y] in self.wlist:
			self.wlist.remove([x,y])
		
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

	def toggle_mode(self, mode=None):
		modes = ["move", "stay"]
		if mode is None or mode not in modes:
			modes.remove(self.mode) #removes current mode
			mode = modes[0] #sets mode to remaining mode
		self.mode = mode
		if mode == "move":
			self.show_grid()
		else:
			self.remove_grid()


if __name__ == '__main__':
	root = Tk()
	app = TSB(root)
	app.mainloop()