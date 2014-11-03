# adding plugin to path
from dotacrunch import parser
from os import path

def main():
	demofile = "examples/replays/1000394049.dem"

	# init parser
	replay_parser = parser.ReplayParser(demofile)

	drawer_puck = replay_parser.get_mapdrawer()
	drawer_viper = replay_parser.get_mapdrawer()

	# read_replay_data() returns one tick for every iteration
	for tick in replay_parser.read_replay_data(interval = 5):

		# draw the position of puck in the current tick on the respective drawer
		puck = tick["heroes"]["Puck"]
		x = puck["worldX"]
		y = puck["worldY"]
		drawer_puck.draw_circle_world_coordinates(x, y, color = "red")

		# draw the position of viper in the current tick on the respective drawer
		viper = tick["heroes"]["Viper"]
		x = viper["worldX"]
		y = viper["worldY"]
		drawer_viper.draw_circle_world_coordinates(x, y, color = "blue")

	drawer_puck.save("examples/output/puck_movement.png")
	drawer_viper.save("examples/output/viper_movement.png")

if __name__ == "__main__":
	main()
