import Tkinter 

class TSB(object):
	def __init__(self, parent, spacing=100):
		self.canvas = Canvas(parent)
		self.h = spacing
		self.w = spacing * 1.33
		pass

	def snap(self, x, y):
		outx = self.canvas.canvasx(x, gridspacing=self.h)
		outy = self.canvas.canvasy(y, gridspacing=self.w)
		return (x,y)

	def add_window(self, window, size=[1,1]):
		self.canvas.create_window(window=window, height=self.h,
															width=self.w)
		#get cursor position xmouse, ymouse
		gridx, gridy = self.snap(xmouse, ymouse)

	def _create_token(self, coord, color):
		'''Create a token at the given coordinate in the given color'''
		(x,y) = coord
		self.canvas.create_oval(x-25, y-25, x+25, y+25, 
														outline=color, fill=color, tags="token")

	def OnTokenButtonPress(self, event):
		'''Being drag of an object'''
		# record the item and its location
		self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
		self._drag_data["x"] = event.x
		self._drag_data["y"] = event.y

	def OnTokenButtonRelease(self, event):
		'''End drag of an object'''
		# reset the drag information
		self._drag_data["item"] = None
		self._drag_data["x"] = 0
		self._drag_data["y"] = 0

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
