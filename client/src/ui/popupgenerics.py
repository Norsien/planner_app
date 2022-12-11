from kivy.properties import StringProperty
from kivy.uix.popup import Popup

from kivy.lang import Builder

from ui.hoverablebutton import HoverableButton

Builder.load_file('ui/kv/popupgenerics.kv')

class PopupButton(HoverableButton):
    def mouseover_highlight(self) -> None:
        self.button_color = self.highlight_color

    def reset_highlight(self) -> None:
        self.button_color = self.default_color

class ErrorPopup(Popup):
    message: str = StringProperty("")

    def __init__(self, message, **kwargs) -> None:
        super().__init__(**kwargs)
        self.message = message
        self.open()