from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.mindmap import MainScreen

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.label import Label

from ui.hoverablebutton import HoverableButton
from ui.saveloadpopup import SaveReminderPopup, SavePlanePopup, LoadPlanePopup

from kivy.core.window import Window
from kivy.lang import Builder


Builder.load_file('ui/kv/topbar.kv')

class TopBar(BoxLayout):
    mainScreen: MainScreen = ObjectProperty(None)

    newPlaneButton: TopPanelButton = ObjectProperty(None)
    savePlaneButton: TopPanelButton = ObjectProperty(None)
    loadPlaneButton: TopPanelButton = ObjectProperty(None)

    # # touch blocker
    # def on_touch_down(self, touch):
    #     if self.collide_point(*touch.pos):
    #         return True
    #     else:
    #         return super().on_touch_down(touch)

    def newPlaneButton_pressed(self) -> None:
        #if anything changed
        doYouWantToSaveChangesPopup: SaveReminderPopup = SaveReminderPopup(mainScreen=self.mainScreen, actionTypeString="New plane")
        doYouWantToSaveChangesPopup.open()
        doYouWantToSaveChangesPopup.bind(on_dismiss = self.resolve_newPlane_saveRemainder)

    def resolve_newPlane_saveRemainder(self, saveRemainder: SaveReminderPopup ) -> None:
        answer: str = saveRemainder.answer
        if answer == 'no':
            self.mainScreen.drawRegion.new_drawingPlane()
        elif answer == 'yes':
            savePlanePopup: SavePlanePopup = SavePlanePopup(mainScreen=self.mainScreen)
            savePlanePopup.open()
            savePlanePopup.bind(on_dismiss = self.resolve_newPlane_afterSaving)

    def resolve_newPlane_afterSaving(self, savePlanePopup: SavePlanePopup) -> None:
        #TODO check success
        self.mainScreen.drawRegion.new_drawingPlane()

    def savePlaneButton_pressed(self) -> None:
        savePlanePopup: SavePlanePopup = SavePlanePopup(mainScreen=self.mainScreen, actionTypeString="Save as...")
        savePlanePopup.open()

    def loadPlaneButton_pressed(self) -> None:
        #if anything changed
        doYouWantToSaveChangesPopup: SaveReminderPopup = SaveReminderPopup(mainScreen=self.mainScreen, actionTypeString="Load from...")
        doYouWantToSaveChangesPopup.open()
        doYouWantToSaveChangesPopup.bind(on_dismiss = self.resolve_loadPlane_saveRemainder)

    def resolve_loadPlane_saveRemainder(self, saveRemainder: SaveReminderPopup ) -> None:
        answer: str = saveRemainder.answer
        if answer == 'no':
            self.open_load_panel()
        elif answer == 'yes':
            savePlanePopup: SavePlanePopup = SavePlanePopup(mainScreen=self.mainScreen)
            savePlanePopup.open()
            savePlanePopup.bind(on_dismiss = self.resolve_loadPlane_afterSaving)

    def resolve_loadPlane_afterSaving(self, savePlanePopup: SavePlanePopup) -> None:
        #TODO check success
        self.open_load_panel()

    def open_load_panel(self) -> None:
        loadPlanePopup: LoadPlanePopup = LoadPlanePopup(mainScreen=self.mainScreen, actionTypeString="Load from...")
        loadPlanePopup.open()

    def nodeListButton_pressed(self) -> None:
        self.mainScreen.leftSideBar.toggle_sideBar()

class TopPanelButton(HoverableButton):
    topBar: TopBar = ObjectProperty(None)
    
    def mouseover_highlight(self) -> None:
        self.button_color = .6, .6, .6, 1

    def reset_highlight(self) -> None:
        self.button_color = .45, .45, 0.45, 1