#Window handler

class WindowHandler(object):
	"""docstring for WindowHandler"""
	def __init__(self):
		self.list = []
		self.stage = None

	def do_to_all(self, **kwargs):
		"""Takes keyword arguments and apllies them to all windows."""
		pass

	def add_window(self, coords, size):
		self.list.append(Window(coords, size))

	def __contains__(self, item):
		for win in self.list:
			if win.get_coords() == item:
				return True
		return False

	def replace(self, coords):
		"""Replaces staged window coords with new coords"""
		if self.stage is not None:
			self.stage.set_coords(coords)
			self.list.ammend(self.stage)
			self.stage = None

	def stage(self, coords):
		for i in len(self.list):
			if self.list[i].get_coords() == coords:
				self.stage = self.list.pop(i)
				return

	def get_size(self, coords):
		for win in self.list:
			if win.get_coords() == coords:
				return win.get_size()
		return None

class Window(object):
	def __init__(self, coords, size):
		self.coords = coords
		self.size = size

	def set_coords(self, coords):
		self.coords = coords

	def get_coords(self):
		return self.coords

	def get_size(self):
		return self.size

class WindowMaker(object):
	"""Creates windows to be placed in the snap board and list."""
	def create(self):
		pass