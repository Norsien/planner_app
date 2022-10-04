from kivy.uix.togglebutton import ToggleButton
from kivy.properties import BooleanProperty
from kivy.core.window import Window

class HoverableToggleButton(ToggleButton):
    mouseOverButton = BooleanProperty(False)

    def on_mouseover(self, window, pos):
        if self.collide_point(*pos):
            Window.set_system_cursor('hand')
            self.mouseOverButton = True
            if self.state == "normal":
                self.mouseover_highlight()
        elif self.mouseOverButton:
            Window.set_system_cursor('arrow')
            self.mouseOverButton = False
            if self.state == "normal":
                self.reset_highligt()

    def on_state(self, *args):
        if self.state == "down":
            self.pressed_highlight()
        else: 
            if self.mouseOverButton:
                self.mouseover_highlight()
            else:
                self.reset_highligt()
        

    def reset_highligt(self):
        pass

    def mouseover_highlight(self):
        pass

    def pressed_highlight(self):
        pass

    def reset_button(self):
        self.state = "normal"