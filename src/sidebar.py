from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from node import Node

class SideBar(BoxLayout):
    is_opened = BooleanProperty(False)

class LeftSideBar(SideBar):
    pass

class RightSideBar(SideBar):

    def open_sideBar(self):
        self.is_opened = True

    def set_node_to_edit(self, nodeData):
        pass

    def close_sideBar(self):
        self.is_opened = False

