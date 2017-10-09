from kivy.app import App
from kivy.uix.screenmanager import NoTransition
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager
from VocationSelectScreen import VocationSelectScreen
from GameScreen import GameScreen


class GameManager(ScreenManager):
    selected_vocation = None

    def __init__(self, **kwargs):
        super(GameManager, self).__init__(**kwargs)
        self.add_widget(VocationSelectScreen(name="VocationSelect"))
        self.add_widget(GameScreen(name="GameScreen"))


class TibiaTowersApp(App):
    def build(self):
        self.title = "Tibia Towers"
        Config.set("graphics", "width", "800")
        Config.set("graphics", "height", "800")
        Config.set("graphics", "borderless", "1")
        gm = GameManager(transition=NoTransition())
        return gm


if __name__ == "__main__":
    TibiaTowersApp().run()
