from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class VocationSelectScreen(Screen):
    def __init__(self, **kwargs):
        super(VocationSelectScreen, self).__init__(**kwargs)
        box = BoxLayout()
        box.orientation = "vertical"
        box.size_hint = (0.5, 0.5)
        box.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.add_widget(box)

        box.add_widget(Label(text="Vocation"))

        vocations = ["Master Sorcerer", "Elder Druid", "Elite Knight", "Royal Paladin"]
        for voc in vocations:
            box.add_widget(Button(text=voc, on_press=lambda e, v=voc: self.select_vocation(v)))

    def select_vocation(self, vocation):
        self.manager.selected_vocation = vocation
        self.manager.current = "GameScreen"
