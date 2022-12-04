from __future__ import annotations
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.relativelayout import RelativeLayout

from ui.node import Node
from ui.hoverablebutton import HoverableToggleButton

from kivy.lang import Builder

Builder.load_file('ui/kv/sidebar.kv')

class SideBar(BoxLayout):
    is_opened: bool = BooleanProperty(False)

    def open_sideBar(self) -> None:
        self.is_opened = True

    def close_sideBar(self) -> None:
        self.is_opened = False

    def toggle_sideBar(self) -> None:
        self.is_opened = not self.is_opened

    # # touch blocker
    # def on_touch_down(self, touch):
    #     if self.collide_point(*touch.pos):
    #         return True
    #     else:
    #         return super().on_touch_down(touch)

class LeftSideBar(SideBar):
    nodes: list[Node] = ListProperty([])
    nodeList: BoxLayout = ObjectProperty(None)
    filterField: TextInput = ObjectProperty(None)
    currentFilter: str = StringProperty("")

    def update_nodes(self, nodes: list[Node]) -> None:
        self.nodes = nodes
        self.update_nodeList()

    def handle_filter(self) -> None:
        self.currentFilter = self.filterField.text
        self.update_nodeList()
        
    def update_nodeList(self) -> None:
        for node in self.nodes:
            node.bind(name=self.update_when_node_changed)
        if self.currentFilter == None or self.currentFilter == "":
            self.nodeList.clear_widgets()
            for node in self.nodes:
                self.nodeList.add_widget(NodeItem(self, node))
        else:
            phrase: str = self.currentFilter
            self.nodeList.clear_widgets()
            for node in self.nodes:
                if self.string_contains_phrase(node.name, phrase):
                    self.nodeList.add_widget(NodeItem(self, node))

    def string_contains_phrase(self, string: str, phrase: str) -> bool:
        string: str = string.lower()
        phrase: str = phrase.lower()
        return phrase in string

    def update_when_node_changed(self, node: Node, name: str) -> None:
        self.update_nodeList()

class NodeItem(HoverableToggleButton):
    node: Node = ObjectProperty()
    nodeName: str = StringProperty()
    sideBar: LeftSideBar = ObjectProperty()

    def __init__(self, sideBar: LeftSideBar, node: Node, **kwargs) -> None:
        super().__init__(**kwargs)
        self.node = node
        self.nodeName = self.node.name
        self.sideBar = sideBar
        self.node.bind(state=self.set_state)

    def on_mouseover(self, window, pos) -> None:
        pass

    def set_state(self, node: Node, state: str) -> None:
        self.state = state

    def select_node(self) -> None:
        self.node.switch_state()

    def reset_highlight(self) -> None:
        self.button_color = self.default_color

    def pressed_highlight(self) -> None:
        self.button_color = self.highlight_color

class RightSideBar(SideBar):
    nameField: PropertyTextInput = ObjectProperty(None)
    descriptionField: PropertyTextInput = ObjectProperty(None)

    currentSelectedNode: Node = ObjectProperty(None, allownone = True)

    def set_node_to_edit(self, node: Node) -> None:
        self.do_stuff_before_swapping()
        self.currentSelectedNode = node
        self.display_node_properties()

    def display_node_properties(self) -> None:
        if self.currentSelectedNode != None:
            self.set_fields(self.currentSelectedNode)
        else:
            self.clear_fields()

    def set_field(self, field: str, value: str) -> None:
        if hasattr(self, field):
            textField: PropertyTextInput = getattr(self, field)
            textField.text = value
        else:
            print("attr does not exist")
        
    def set_fields(self, node: Node) -> None:
        self.set_field("nameField", str(node.name))
        self.set_field("descriptionField", str(node.shortDescription))

    def clear_fields(self) -> None:
        self.set_field("nameField", "")
        self.set_field("descriptionField", "")

    def delete_current_node(self) -> None:
        if self.currentSelectedNode != None:
            print("delete pop up")
            self.currentSelectedNode.delete()

    def do_stuff_before_swapping(self) -> None:
        self.nameField.focus = False
        self.descriptionField.focus = False

class PropertyTextInput(TextInput):
    sideBar: sideBar = ObjectProperty(None)

    def on_focus(self, what, value) -> None:
        if value == False:
            print("Zmiana property: ")
            print(self.property, self.sideBar.currentSelectedNode)
            setattr(self.sideBar.currentSelectedNode, self.property, self.text)

    