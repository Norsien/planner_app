from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.mindmap import MainScreen
    from ui.planepackage import PlanePackage

from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, OptionProperty

from service.planepackageservice import (
    get_planePackage_list,
    check_planePackage_name,
    create_planePackage,
    update_planePackage,
    delete_planePackage_by_name,
    get_planePackage_by_name
)
from service.transferable import to_planePackage
from ui.popupgenerics import ErrorPopup

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

    def do_not_save_the_changes(self) -> None:
        self.answer = "no"
        self.dismiss()

    def save_the_changes(self) -> None:
        self.answer = "yes"
        self.dismiss()

class SaveLoadPopup(Popup):
    mainScreen: MainScreen = ObjectProperty()
    packageList: BoxLayout = ObjectProperty()
    nameField: TextInput = ObjectProperty()

    actionTypeString: str = StringProperty("")
    is_wide: bool = BooleanProperty(False)

    def __init__(self, mainScreen: MainScreen, **kwargs) -> None:
        super().__init__(**kwargs)
        self.mainScreen = mainScreen
        # self.set_nameField_text(self.mainScreen.planePackage.get_planePackage_name())

    def show_saves_from_server(self) -> None:
        self.get_planePackage_list()
        self.width: int = 600
        self.is_wide = True

    def reload_planePackage_list(self) -> None:
        self.get_planePackage_list()

    def get_planePackage_list(self) -> None:
        try:
            packages: dict[str, any] = get_planePackage_list()
        except Exception as e:
            print(f'Exception of type: {type(e)}')
            ErrorPopup("Could not get package list from server.")
            return

        self.packageList.clear_widgets()
        for package in packages:
            self.packageList.add_widget(ListItem(self, name=package["name"]))

    def set_nameField_text(self, name: str) -> None:
        self.nameField.text = name        

    def get_nameField_text(self) -> str:
        return self.nameField.text

    def handle_submit(self) -> None:
        pass

    def show_not_implemented_message(self):
        ErrorPopup("Not implemented.")

class SavePlanePackagePopup(SaveLoadPopup):
    saveSuccess: bool = BooleanProperty(False)

    def handle_submit(self) -> None:
        packageName: str = self.get_nameField_text()
        packageData: dict[str, any] = self.mainScreen.planePackage.to_dict()
        try:
            remotePackage: dict[str, any] = check_planePackage_name(packageName)
        except Exception as e:
            print(f'Exception of type: {type(e)}')
            ErrorPopup("Error while trying to check package name on the server.")
            return
        if remotePackage == None:
            self.mainScreen.planePackage.set_planePackage_name(packageName)
            packageData["name"] = packageName
            self.save_new_package(packageData)
        elif packageData["name"] == remotePackage["name"]:
            self.update_package(packageData)
        else:
            overwritePopup: OverwriteConfirmationPopup = OverwriteConfirmationPopup(self, name=packageName, data=packageData)
            overwritePopup.bind(on_dismiss=self.handle_overwrite)
            overwritePopup.open()

    def handle_overwrite(self, overwritePopup: OverwriteConfirmationPopup) -> None:
        if overwritePopup.confirmed:
            packageData: dict[str, any] = overwritePopup.itemData
            self.mainScreen.planePackage.set_planePackage_name(overwritePopup.itemName)
            packageData["name"] = overwritePopup.itemName
            self.update_package(packageData)
            self.saveSuccess = True
            self.dismiss()

    def save_new_package(self, packageData: dict[str, any]) -> None:
        try: 
            result: dict[str, any] = create_planePackage(packageData)
        except Exception as e:
            print(f'Exception of type: {type(e)}')
            ErrorPopup("Could not save package on the server.")
            return
        self.reload_planePackage_list()
        self.saveSuccess = True
        self.dismiss()

    def update_package(self, packageData: dict[str, any]) -> None:
        try:
            result: dict[str, any] = update_planePackage(packageData)
        except Exception as e:
            print(f'Exception of type: {type(e)}')
            ErrorPopup("Could not save changes on the server.")
            return
        self.reload_planePackage_list()
        self.saveSuccess = True
        self.dismiss()

class LoadPlanePackagePopup(SaveLoadPopup):
    def handle_submit(self) -> None:
        packageName: str = self.get_nameField_text()
        try:
            remotePackage: dict[str, any] = check_planePackage_name(packageName)
        except Exception as e:
            print(f'Exception of type: {type(e)}')
            ErrorPopup("Error while trying to check package name on the server.")
            return
        if remotePackage == None:
            ErrorPopup("Package with such name does not exist.")
            return
        else:
            planeDict: dict[str, any] = get_planePackage_by_name(packageName)
            planePackage: PlanePackage = to_planePackage(planeDict)
            self.mainScreen.set_planePackage(planePackage)
            self.dismiss()

class ListItem(RelativeLayout):
    itemName: str = StringProperty("")
    itemLastEditDate: str = StringProperty()
    popupParent: SaveLoadPopup = ObjectProperty()

    def __init__(self, popupParent: SaveLoadPopup, name: str = '', **kwargs) -> None:
        super().__init__(**kwargs)
        self.itemName = name
        self.popupParent = popupParent

    def set_text_to_field(self) -> None:
        self.popupParent.set_nameField_text(self.itemName)

    def delete_package(self) -> None:
        deletePackagePopup: DeleteConfirmationPopup = DeleteConfirmationPopup(self.popupParent, self.itemName)
        deletePackagePopup.open()

class DeleteConfirmationPopup(Popup):
    itemName: str = StringProperty("")
    popupParent: SaveLoadPopup = ObjectProperty()

    def __init__(self, popupParent: SaveLoadPopup, name: str = '', **kwargs) -> None:
        super().__init__(**kwargs)
        self.itemName = name
        self.popupParent = popupParent
    
    def confirm_delete(self) -> None:
        try:
            result: dict[str, any] = delete_planePackage_by_name(self.itemName)
        except Exception as e:
            print(f'Exception of type: {type(e)}')
            ErrorPopup("Could not delete package from the server.")
            return
        if result["success"] == True:
            self.popupParent.reload_planePackage_list()
            self.dismiss()
        else:
            ErrorPopup("Could not delete package from server.")

class OverwriteConfirmationPopup(Popup):
    itemName: str = StringProperty("")
    itemData: dict[str, any] = ObjectProperty()
    popupParent: SaveLoadPopup = ObjectProperty()
    confirmed: bool = BooleanProperty(False)

    def __init__(self, popupParent: SaveLoadPopup, name: str = '', data = {}, **kwargs) -> None:
        super().__init__(**kwargs)
        self.itemName = name
        self.itemData = data
        self.popupParent = popupParent

    def confirm_overwrite(self) -> None:
        self.confirmed = True
        self.dismiss()
