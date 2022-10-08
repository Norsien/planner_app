from hoverabletogglebutton import HoverableToggleButton

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty

from kivy.core.window import Window

class BottomBar(BoxLayout):
    # References to other widgets
    mainScreen = ObjectProperty(None)
    createNodeButton = ObjectProperty(None)
    connectNodesButton = ObjectProperty(None)
    deleteNodeButton = ObjectProperty(None)
    positionDisplay = ObjectProperty(None)
    toggleBorderButton = ObjectProperty(None)

    lastPosition = StringProperty("")
    currentNodeOptionButton = ObjectProperty(None, allownone = True)

    def manage_nodeOptions_buttons(self):
        if self.currentNodeOptionButton == None:
            self.mainScreen.drawingPlane.reset_mode()
        else:
            self.mainScreen.drawingPlane.enable_mode(self.currentNodeOptionButton.buttonOption)

    def manage_border_button(self):
        self.mainScreen.drawingPlane.toggle_border_visibility()

    def set_positionDisplay_value(self, value):
        if value != None:
            self.lastPosition = str(value)

    def display_position(self, dt):
        self.positionDisplay.text = self.lastPosition

class BottomPanelButton(HoverableToggleButton):
    # References to other widgets
    bottomBar = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(BottomPanelButton, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouseover) 

    def reset_highligt(self):
        self.size = (30, 30)
        self.button_color = 0.3, 0.4, 0.9, 1

    def mouseover_highlight(self):
        self.size = (34, 34)
        self.button_color = 0.36, 0.48, 0.99, 1

    def pressed_highlight(self):
        self.size = (34, 34)
        self.button_color = 0.7, 0.6, 0.2, 1  

class NodeOptionsButton(BottomPanelButton):

    buttonOption = StringProperty(None)

    def release_others_in_group(self):
        if self.bottomBar.currentNodeOptionButton != None:
            self.bottomBar.currentNodeOptionButton.reset_button()
            self.bottomBar.currentNodeOptionButton = None

    def select_me_in_group(self):
        self.bottomBar.currentNodeOptionButton = self

    def release_me_in_group(self):
        self.bottomBar.currentNodeOptionButton = None

    def on_press(self):
        self.bottomBar.manage_nodeOptions_buttons()
