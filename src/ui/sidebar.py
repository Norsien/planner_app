from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from ui.node import Node

from kivy.lang import Builder

Builder.load_file('ui/kv/sidebar.kv')

class SideBar(BoxLayout):
    is_opened = BooleanProperty(False)

class LeftSideBar(SideBar):
    pass

class RightSideBar(SideBar):
    nameField = ObjectProperty(None)
    nodeIdField = ObjectProperty(None)
    descriptionField = ObjectProperty(None)

    currentNode = ObjectProperty(None, allownone = True)

    def open_sideBar(self):
        self.is_opened = True

    def set_node_to_edit(self, nodeData):
        self.currentNode = nodeData
        self.display_node_properties()

    def display_node_properties(self):
        if self.currentNode != None:
            self.set_nameField()
            self.set_nodeIdField()
            self.set_descriptionField()

    def set_nameField(self):
        self.nameField.text = str(self.currentNode.name)

    def set_nodeIdField(self):
        self.nodeIdField.text = str(self.currentNode.nodeId)

    def set_descriptionField(self):
        self.descriptionField.text = str(self.currentNode.shortDescription)

    def close_sideBar(self):
        self.is_opened = False