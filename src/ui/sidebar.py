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

    def set_node_to_edit(self, node):
        self.do_stuff_before_swapping()
        self.currentSelectedNode = node
        self.display_node_properties()

    def display_node_properties(self):
        if self.currentSelectedNode != None:
            self.set_fields(self.currentSelectedNode)
        else:
            self.clear_fields()

    def set_field(self, field, value):
        if hasattr(self, field):
            textField = getattr(self, field)
            textField.text = value
        else:
            print("attr does not exist")
        
    def set_fields(self, node):
        self.set_field("nameField", str(node.name))
        self.set_field("nodeIdField", str(node.nodeId))
        self.set_field("descriptionField", str(node.shortDescription))

    def clear_fields(self):
        self.set_field("nameField", "")
        self.set_field("nodeIdField", "")
        self.set_field("descriptionField", "")

    def delete_current_node(self):
        if self.currentSelectedNode != None:
            print("delete pop up")
            self.currentSelectedNode.delete()

    def do_stuff_before_swapping(self):
        self.nameField.focus = False
        self.nodeIdField.focus = False
        self.descriptionField.focus = False

class PropertyTextInput(TextInput):
    sideBar = ObjectProperty(None)

    def on_focus(self, what, value):
        if value == False:
            print("Pora zmienic: ")
            print(self.property, self.sideBar.currentSelectedNode)
            setattr(self.sideBar.currentSelectedNode, self.property, self.text)

    