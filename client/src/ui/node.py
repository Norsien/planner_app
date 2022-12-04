from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.drawingplane import DrawingPlane

from ui.hoverablebutton import HoverableToggleButton
from ui.nodetooltip import NodeTooltip

from kivy.properties import NumericProperty, StringProperty, ListProperty, BooleanProperty, ObjectProperty

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock

Builder.load_file('ui/kv/node.kv')

class Node(HoverableToggleButton):
    drawingPlane: DrawingPlane = ObjectProperty()

    name: str = StringProperty("New node")
    shortDescription: str = StringProperty("This is a new node.")
    detailedDescription: str = StringProperty()
    pos: tuple[int, int]

    tooltip: NodeTooltip = ObjectProperty(None)

    def __init__(self, pos, **kwargs) -> None:
        super(Node, self).__init__(**kwargs)
        self.pos = (round(pos[0] - self.size[0]/2), round(pos[1] - self.size[1]/2))
        self.tooltip = NodeTooltip(self)
        Window.bind(mouse_pos=self.tooltip_check)

    def on_mouseover(self, window, pos) -> None:
        pos: tuple[int, int] = self.drawingPlane.to_local(pos[0], pos[1])

        super(Node, self).on_mouseover(window, pos)

    def tooltip_check(self, window, pos) -> None:
        if not self.get_root_window():
            return
        local_pos: tuple[int, int] = self.drawingPlane.to_local(pos[0], pos[1])
        self.tooltip.pos = pos
        if self.collide_point(*local_pos):
            self.tooltip.pos = pos
            if not self.tooltip.is_visible:
                self.tooltip.is_visible = True
                Window.add_widget(self.tooltip)
        elif self.tooltip.is_visible:
            self.tooltip.is_visible = False
            Window.remove_widget(self.tooltip)

    def close_tooltip(self, *args) -> None:
        Window.remove_widget(self.tooltip)

    def display_tooltip(self, *args) -> None:
        print("done")
        Window.add_widget(self.tooltip)

    def switch_state(self) -> None: 
        if self.state == "down":
            self.state = "normal"
        else:
            self.state = "down"

    def reset_highlight(self) -> None:
        self.button_color = 0.4, 0.7, 0.4, .4

    def mouseover_highlight(self) -> None:
        self.button_color = 0.6, 0.9, 0.6, .5

    def pressed_highlight(self) -> None:
        self.button_color = 0.6, 0.9, 0.6, 1

    def release_others_in_group(self) -> None:
        if self.drawingPlane.currentSelectedNode != None:
            self.drawingPlane.currentSelectedNode.reset_button()
            self.drawingPlane.currentSelectedNode = None

    def select_me_in_group(self) -> None:
        self.drawingPlane.currentSelectedNode = self

    def release_me_in_group(self) -> None:
        self.drawingPlane.currentSelectedNode = None

    def set_drawingPlane(self, drawingPlane: DrawingPlane) -> None:
        self.drawingPlane = drawingPlane

    def delete(self) -> None:
        self.reset_button()
        self.drawingPlane.remove_widget(self)
        self.drawingPlane.nodeList.remove(self)
