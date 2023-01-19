from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.mindmap import MainScreen
    from ui.node import Node
    from kivy.uix.textinput import TextInput
    from ui.drawingplane import DrawingPlane
from re import match

from kivy.uix.popup import Popup
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from ui.popupgenerics import ErrorPopup

from kivy.lang import Builder

Builder.load_file('ui/kv/modifyplanepopup.kv')

MAX_WIDTH: int = 10000
MAX_HEIGHT: int = 10000
pattern: str = "^[A-Za-z0-9_-]*$"

class ModifyPlanePopup(Popup):
    mainScreen: MainScreen = ObjectProperty()

    nameField: TextInput = ObjectProperty()
    widthField: TextInput = ObjectProperty()
    heightField: TextInput = ObjectProperty()

    def __init__(self, mainScreen: MainScreen, **kwargs):
        super().__init__(**kwargs)
        self.mainScreen = mainScreen

    def handle_submit(self) -> None:
        pass

    def validate_properties(self, itemName = None) -> bool:
        if self.nameField.text == "":
            ErrorPopup("Name cannot be empty.")
            return False
        name: str = self.nameField.text
        if not bool(match(pattern, name)):
            ErrorPopup("Name can only contain letters, numbers, underscore and dash.")
            return False
        if itemName != name and not self.mainScreen.planePackage.check_name_aviability(name):
            ErrorPopup("Plane with this name already exists in this package.")
            return False
        if not self.widthField.text.isdigit():
            ErrorPopup("Width value is not an integer.")
            return False
        width: int = int(self.widthField.text)
        if width <= 0 or width > MAX_WIDTH:
            ErrorPopup("Width value is out of allowed bounds: (1, {})".format(MAX_WIDTH))
            return False
        if not self.heightField.text.isdigit():
            ErrorPopup("Height value is not an integer.")
            return False
        height: int = int(self.widthField.text)
        if height <= 0 or height > MAX_HEIGHT:
            ErrorPopup("Height value is out of allowed bounds: (1, {})".format(MAX_HEIGHT))
            return False
        return True
       
class AddNewPlanePopup(ModifyPlanePopup):
    def handle_submit(self) -> None:
        if not self.validate_properties():
            return
        self.mainScreen.planePackage.new_plane(
            self.nameField.text,
            int(self.widthField.text),
            int(self.heightField.text)
        )
        self.dismiss()

class EditPlanePopup(ModifyPlanePopup):
    plane: DrawingPlane = ObjectProperty()
    itemName: str = StringProperty("")
    
    def __init__(self, mainScreen: MainScreen, plane: DrawingPlane, **kwargs) -> None:
        super().__init__(mainScreen, **kwargs)
        self.plane = plane
        self.itemName = plane.name
        self.nameField.text = plane.name
        self.widthField.text = str(plane.width)
        self.heightField.text = str(plane.height)

    def handle_submit(self) -> None:
        if not self.validate_properties(self.itemName):
            return
        self.plane.name = self.nameField.text
        self.plane.width = int(self.widthField.text)
        self.plane.height = int(self.heightField.text)
        self.dismiss()

class DeletePlanePopup(Popup):
    mainScreen: MainScreen = ObjectProperty()

    itemName: str = StringProperty("")
    plane: Node = ObjectProperty()

    def __init__(self, plane: DrawingPlane, mainScreen: MainScreen,  **kwargs) -> None:
        super().__init__(**kwargs)
        self.plane = plane
        self.itemName = plane.name
        self.mainScreen = mainScreen
        self.open()
    
    def confirm_delete(self) -> None:
        self.mainScreen.planePackage.delete_plane(self.plane)
        self.dismiss()

class DeleteNodePopup(Popup):
    itemName: str = StringProperty("")
    node: Node = ObjectProperty()

    def __init__(self, node: Node, **kwargs) -> None:
        super().__init__(**kwargs)
        self.node = node
        self.itemName = node.name
        self.open()
    
    def confirm_delete(self) -> None:
        self.node.delete()
        self.dismiss()

