# adding plugin to path
import sys
sys.path.append('..')

from replayparser import parser

replay_parser = parser.ReplayParser("replays/1000394049.dem")
draw_data = {}

interval = 10 # in seconds
i = 0
tracked_heroes = ["npc_dota_hero_puck"]

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
drawer.draw_circle_world_coordinates_list(draw_data["npc_dota_hero_puck"])
drawer.save("output/puck_movement.png")