# adding plugin to path
from dotacrunch import parser
from os import path

def main():
	demofile = "examples/replays/1000394049.dem"

	# init parser
	replay_parser = parser.ReplayParser(demofile)

	hero_data = {}		# for saving data about the heroes
	interval = 5 		# interval in seconds, in which to parse information
	i = 0				# counter

	# read_replay_data() returns one tick for every iteration
	for tick in replay_parser.read_replay_data():

		# i * interval is minimum time for next tick to be counted
		# dont count, if time is too low
		if tick["time"] < i * interval:
			continue
		i = i + 1

		# read hero data from tick
		for hero in tick["heroes"]:
			heroname = hero["name"]

			x = hero["worldX"]
			y = hero["worldY"]

			if heroname not in hero_data:
				hero_data[heroname] = [(x, y)]
			else:
				hero_data[heroname].append((x, y))

	# get a MapDrawer object to draw on a dota minimap
	drawer = replay_parser.get_mapdrawer()

	# draw the positions that we gathered earlier of Puck in the replay and save them
	drawer.draw_circle_world_coordinates_list(hero_data["npc_dota_hero_puck"], color = "blue")
	drawer.save("examples/output/puck_movement.png")

	# draw the positions that we gathered earlier of Viper in the replay and save them
	drawer = replay_parser.get_mapdrawer()
	drawer.draw_circle_world_coordinates_list(hero_data["npc_dota_hero_viper"], color = "blue")
	drawer.save("examples/output/viper_movement.png")

if __name__ == "__main__":
	main()
