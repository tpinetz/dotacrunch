import matplotlib
matplotlib.use('Agg')

from dotacrunch import parser
import matplotlib.pyplot as plt

def main():
	demofile = "examples/replays/1000394049.dem"

	# init parser
	replay_parser = parser.ReplayParser(demofile)

	puck_gpm_xpm = []
	viper_gpm_xpm = []

	# read_replay_data() returns one tick for every iteration
	for tick in replay_parser.read_replay_data(interval = 5):
		# getting time value and converting it into seconds
		seconds = tick["time"]
		minutes = seconds / 60

		# collecting data
		puck = tick["heroes"]["Puck"]
		puck_gpm_xpm.append((minutes, puck["gpm"], puck["xpm"]))

		viper = tick["heroes"]["Viper"]
		viper_gpm_xpm.append((minutes, viper["gpm"], viper["xpm"]))

	# plotting for puck
	time, gpm, xpm = zip(*puck_gpm_xpm)
	plt.subplot(2, 1, 1)
	plt.plot(time, gpm, color = "#DE0909", label = "GPM")	# red
	plt.plot(time, xpm, color = "#0088FF", label = "XPM")	# blue
	plt.title("Puck GPM & XPM")

	# plotting for viper
	time, gpm, xpm = zip(*viper_gpm_xpm)
	plt.subplot(2, 1, 2)
	plt.plot(time, gpm, color = "#DE0909", label = "GPM")	# red
	plt.plot(time, xpm, color = "#0088FF", label = "XPM")	# blue
	plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
	plt.title("Viper GPM & XPM")

	plt.savefig("examples/output/gpm_xpm_graph.png")

if __name__ == "__main__":
	main()