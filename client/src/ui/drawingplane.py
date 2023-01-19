from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.drawregion import DrawRegion
    from ui.sidebar import PlaneItem

from ui.node import Node
from ui.visualwidgetborder import VisualWidgetBorder

from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.image import Image
from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty, ListProperty, OptionProperty, StringProperty
from kivy.graphics.transformation import Matrix

from math import floor

from kivy.core.window import Window
from kivy.lang import Builder

from kivy.lang import Builder

Builder.load_file('ui/kv/drawingplane.kv')

class DrawingPlane(ScatterLayout):
    drawRegion: DrawRegion = ObjectProperty(None)

    initialRecenterDone: bool = BooleanProperty(False)
    previousParentWidth: int = NumericProperty()
    previousParentHeight: int = NumericProperty()
    previousParentPosX: int = NumericProperty()
    previousParentPosY: int = NumericProperty()
    currentNodeMode: str = OptionProperty("None", options=["None", "Add", "Connect", "Delete"])
    zoomOptions: list[float] = ListProperty((0.5, 0.7, 0.85, 1, 1.2, 1.4, 1.7, 2.0))
    currentZoomLevel: int = NumericProperty(3)
    borderVisible: bool = BooleanProperty(False)
    currentCursorPosition: list[int] = ListProperty(None)

    isCurrentPlane: bool = BooleanProperty(False)
    myButtonOnPlaneList: PlaneItem = ObjectProperty()
    currentSelectedNode: Node = ObjectProperty(None, allownone = True)
    backgroundImage: Image = ObjectProperty(None)
    name: str = StringProperty("")
    nodeList: list[Node] = ListProperty([])

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.bind(currentSelectedNode=self.when_node_selected_behaviour)

    def set_myButtonOnPlaneList(self, button: PlaneItem) -> None:
        self.myButtonOnPlaneList = button

    # # should be limited to once every 1/30 sec
    def recenter_plane(self) -> None:
        if not self.initialRecenterDone:
            pos_x: int = (self.width/2 - self.drawRegion.pos[0] - self.drawRegion.width/2)
            pos_y: int = (self.height/2 - self.drawRegion.pos[1] - self.drawRegion.height/2)
            self.pos: tuple[int, int] = (-pos_x, -pos_y)
            self.previousParentWidth = self.drawRegion.width
            self.previousParentHeight = self.drawRegion.height
            self.previousParentPosX = self.drawRegion.pos[0]
            self.previousParentPosY = self.drawRegion.pos[1]

            self.initialRecenterDone = True
        else:

            self.apply_transform(Matrix().translate((self.drawRegion.width - self.previousParentWidth +\
                                                     2*(self.drawRegion.pos[0] - self.previousParentPosX))/2, \
                                                    (self.drawRegion.height - self.previousParentHeight +\
                                                     2*(self.drawRegion.pos[1] - self.previousParentPosY))/2, 0))
            self.previousParentWidth = self.drawRegion.width
            self.previousParentHeight = self.drawRegion.height
            self.previousParentPosX = self.drawRegion.pos[0]
            self.previousParentPosY = self.drawRegion.pos[1]
    
    def on_touch_down(self, touch, **kwargs) -> None:
        if self.collide_point(*touch.pos):
            if self.currentNodeMode == "Add":
                if touch.button == "left":
                    self.create_new_node(self.to_local(touch.x, touch.y))
                    self.reset_mode()
            if touch.is_mouse_scrolling:
                if touch.button == 'scrollup':
                    self.change_scale(touch, -1)
                elif touch.button == 'scrolldown':
                    self.change_scale(touch, 1)
            else:
                super().on_touch_down(touch)

    def when_node_selected_behaviour(self, instance, value) -> None:
        if self.currentSelectedNode == None:
            self.drawRegion.mainScreen.rightSideBar.set_node_to_edit(None)
            self.drawRegion.mainScreen.rightSideBar.close_sideBar()
        else:
            self.drawRegion.mainScreen.rightSideBar.set_node_to_edit(self.currentSelectedNode)
            self.drawRegion.mainScreen.rightSideBar.open_sideBar()  

    def change_scale(self, touch, val: int) -> None:
        newZoomLevel: int = self.currentZoomLevel + val
        if newZoomLevel < 0:
            newZoomLevel = 0
        elif newZoomLevel >= len(self.zoomOptions):
            newZoomLevel = len(self.zoomOptions) - 1
        scale: float = self.zoomOptions[newZoomLevel]/self.zoomOptions[self.currentZoomLevel]
        self.apply_transform(Matrix().scale(scale, scale, scale), anchor=touch.pos)
        self.currentZoomLevel = newZoomLevel

    def enable_mode(self, mode: str) -> None:
        self.currentNodeMode = mode

    def reset_mode(self) -> None:
        self.currentNodeMode = "None"
        self.drawRegion.mainScreen.bottomBar.createNodeButton.reset_button()

    def set_border_visibility(self, val: bool) -> None:
        self.borderVisible = val

    def get_coordinates(self, window, pos) -> None:
        if self.collide_point(*pos):
            pos_x: int = (self.to_local(pos[0], pos[1])[0])
            pos_y: int = (self.to_local(pos[0], pos[1])[1])
            pos: tuple[int, int] = floor(pos_x), floor(pos_y)
            self.currentCursorPosition = pos
            self.drawRegion.mainScreen.bottomBar.set_positionDisplay_value(pos)

    def set_plane_name(self, planeName: str) -> None:
        self.name = planeName

    def create_new_node(self, pos) -> None:
        newNode: Node = Node(pos)
        self.put_node(newNode)

    def put_node(self, node: Node) -> None:
        self.nodeList.append(node)
        self.draw_a_node(node)

    def draw_a_node(self, node) -> None:
        if node.pos != None:
            node.set_drawingPlane(self)
            self.add_widget(node)

    def to_dict(self) -> dict[str, any]:
        node_list: list[dict[str, any]] = []
        for node in self.nodeList:
            node_list.append(node.to_dict())

        plane_dictionary: dict[str, any] = {
            "name": self.name,
            "height": self.height,
            "width": self.width,
            "elements": node_list
        }
        return plane_dictionary