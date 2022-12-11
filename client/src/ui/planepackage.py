from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.mindmap import MainScreen

from ui.drawingplane import DrawingPlane
from ui.popupgenerics import ErrorPopup
from kivy.uix.widget import Widget

from kivy.properties import StringProperty, ObjectProperty, ListProperty

class PlanePackage(Widget):
    mainScreen: MainScreen = ObjectProperty(None)

    name: str = StringProperty("")

    planeList: list[DrawingPlane] = ListProperty([])
    topPlane: DrawingPlane = ObjectProperty(None)

    def get_topPlane(self) -> DrawingPlane:
        if self.topPlane != None:
            return self.topPlane
        elif len(self.planeList) == 0:
            plane: DrawingPlane = DrawingPlane()
            plane.set_plane_name("plane")
            self.add_plane(plane)
        self.topPlane = self.planeList[0]
        return self.topPlane

    def add_plane(self, plane: DrawingPlane) -> None:
        if any(plane.name == pl.name for pl in self.planeList):
            ErrorPopup("Plane with this name already exists in this package.")
            return
        self.planeList.append(plane)

    def new_plane(self, name: str, width: int, height: int) -> None:
        plane: DrawingPlane = DrawingPlane()
        plane.name = name
        plane.width = width
        plane.height = height
        self.add_plane(plane)

    def delete_plane(self, plane: DrawingPlane):
        if plane == self.topPlane:
            ErrorPopup("Cannot remove current plane.")
            return
        if not plane in self.planeList:
            ErrorPopup("Plane is not a part of current plane package.")
            return
        self.planeList.remove(plane)

    def check_name_aviability(self, name: str) -> bool:
        if any(name == pl.name for pl in self.planeList):
            return False
        return True

    def set_topPlane(self, plane: DrawingPlane) -> None:
        self.topPlane = plane

    def set_planePackage_name(self, name: str) -> None:
        self.name = name

    def get_planePackage_name(self) -> str:
        return self.name

    def to_dict(self) -> dict[str, any]:
        plane_list: list[dict[str, any]] = []
        for plane in self.planeList:
            plane_list.append(plane.to_dict())

        planePackage_dictionary: dict[str, any] = {
            "name": self.name,
            "planes": plane_list,
            "topPlane": self.topPlane.name
        }
        return planePackage_dictionary


