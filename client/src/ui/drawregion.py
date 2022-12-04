from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.mindmap import MainScreen
    from ui.node import Node

from kivy.uix.stencilview import StencilView
from kivy.properties import ObjectProperty

from ui.drawingplane import DrawingPlane

import service.drawingplaneservice as service
import service.transferable as transfer

from kivy.core.window import Window
from kivy.lang import Builder

Builder.load_file('ui/kv/drawregion.kv')

class DrawRegion(StencilView):
    mainScreen: MainScreen = ObjectProperty(None)
    currentDrawingPlane: DrawingPlane = ObjectProperty(None)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.bind(size=self.drawRegion_size_changed)
        Window.bind(on_request_close = self.ask_before_closing)

    def drawRegion_size_changed(self, instance, value) -> None:
        if self.size[0] > 100 and self.size[1] > 100 :
            self.currentDrawingPlane.recenter_plane()

    def set_drawingPlane(self, plane: DrawingPlane) -> None:
        plane.drawRegion = self
        self.change_nodeList(plane.nodeList)
        plane.bind(nodeList = self.when_node_list_changed)
        self.currentDrawingPlane = plane
        self.add_widget(self.currentDrawingPlane)
        self.currentDrawingPlane.recenter_plane()

    def new_drawingPlane(self) -> None:
        plane: DrawingPlane = DrawingPlane()
        self.remove_widget(self.currentDrawingPlane)
        self.set_drawingPlane(plane)

    def load_drawingPlane(self, planeName: str) -> None:
        plane: DrawingPlane = self.get_drawingPlane(planeName)
        self.remove_widget(self.currentDrawingPlane)
        self.set_drawingPlane(plane)

    def on_kv_post(self, source) -> None:
        plane: DrawingPlane = self.get_default_drawingPlane()
        self.set_drawingPlane(plane)
        self.currentDrawingPlane.initialRecenterDone = False

    def get_drawingPlane(self, planeName: str) -> DrawingPlane:
        plane: DrawingPlane = transfer.to_plane(service.get_plane_by_name(planeName))
        return plane

    def ask_before_closing(self, source) -> bool:
        print("Add popup before closing")
        return False

    def when_node_list_changed(self, plane: DrawingPlane, nodeList: list[Node]) -> None:
        self.change_nodeList(nodeList)

    def change_nodeList(self, nodeList: list[Node]) -> None:
        self.mainScreen.leftSideBar.update_nodes(nodeList)
  
    def get_default_drawingPlane(self) -> DrawingPlane:
        plane: DrawingPlane = DrawingPlane()
        return plane

        # plane: DrawingPlane = transfer.to_plane(service.get_default_plane())
        # return plane