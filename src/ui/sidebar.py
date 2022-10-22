import imp
from turtle import textinput
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
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

    currentSelectedNode = ObjectProperty(None, allownone = True)

    def open_sideBar(self):
        self.is_opened = True

    def close_sideBar(self):
        self.is_opened = False

    def set_node_to_edit(self, nodeData):
        self.currentSelectedNode = nodeData
        self.display_node_properties()

    def display_node_properties(self):
        if self.currentSelectedNode != None:
            self.set_fields(self.currentSelectedNode)
        else:
            self.clear_fields()

    def set_nameField(self, text):
        self.nameField.text = text

    def set_nodeIdField(self, text):
        self.nodeIdField.text = text

    def set_descriptionField(self, text):
        self.descriptionField.text = text

    def set_fields(self, node):
        self.set_nameField(str(node.name))
        self.set_nodeIdField(str(node.nodeId))
        self.set_descriptionField(str(node.shortDescription))

    def clear_fields(self):
        self.set_nameField("")
        self.set_nodeIdField("")
        self.set_descriptionField("")

    def delete_current_node(self):
        if self.currentSelectedNode != None:
            print("delete pop up")
            self.currentSelectedNode.delete()

    def update_current_node(self):
        print("updating now")

class PropertyTextInput(TextInput):
    sideBar = ObjectProperty(None)

    def on_focus(self, what, value):
        if value == False:
            print("Validate input and save now")