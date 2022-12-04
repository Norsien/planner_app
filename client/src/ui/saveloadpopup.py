from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.mindmap import MainScreen

from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, OptionProperty

from ui.hoverablebutton import HoverableButton
from service.drawingplaneservice import get_plane_list, check_plane_by_name, create_plane, update_plane, delete_plane_by_name

from kivy.core.window import Window
from kivy.lang import Builder

Builder.load_file('ui/kv/saveloadpopup.kv')

class SaveReminderPopup(Popup):
    mainScreen: MainScreen = ObjectProperty()

    actionTypeString: str = StringProperty("")
    answer: str = OptionProperty("cancel", options = ["cancel", "yes", "no"])

    def __init__(self, mainScreen: MainScreen, actionType: str = "Before leaving", **kwargs) -> None:
        super().__init__(**kwargs)
        self.actionTypeString = actionType
        self.mainScreen = mainScreen
    
    def save_the_changes(self) -> None:
        pass

    def do_not_save_the_changes(self) -> None:
        self.answer = "no"
        self.dismiss()

    def save_the_changes(self) -> None:
        self.answer = "yes"
        self.dismiss()

class SaveLoadPopup(Popup):
    mainScreen: MainScreen = ObjectProperty()
    planeList: BoxLayout = ObjectProperty()
    nameField: TextInput = ObjectProperty()

    actionTypeString: str = StringProperty("")
    is_wide: bool = BooleanProperty(False)

    def __init__(self, mainScreen: MainScreen, **kwargs) -> None:
        super().__init__(**kwargs)
        self.mainScreen = mainScreen
        self.set_plane_name(self.mainScreen.drawRegion.currentDrawingPlane.name)

    def show_saves_from_server(self) -> None:
        self.get_planes_list()
        self.width: int = 600
        self.is_wide = True

    def get_planes_list(self) -> None:
        # try 
        planes: dict[str, any] = get_plane_list()
        # catch

        self.planeList.clear_widgets()
        for plane in planes:
            self.planeList.add_widget(ListItem(self, planeName=plane["name"]))

    def reload_plane_list(self) -> None:
        self.get_planes_list()

    def set_plane_name(self, planeName: str) -> None:
        self.nameField.text = planeName        

    def get_plane_name(self) -> str:
        return self.nameField.text

    def handle_submit(self) -> None:
        pass

class SavePlanePopup(SaveLoadPopup):
    def __init__(self, mainScreen: MainScreen, **kwargs) -> None:
        super().__init__(mainScreen, **kwargs)
        self.actionTypeString = "Save as..."

    def handle_submit(self) -> None:
        planeName: str = self.get_plane_name()
        planeData: dict[str, any] = self.mainScreen.drawRegion.currentDrawingPlane.to_dict()
        remotePlane: dict[str, any] = check_plane_by_name(planeName)
        if remotePlane == None:
            self.mainScreen.drawRegion.currentDrawingPlane.set_plane_name(planeName)
            planeData["name"] = planeName
            self.save_new_plane(planeData)
            self.dismiss()
        elif planeData["name"] == remotePlane["name"]:
            self.update_plane(planeData)
            self.dismiss()
        else:
            overwritePopup: OverwriteConfirmationPopup = OverwriteConfirmationPopup(self, planeToOverwirte = planeName, planeData = planeData)
            overwritePopup.bind(on_dismiss=self.handle_overwrite)
            overwritePopup.open()

    def handle_overwrite(self, overwritePopup: OverwriteConfirmationPopup) -> None:
        if overwritePopup.confirmed:
            planeData: dict[str, any] = overwritePopup.planeData
            self.mainScreen.drawRegion.currentDrawingPlane.set_plane_name(overwritePopup.planeName)
            planeData["name"] = overwritePopup.planeName
            self.update_plane(planeData)
            self.dismiss()

    def save_new_plane(self, planeData: dict[str, any]) -> None:
        result: dict[str, any] = create_plane(planeData)
        self.reload_plane_list()

    def update_plane(self, planeData: dict[str, any]) -> None:
        result: dict[str, any] = update_plane(planeData)
        self.reload_plane_list()

class LoadPlanePopup(SaveLoadPopup):
    def __init__(self, mainScreen: MainScreen, **kwargs) -> None:
        super().__init__(mainScreen, **kwargs)
        self.actionTypeString = "Load from..."

    def handle_submit(self) -> None:
        planeName: str = self.get_plane_name()
        remotePlane: dict[str, any] = check_plane_by_name(planeName)
        if remotePlane == None:
            print("Plane does not exist popup, add authorization")
            return
        else:
            self.mainScreen.drawRegion.load_drawingPlane(planeName)
            self.dismiss()

class PopupButton(HoverableButton):
    def mouseover_highlight(self) -> None:
        self.button_color = self.highlight_color

    def reset_highlight(self) -> None:
        self.button_color = self.default_color

class ListItem(RelativeLayout):
    planeName: str = StringProperty("")
    itemLastEditDate: str = StringProperty()
    popupParent: SavePlanePopup = ObjectProperty()

    def __init__(self, popupParent: SavePlanePopup, planeName: str = '', **kwargs) -> None:
        super().__init__(**kwargs)
        self.planeName = planeName
        self.popupParent = popupParent

    def set_text_to_field(self) -> None:
        self.popupParent.set_plane_name(self.planeName)

    def delete_plane(self) -> None:
        deletePlanePopup: DeleteConfirmationPopup = DeleteConfirmationPopup(self.popupParent, planeToDelete=self.planeName)
        if (self.planeName!='dev'):
            deletePlanePopup.open()
        else:
            print("TODO delte this after unmocking dev plane")


class DeleteConfirmationPopup(Popup):
    planeName: str = StringProperty("")
    popupParent: SavePlanePopup = ObjectProperty()

    def __init__(self, popupParent: SavePlanePopup, planeToDelete: str = '', **kwargs) -> None:
        super().__init__(**kwargs)
        self.planeName = planeToDelete
        self.popupParent = popupParent
    
    def confirm_delete(self) -> None:
        #try
        result: dict[str, any] = delete_plane_by_name(self.planeName)
        #catch
        if result["success"] == True:
            self.popupParent.reload_plane_list()
            self.dismiss()
        else:
            ErrorPopup(message="Could not delete specified plane from server.")

class OverwriteConfirmationPopup(Popup):
    planeName: str = StringProperty("")
    planeData: dict[str, any] = ObjectProperty()
    popupParent: SavePlanePopup = ObjectProperty()
    confirmed: bool = BooleanProperty(False)

    def __init__(self, popupParent: SavePlanePopup, planeToOverwirte: str = '', planeData = {}, **kwargs) -> None:
        super().__init__(**kwargs)
        self.planeName = planeToOverwirte
        self.planeData = planeData
        self.popupParent = popupParent

    def confirm_overwrite(self) -> None:
        self.confirmed = True
        self.dismiss()


class ErrorPopup(Popup):
    message: str = StringProperty("")

    def __init__(self, message="Unspecified information.",**kwargs) -> None:
        super().__init__(**kwargs)
        self.message = message
        self.open()
