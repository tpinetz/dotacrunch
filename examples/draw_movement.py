# adding plugin to path
from dotacrunch import parser
from os import path

def main():
	libdir = path.abspath(path.dirname(__file__))
	demofile = libdir + "/replays/1000394049.dem"

	replay_parser = parser.ReplayParser(demofile)
	draw_data = {}

	interval = 5 # in seconds
	i = 0

	for tick in replay_parser.read_replay_data():

		if tick["time"] < i * interval:
			continue
		i = i + 1

		for hero in tick["heroes"]:
			heroname = hero["name"]

			x = hero["worldX"]
			y = hero["worldY"]

			if heroname not in draw_data:
				draw_data[heroname] = [(x, y)]
			else:
				draw_data[heroname].append((x, y))

	drawer = replay_parser.get_mapdrawer()
	drawer.draw_circle_world_coordinates_list(draw_data["npc_dota_hero_puck"], color = "blue")
	drawer.save(libdir + "/output/puck_movement.png")

	drawer = replay_parser.get_mapdrawer()
	drawer.draw_circle_world_coordinates_list(draw_data["npc_dota_hero_viper"], color = "blue")
	drawer.save(libdir + "/output/viper_movement.png")

if __name__ == "__main__":
	main()
