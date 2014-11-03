import unittest
from parser import ReplayParser
from mapdrawer import MapDrawer
from os import path

class ReplayParserTestCase(unittest.TestCase):

	def setUp(self):
		libdir = path.abspath(path.dirname(__file__))
		self.testfile = libdir + "/replays/1000394049.dem"

	def test_read_replay_data_heroes_first_tick(self):
		"""
			tick_data contains heroes in right format
			herodata contains name, x, y
		"""

		replay_parser = ReplayParser(self.testfile)
		for tick in replay_parser.read_replay_data():
			self.assertTrue("heroes" in tick)

			herodata = tick["heroes"]
			self.assertTrue(len(herodata) is 10)

			for hero in herodata:
				self.assertTrue("name" in hero)
				self.assertTrue("worldX" in hero)
				self.assertTrue("worldY" in hero)

			break

	def test_get_mapdrawer_should_fail(self):
		"""
			cant get mapdrawer before iterating
		"""
		replay_parser = ReplayParser(self.testfile)

		self.assertRaises(Exception, replay_parser.get_mapdrawer)

	def test_get_mapdrawer_should_succeed(self):
		"""
			can get mapdrawer after iterating
		"""
		replay_parser = ReplayParser(self.testfile)
		for tick in replay_parser.read_replay_data():
			break

		drawer = replay_parser.get_mapdrawer()



if __name__ == '__main__':
    unittest.main()