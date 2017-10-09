from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.add_widget(MapWidget())
        self.add_widget(ChatWidget())
        self.add_widget(InventoryWidget())


class MapWidget(Widget):
    def __init__(self, **kwargs):
        super(MapWidget, self).__init__(**kwargs)
        self.pos_hint = {"top": 1, "left": 1}
        with self.canvas.before:
            Rectangle(size=self.size, pos_hint = {"top": 1, "right": 1})


class ChatWidget(Widget):
    def __init__(self, **kwargs):
        super(ChatWidget, self).__init__(**kwargs)


class InventoryWidget(Widget):
    def __init__(self, **kwargs):
        super(InventoryWidget, self).__init__(**kwargs)
