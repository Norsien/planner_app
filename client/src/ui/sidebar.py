from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.mindmap import MainScreen
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty, OptionProperty, ListProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button

from ui.node import Node
from ui.drawingplane import DrawingPlane
from ui.hoverablebutton import HoverableToggleButton, HoverableButton
from ui.modifyplanepopup import AddNewPlanePopup, EditPlanePopup, DeleteNodePopup, DeletePlanePopup

from kivy.lang import Builder

Builder.load_file('ui/kv/sidebar.kv')

class SideBar(BoxLayout):
    mainScreen: MainScreen = ObjectProperty()

    is_opened: bool = BooleanProperty(False)
    background_color: list[float, float, float] = ListProperty([.4, .4, .5, 1])

    def open_sideBar(self) -> None:
        self.is_opened = True

    def close_sideBar(self) -> None:
        self.is_opened = False

    def toggle_sideBar(self) -> None:
        self.is_opened = not self.is_opened

def string_contains_phrase(string: str, phrase: str) -> bool:
    string: str = string.lower()
    phrase: str = phrase.lower()
    return phrase in string

class NodeListSideBar(SideBar):
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
                if string_contains_phrase(node.name, phrase):
                    self.nodeList.add_widget(NodeItem(self, node))

    def update_when_node_changed(self, node: Node, name: str) -> None:
        self.update_nodeList()

class NodeItem(HoverableToggleButton):
    node: Node = ObjectProperty()
    nodeName: str = StringProperty()
    sideBar: NodeListSideBar = ObjectProperty()

    def __init__(self, sideBar: NodeListSideBar, node: Node, **kwargs) -> None:
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

class PlaneListSideBar(SideBar):
    mainScreen = ObjectProperty(None)
    addPlaneButton: Button = ObjectProperty(None)

    planes: list[DrawingPlane] = ListProperty([])
    planeList: BoxLayout = ObjectProperty()
    filterField: TextInput = ObjectProperty(None)
    currentFilter: str = StringProperty("")

    def update_planes(self, planes: list[DrawingPlane]) -> None:
        self.planes = planes
        self.update_planeList()

    def handle_filter(self) -> None:
        self.currentFilter = self.filterField.text
        self.update_planeList()

    def update_planeList(self) -> None:
        for plane in self.planes:
            plane.bind(name=self.update_when_plane_changed)
            plane.bind(nodeList=self.update_when_plane_changed)
        if self.currentFilter == None or self.currentFilter == "":
            self.planeList.clear_widgets()
            for plane in self.planes:
                self.planeList.add_widget(PlaneItem(self.mainScreen, plane))
        else:
            phrase: str = self.currentFilter
            self.planeList.clear_widgets()
            for plane in self.planes:
                if string_contains_phrase(plane.name, phrase):
                    self.planeList.add_widget(PlaneItem(self.mainScreen, plane))

    def handle_addNewPlane(self) -> None:
        addNewPlanePopup: AddNewPlanePopup = AddNewPlanePopup(self.mainScreen)
        addNewPlanePopup.open()
    
    def update_when_plane_changed(self, plane: DrawingPlane, name: str) -> None:
        self.update_planeList()

class PlaneItem(RelativeLayout):
    mainScreen: MainScreen = ObjectProperty()

    planeItemButton: PlaneItemButton = ObjectProperty()
    plane: DrawingPlane = ObjectProperty()
    planeName: str = StringProperty()
    nodeCount: int = NumericProperty()
    isCurrentPlane: bool = BooleanProperty()

    def __init__(self, mainScreen: MainScreen, plane: DrawingPlane, **kwargs) -> None:
        super().__init__(**kwargs)
        self.plane = plane
        self.planeName = self.plane.name
        self.mainScreen = mainScreen
        self.nodeCount = len(self.plane.nodeList)
        plane.set_myButtonOnPlaneList(self)
        self.change_highligt(plane.isCurrentPlane)

    def handle_edit(self) -> None:
        editlanePopup: EditPlanePopup = EditPlanePopup(self.mainScreen, self.plane)
        editlanePopup.open()

    def handle_delete(self) -> None:
        if self.isCurrentPlane:
            return
        DeletePlanePopup(self.plane, self.mainScreen)

    def change_highligt(self, isCurrentPlane) -> None:
        self.isCurrentPlane = isCurrentPlane
        if isCurrentPlane:
            self.planeItemButton.button_color = self.planeItemButton.highlight_color
        else:
            self.planeItemButton.button_color = self.planeItemButton.default_color

class PlaneItemButton(Button):
    mainScreen: MainScreen = ObjectProperty()
    plane: DrawingPlane = ObjectProperty()
    sideBar: PlaneListSideBar = ObjectProperty()
    button_color: tuple[float, float, float, float]

    def select_plane(self) -> None:
        self.mainScreen.planePackage.set_topPlane(self.plane)
        self.mainScreen.drawRegion.display_topPlane()

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
        
    def set_fields(self, node: Node) -> None:
        self.set_field("nameField", str(node.name))
        self.set_field("descriptionField", str(node.shortDescription))

    def clear_fields(self) -> None:
        self.set_field("nameField", "")
        self.set_field("descriptionField", "")

    def delete_current_node(self) -> None:
        if self.currentSelectedNode != None:
            DeleteNodePopup(self.currentSelectedNode)

    def do_stuff_before_swapping(self) -> None:
        self.nameField.focus = False
        self.descriptionField.focus = False

class PropertyTextInput(TextInput):
    sideBar: sideBar = ObjectProperty(None)

    def on_focus(self, what, value) -> None:
        if value == False:
            print(self.property, self.sideBar.currentSelectedNode)
            setattr(self.sideBar.currentSelectedNode, self.property, self.text)

    