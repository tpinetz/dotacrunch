import io

from smoke.io.wrap import demo as io_wrp_dm
from smoke.replay import demo as rply_dm

from const import HEROES

from drawer import MapDrawer

from copy import deepcopy

class ReplayParser():
    """
        A class that provides an interface for skimming through a replay's data
    """
    def __init__(self, demofile):
        self.demofile = demofile

        demofile_io = io.open(self.demofile, 'rb')

        # reading demofile 
        demo_io = io_wrp_dm.Wrap(demofile_io)
        demo_io.bootstrap() 
        self.demo = rply_dm.Demo(demo_io)
        self.demo.bootstrap()

        # storing some general info tables
        self.received_tables = self.demo.match.recv_tables
        self.class_info = self.demo.match.class_info
        self.game_meta_tables = self.received_tables.by_dt['DT_DOTAGamerulesProxy']
        self.game_status_index = self.game_meta_tables.by_name['dota_gamerules_data.m_nGameState']
        self.npc_info_table = self.received_tables.by_dt['DT_DOTA_BaseNPC']

        self.general_data = {"file" : self.demofile}
        self.parse_general_data()

    def get_mapdrawer(self):
        """
            returns a mapdrawer instance for drawing on a dota2map with the replay of this instance
            YOU HAVE TO FINISH ONE ITERATION OF read_replay_data BEFORE CALLING THIS FUNCTION
        """
        if not hasattr(self, "tower_data"):
            raise Exception("Cannot call this function before completing one read_replay_data iteration!")

        return MapDrawer(self.tower_data, self.received_tables)

    def read_general_data(self):
        """ 
            returns a dictionary with general data about the replay
        """        
        return self.general_data

    def parse_general_data(self):
        """
            reads general data from demofile and stores it in self.general_data
        """
        for tick in self.demo.play():
            if not hasattr(self, "tower_data"):
                self.tower_data = tick.entities.by_cls[self.class_info['DT_DOTA_BaseNPC_Tower']]

            break

    def read_replay_data(self, interval = 5):
        """
            reads the info of one tick and returns it, use it in a for loop
            @param interval: interval in seconds between ticks
        """

        timedelta = 0
        i = 0

        # general data
        for tick in self.demo.play():
            tick_data = {
                "heroes" : {}
            }

            # getting infos about tick
            game_meta = tick.entities.by_cls[self.class_info['DT_DOTAGamerulesProxy']][0].state
            current_game_status = game_meta.get(self.game_status_index)

            # only count data after game has started
            if current_game_status < 5:
                continue

            # time
            time = game_meta.get(self.game_meta_tables.by_name['dota_gamerules_data.m_fGameTime'])
            if timedelta is 0:
                timedelta = time
            time = time - timedelta # minutes = round((time / 60) * 10) / 10
            tick_data["time"] = time

            if time < i * interval:
                continue
            i = i + 1

            # heroes
            hero_list = self.get_hero_info_for_tick(tick.entities)
            for hero_id, name, handle in hero_list:
                hero_data = tick.entities.by_ehandle[handle].state

                position_x_index = self.npc_info_table.by_name['m_cellX']
                position_y_index = self.npc_info_table.by_name['m_cellY']
                position_vector_index = self.npc_info_table.by_name['m_vecOrigin']

                worldX = hero_data.get(position_x_index) + hero_data.get(position_vector_index)[0]/128.
                worldY = hero_data.get(position_y_index) + hero_data.get(position_vector_index)[0]/128.

                tick_data["heroes"][name] = {
                    "name" : name,
                    "worldX" : worldX,
                    "worldY" : worldY,
                    "hero_id" : hero_id
                }

            yield tick_data

    def get_hero_info_for_tick(self, entities):
        """
            Maps the hero_ids from the replay entities to the respective m_nGameState
            @param entities: entities table
        """
        world_data = entities.by_cls[self.class_info['DT_DOTA_PlayerResource']]
        rt = self.received_tables.by_dt['DT_DOTA_PlayerResource']
        current_data = world_data[0].state
        hero_data = []

        for i in range(10):
            hero_ehandle_index = rt.by_name['m_hSelectedHero.{:04d}'.format(i)]
            hero_ehandle = current_data.get(hero_ehandle_index)

            hero_id_index = rt.by_name['m_nSelectedHeroID.{:04d}'.format(i)]
            hero_id = current_data.get(hero_id_index)
            
            hero_data.append((hero_id, HEROES[hero_id]["name"], hero_ehandle))

        return hero_data