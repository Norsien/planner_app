from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.node import Node

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import BooleanProperty, ObjectProperty

from kivy.lang import Builder

Builder.load_file('ui/kv/nodetooltip.kv')

class NodeTooltip(BoxLayout):
    is_visible: bool = BooleanProperty(False)
    node: Node = ObjectProperty(None)

    def __init__(self, node: Node, **kwargs) -> None:
        self.node = node
        super().__init__(**kwargs)