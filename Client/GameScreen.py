from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.core.image import Image
from kivy.clock import Clock
from kivy.config import Config


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.add_widget(MapWidget())
        #self.add_widget(ChatWidget())
        #self.add_widget(InventoryWidget())


class MapWidget(Widget):
    tile_columns = 15
    tile_rows = 11
    tile_diameter = 32
    x_pos_offset = 0
    y_pos_offset = 0

    def __init__(self, **kwargs):
        super(MapWidget, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_ui, 1.0 / 60.0)
        self.y_pos_offset = float(Config.get("graphics", "height")) - (self.tile_diameter * self.tile_rows)

    def update_ui(self, dt):
        with self.canvas:
            # Draw map tiles.
            for x in range(self.tile_columns):
                for y in range(self.tile_rows):
                    tile_pos_x = (x * self.tile_diameter) + self.x_pos_offset
                    tile_pos_y = (y * self.tile_diameter) + self.y_pos_offset
                    Rectangle(source="Assets/grass.png", pos=(tile_pos_x, tile_pos_y), size=(self.tile_diameter, self.tile_diameter))


class ChatWidget(Widget):
    def __init__(self, **kwargs):
        super(ChatWidget, self).__init__(**kwargs)


class InventoryWidget(Widget):
    def __init__(self, **kwargs):
        super(InventoryWidget, self).__init__(**kwargs)
