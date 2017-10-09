from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.config import Config


class VocationSelectScreen(Screen):
    def select_vocation(self, vocation):
        self.manager.selected_vocation = vocation
        self.manager.current = "GameScreen"


class GameScreen(Screen):
    def on_enter(self, *args):
        print(self.manager.selected_vocation)


class GameManager(ScreenManager):
    selected_vocation = None

    def setup(self):
        self.add_widget(VocationSelectScreen(name="VocationSelect"))
        self.add_widget(GameScreen(name="GameScreen"))


class TibiaTowersApp(App):
    def build(self):
        Config.set("graphics", "width", "400")
        Config.set("graphics", "height", "400")
        Config.set("graphics", "borderless", "0")
        gm = GameManager(transition=NoTransition())
        gm.setup()
        return gm


if __name__ == "__main__":
    TibiaTowersApp().run()
