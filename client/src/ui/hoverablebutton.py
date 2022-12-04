from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import BooleanProperty
from kivy.core.window import Window

class HoverableButton(Button):
    mouseOverButton: bool = BooleanProperty(False)
    size: tuple[int, int]
    button_color: tuple[float, float, float, float]

    def __init__(self, **kwargs) -> None:
        super(HoverableButton, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouseover)

    def on_mouseover(self, window, pos) -> None:
        if self.collide_point(*pos):
            Window.set_system_cursor('hand')
            self.mouseOverButton = True
            self.mouseover_highlight()
        elif self.mouseOverButton:
            Window.set_system_cursor('arrow')
            self.mouseOverButton = False
            self.reset_highlight()
        
    def reset_highlight(self) -> None:
        pass

    def mouseover_highlight(self) -> None:
        pass


class HoverableToggleButton(ToggleButton):
    mouseOverButton: bool = BooleanProperty(False)
    size: tuple[int, int]
    button_color: tuple[float, float, float, float]

    def __init__(self, **kwargs) -> None:
        super(HoverableToggleButton, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouseover)

    def on_mouseover(self, window, pos) -> None:
        if self.collide_point(*pos):
            Window.set_system_cursor('hand')
            self.mouseOverButton = True
            if self.state == "normal":
                self.mouseover_highlight()
        elif self.mouseOverButton:
            Window.set_system_cursor('arrow')
            self.mouseOverButton = False
            if self.state == "normal":
                self.reset_highlight()

    def on_state(self, *args) -> None:
        if self.state == "down":
            self.release_others_in_group()
            self.select_me_in_group()
            self.pressed_highlight()
        else:
            self.release_me_in_group()
            if self.mouseOverButton:
                self.mouseover_highlight()
            else:
                self.reset_highlight()

    def reset_highlight(self) -> None:
        pass

    def mouseover_highlight(self) -> None:
        pass

    def pressed_highlight(self) -> None:
        pass

    def release_others_in_group(self) -> None:
        pass

    def select_me_in_group(self) -> None:
        pass

    def release_me_in_group(self) -> None:
        pass

    def reset_button(self) -> None:
        self.state: str = "normal"