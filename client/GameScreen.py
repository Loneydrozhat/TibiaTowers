from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.core.image import Image
from kivy.clock import Clock
from kivy.config import Config
import socket
import struct
import threading
import pickle

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MapWidget())
        #self.add_widget(ChatWidget())
        #self.add_widget(InventoryWidget())


class MapWidget(Widget):
    tile_columns = 15
    tile_rows = 11
    tile_diameter = 32
    x_pos_offset = 0
    y_pos_offset = 0
    map_data = None
    socket_buffer_size = 1024
    force_thread_halt = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update_ui, 1.0 / 60.0)
        self.y_pos_offset = float(Config.get("graphics", "height")) - (self.tile_diameter * self.tile_rows)
        map_data_thread = threading.Thread(target=self.get_map_data)
        map_data_thread.start()

    def get_map_data(self):
        while not self.force_thread_halt:
            try:
                print("Connecting to server...")
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("127.0.0.1", 8000))
                print("Connected to server.")
                while not self.force_thread_halt:
                    try:
                        content_length = struct.unpack(">I", s.recv(4))[0]
                        recv_data = bytes()
                        while len(recv_data) < content_length:
                            recv_size = content_length - len(recv_data)
                            if recv_size > self.socket_buffer_size:
                                recv_size = self.socket_buffer_size
                            recv_data += s.recv(recv_size)
                        self.map_data = pickle.loads(recv_data)
                    except EOFError:
                        print("Error - Unexpected EOF.")
                    except pickle.UnpicklingError:
                        print("Error - Unpickling error.")
                    except ConnectionResetError:
                        print("Error - Connection was reset.")
                    except(EOFError, pickle.UnpicklingError, ConnectionResetError):
                        s.close()
                        break
            except ConnectionRefusedError:
                print("Error - Connection was refused.")

    def update_ui(self, dt):
        self.canvas.clear()
        if self.map_data is not None:
            render_from_x = int(self.map_data["PLAYER"]["X"] - ((self.tile_columns - 1) / 2))
            render_from_y = int(self.map_data["PLAYER"]["Y"] - ((self.tile_rows - 1) / 2))
            for col in range(self.tile_columns):
                for row in range(self.tile_rows):
                    # Draw map tiles.
                    object_lists = ["TILES", "OBJECTS", "SENTIENTS"]
                    for object_list in object_lists:
                        item = self.map_data[object_list][render_from_x + col][render_from_y + row]
                        if item is not None:
                            tile_source = "assets/{0}/{1}.png".format(object_list.lower(), item["TYPE"].lower())
                            tile_pos_x = (col * self.tile_diameter) + self.x_pos_offset
                            tile_pos_y = (row * self.tile_diameter) + self.y_pos_offset
                            rect = Rectangle(source=tile_source, pos=(tile_pos_x, tile_pos_y), size=(self.tile_diameter, self.tile_diameter))
                            self.canvas.add(rect)


class ChatWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class InventoryWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
