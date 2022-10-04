from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout

class SideBar(BoxLayout):
    pass

class LeftSideBar(SideBar):
    pass

class RightSideBar(SideBar):
    is_visible = BooleanProperty(False)
    pass