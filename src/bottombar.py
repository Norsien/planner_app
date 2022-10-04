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

    def manage_nodeOptions_buttons(self):
        if self.ids.createNodeButton.state == "down":
            print('+')
            self.mainScreen.ids.drawingPlane.enable_addingNewNodesMode()
        elif self.ids.connectNodesButton.state == "down":
            print('S')
            self.mainScreen.ids.drawingPlane.enable_connectNodesMode()
        elif self.ids.deleteNodeButton.state == "down":
            print("-")
            self.mainScreen.ids.drawingPlane.enable_deleteNodesMode()
        else:
            print("M")
            self.mainScreen.ids.drawingPlane.reset_mode()

    def manage_border_button(self):
        self.mainScreen.ids.drawingPlane.toggle_border_visibility()
        if self.ids.toggleBorderButton.state == "down":
            print('B+')
        else:
            print('B-')

    def set_positionDisplay_value(self, value):
        if value != None:
            self.lastPosition = str(value)

    def display_position(self, dt):
        self.ids.positionDisplay.text = self.lastPosition

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

class ButtonBox(AnchorLayout):
    pass