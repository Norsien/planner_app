from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.mindmap import MainScreen
    from kivy.uix.textinput import TextInput

from ui.hoverablebutton import HoverableToggleButton

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty

from kivy.core.window import Window
from kivy.lang import Builder

Builder.load_file('ui/kv/bottombar.kv')

class BottomBar(BoxLayout):
    # References to other widgets
    mainScreen: MainScreen = ObjectProperty(None)

    createNodeButton: NodeOptionsButton = ObjectProperty(None)
    connectNodesButton: NodeOptionsButton = ObjectProperty(None)
    deleteNodeButton: NodeOptionsButton = ObjectProperty(None)
    toggleBorderButton:BottomPanelButton = ObjectProperty(None)
    positionDisplay: TextInput = ObjectProperty(None)

    lastPosition: str = StringProperty("")
    currentNodeOptionButton: NodeOptionsButton = ObjectProperty(None, allownone = True)

    # # touch blocker
    # def on_touch_down(self, touch):
    #     if self.collide_point(*touch.pos):
    #         return True
    #     else:
    #         return super().on_touch_down(touch)

    def manage_nodeOptions_buttons(self) -> None:
        if self.currentNodeOptionButton == None:
            self.mainScreen.drawRegion.currentDrawingPlane.reset_mode()
        else:
            self.mainScreen.drawRegion.currentDrawingPlane.enable_mode(self.currentNodeOptionButton.buttonOption)

    def set_border_button(self, val) -> None:
        self.mainScreen.drawRegion.currentDrawingPlane.set_border_visibility(val)

    def set_positionDisplay_value(self, value: tuple(int, int)) -> None:
        if value != None:
            self.lastPosition = str(value)

    def display_position(self, dt) -> None:
        self.positionDisplay.text = self.lastPosition

class BottomPanelButton(HoverableToggleButton):
    # References to other widgets
    bottomBar: BottomBar = ObjectProperty(None)

    def reset_highlight(self) -> None:
        self.size = (30, 30)
        self.button_color = 0.3, 0.4, 0.9, 1

    def mouseover_highlight(self) -> None:
        self.size = (34, 34)
        self.button_color = 0.36, 0.48, 0.99, 1

    def pressed_highlight(self) -> None:
        self.size = (34, 34)
        self.button_color = 0.7, 0.6, 0.2, 1  

class NodeOptionsButton(BottomPanelButton):

    buttonOption: str = StringProperty(None)

    def release_others_in_group(self) -> None:
        if self.bottomBar.currentNodeOptionButton != None:
            self.bottomBar.currentNodeOptionButton.reset_button()
            self.bottomBar.currentNodeOptionButton = None

    def select_me_in_group(self) -> None:
        self.bottomBar.currentNodeOptionButton = self

    def release_me_in_group(self) -> None:
        self.bottomBar.currentNodeOptionButton = None

    def on_press(self) -> None:
        self.bottomBar.manage_nodeOptions_buttons()
