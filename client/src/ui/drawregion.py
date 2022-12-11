from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.mindmap import MainScreen
    from ui.node import Node

from kivy.uix.stencilview import StencilView
from kivy.properties import ObjectProperty

from ui.drawingplane import DrawingPlane

# import service.drawingplaneservice as service
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

    def drawRegion_size_changed(self, instance, value) -> None:
        if self.size[0] > 100 and self.size[1] > 100 :
            self.currentDrawingPlane.recenter_plane()

    def set_drawingPlane(self, plane: DrawingPlane) -> None:
        plane.drawRegion = self
        self.change_nodeList(plane.nodeList)
        plane.bind(nodeList = self.when_node_list_changed)
        if self.currentDrawingPlane:
            if self.currentDrawingPlane.currentSelectedNode:
                self.currentDrawingPlane.currentSelectedNode.reset_button()
                self.currentDrawingPlane.currentSelectedNode = None
            self.currentDrawingPlane.isCurrentPlane = False
            if self.currentDrawingPlane.myButtonOnPlaneList:
                self.currentDrawingPlane.myButtonOnPlaneList.change_highligt(False)
            self.currentDrawingPlane.unbind(nodeList = self.when_node_list_changed)
            Window.bind(mouse_pos=self.currentDrawingPlane.get_coordinates)
            self.remove_widget(self.currentDrawingPlane)
            plane.set_border_visibility(self.currentDrawingPlane.borderVisible)


        self.currentDrawingPlane = plane
        self.currentDrawingPlane.isCurrentPlane = True
        if self.currentDrawingPlane.myButtonOnPlaneList:
            self.currentDrawingPlane.myButtonOnPlaneList.change_highligt(True)
        self.add_widget(self.currentDrawingPlane)
        self.currentDrawingPlane.recenter_plane()
        Window.bind(mouse_pos=self.currentDrawingPlane.get_coordinates)

    def on_kv_post(self, source) -> None:
        self.mainScreen.set_planePackage_default()

    def display_topPlane(self) -> None:
        plane: DrawingPlane = self.mainScreen.planePackage.get_topPlane()
        if plane == self.currentDrawingPlane:
            return
        self.set_drawingPlane(plane)

    def when_node_list_changed(self, plane: DrawingPlane, nodeList: list[Node]) -> None:
        self.change_nodeList(nodeList)

    def change_nodeList(self, nodeList: list[Node]) -> None:
        self.mainScreen.nodeListSideBar.update_nodes(nodeList)