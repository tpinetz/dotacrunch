import unittest
from parser import ReplayParser
from drawer import MapDrawer
from os import path

class ReplayParserTestCase(unittest.TestCase):

	def setUp(self):
		libdir = path.abspath(path.dirname(__file__))
		self.testfile = libdir + "/replays/1000394049.dem"

	def test_read_replay_data_heroes_first_tick(self):
		"""
			tick_data contains heroes in right format
			herodata contains name, x, y and they have the right type
		"""

		replay_parser = ReplayParser(self.testfile)
		for tick in replay_parser.read_replay_data():
			self.assertTrue("heroes" in tick)

			herodata = tick["heroes"]
			self.assertTrue(len(herodata) is 10)

			for heroname, data in herodata.iteritems():
				self.assertTrue(heroname)

				self.assertTrue("name" in data)
				self.assertIsInstance(data["name"], str)

				self.assertTrue("worldX" in data)
				self.assertIsInstance(data["worldX"], float)

				self.assertTrue("worldY" in data)
				self.assertIsInstance(data["worldY"], float)

			break

	def test_read_replay_data_interval(self, interval=3):
		replay_parser = ReplayParser(self.testfile)

		prev = -1
		cur = -1

		for tick in replay_parser.read_replay_data(interval = interval):
			prev = cur
			cur = tick["time"]

			if prev is not -1:
				self.assertTrue(round(cur) - round(prev) == interval)

			if cur > 60:
				break

	def test_read_general_data(self):
		replay_parser = ReplayParser(self.testfile)
		general_data = replay_parser.read_general_data()

		self.assertTrue("file" in general_data)

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