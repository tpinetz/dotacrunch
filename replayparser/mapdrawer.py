from PIL import Image, ImageDraw
from numpy import array, random, vstack, ones, linalg
from const import TOWERS
from copy import deepcopy
from os import path

class MapDrawer:
    """
        a class for drawing Dota2Maps with replay-parsed data

    """
    def __init__(self, towers, received_tables):
        self.coordinates = []
        libdir = path.abspath(path.dirname(__file__))
        self.image = Image.open(libdir + "/assets/dota2map.png")
        self.draw = ImageDraw.Draw(self.image)

        self.map_w, self.map_h = self.image.size

        # init information tables and respective columns
        tower_info_table = received_tables.by_dt['DT_DOTA_BaseNPC_Tower']
        position_x_index = tower_info_table.by_name['m_cellX']
        position_y_index = tower_info_table.by_name['m_cellY']
        position_vector_index = tower_info_table.by_name['m_vecOrigin']
        name_index = tower_info_table.by_name['m_iName']

        tower_list = deepcopy(TOWERS)

        # getting world coordinates for every tower in TOWERS
        for name, data in tower_list.iteritems():
            for t in towers:
                state = t.state
                state_name = state.get(name_index)
                if state_name == name:
                    data["worldX"] = state.get(position_x_index) + state.get(position_vector_index)[0] / 128.

                    if "worldY" not in data:
                        data["worldY"] = state.get(position_y_index) + state.get(position_vector_index)[1] / 128.

        # caching vals, so ordering stays the same throughout the comprehensions
        vals = tower_list.values()
        x = [v["worldX"] for v in vals if "worldX" in v]
        y = [v["worldY"] for v in vals if "worldY" in v]
        x_map = [v["x"] for v in vals if "worldX" in v]
        y_map = [v["y"] for v in vals if "worldY" in v]

        # calculating scale and offset to convert worldcoordinates to coordinates on the map 
        Ax = vstack((x, ones(len(x)))).T
        Ay = vstack((y, ones(len(y)))).T
        self.scale_x, self.offset_x = linalg.lstsq(Ax, x_map)[0]
        self.scale_y, self.offset_y = linalg.lstsq(Ay, y_map)[0]

        # import matplotlib
        # matplotlib.use('Agg')
        # import matplotlib.pyplot as plt

        # x_tomap = [(a * self.scale_x) + self.offset_x for a in x]
        # y_tomap = [(a * self.scale_y) + self.offset_y for a in y]

        # plotting conversion output for debugging purposes
        # fig, axarr = plt.subplots(nrows = 2, ncols = 2)
        # axarr[0][0].scatter(x_tomap, y_tomap)
        # axarr[0][1].scatter(x_map, y_map)
        # axarr[1][0].scatter(x, y)

        # plt.savefig("output/towers.png", figsize=(12, 4), dpi=150)
        

    def draw_circle_world_coordinates(self, worldX, worldY, r=20, color="red"):
        """
            draws a circle at the specified world coordinates (from bottom-left) with radius r (in px) and the color as required by PIL
        """
        x, y = self.convert_coordinates(worldX, worldY)
        bounds = (x-r, self.map_h-(y+r), x+r, self.map_h-(y-r))
        bounds = tuple(int(round(a)) for a in bounds)
        self.draw.ellipse(bounds, fill = color)

    def draw_circle_world_coordinates_list(self, coordinates, r=20, color="red"):
        """
            same as draw_circle_world_coordinates, but for batch drawing
        """
        for x, y in coordinates:
            self.draw_circle_world_coordinates(x, y, r, color)

    def draw_circle_map_coordinates(self, x, y, r=20, color="red"):
        """
            draws a circle on the specified pixels (from bottom-left) with radius r (in px) and the color as required by PIL
        """
        bounds = (x-r, self.map_h-(y+r), x+r, self.map_h-(y-r))
        bounds = tuple(int(round(a)) for a in bounds)
        self.draw.ellipse(bounds, fill = color)

    def draw_circle_map_coordinates_list(self, coordinates, r=20, color="red"):
        """
            same as draw_circle_map_coordinates, but for batch drawing
        """
        for x, y in coordinates:
            self.draw_circle_map_coordinates(x, y, r, color)

    def save(self, filename, scale=4):
        """
            saves the map
        """
        del self.draw
        scaled = self.image.resize((self.map_w / scale, self.map_h / scale), Image.ANTIALIAS)
        scaled.save(filename)     

    def convert_coordinates(self, worldX, worldY):
        """
            converts world coordinates to map coordinates by using the scale and offset defined in the __init__ method
        """
        return (worldX * self.scale_x) + self.offset_x, (worldY * self.scale_y) + self.offset_y