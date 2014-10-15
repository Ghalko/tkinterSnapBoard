import unittest
from tsb.tsb import TSB
from Tkinter import *

class TestTSB(unittest.TestCase):
	def setUp(self):
		root = Tk()
		self.tsb = TSB(root)

	def tearDown(self):
		self.tsb = None

	def test_toggle_mode(self):
		"""Tests toggle_mode"""
		self.assertEqual("move", self.tsb.mode)
		self.tsb.toggle_mode()
		self.assertEqual("stay", self.tsb.mode)
		self.tsb.toggle_mode()
		self.assertEqual("move", self.tsb.mode)
		self.tsb.toggle_mode(mode="incorrect")
		self.assertEqual("stay", self.tsb.mode)
		self.tsb.toggle_mode(mode="stay")
		self.assertEqual("stay", self.tsb.mode)