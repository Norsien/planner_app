from tokenize import String
from ui.hoverabletogglebutton import HoverableToggleButton

from kivy.properties import NumericProperty, StringProperty, ListProperty, ObjectProperty

from kivy.lang import Builder
from kivy.core.window import Window

Builder.load_file('ui/kv/node.kv')

class Node(HoverableToggleButton):

    nodeData = ObjectProperty()
    drawingPlane = ObjectProperty()

    name = StringProperty("New node")
    nodeId = NumericProperty(1)
    shortDescription = StringProperty("This is a new node.")
    detailedDescription = StringProperty()

    def __init__(self, pos, **kwargs):
        super(Node, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouseover)
        self.pos = (pos[0] - self.size[0]/2, pos[1] - self.size[1]/2)

    def on_mouseover(self, window, pos):
        pos = self.drawingPlane.to_local(pos[0], pos[1])
        super(Node, self).on_mouseover(window, pos)

    def reset_highligt(self):
        self.button_color = 0.4, 0.7, 0.4, .4

    def mouseover_highlight(self):
        self.button_color = 0.6, 0.9, 0.6, .5

    def pressed_highlight(self):
        self.button_color = 0.6, 0.9, 0.6, 1

    def release_others_in_group(self):
        if self.drawingPlane.currentSelectedNode != None:
            self.drawingPlane.currentSelectedNode.reset_button()
            self.drawingPlane.currentSelectedNode = None

    def select_me_in_group(self):
        self.drawingPlane.currentSelectedNode = self

    def release_me_in_group(self):
        self.drawingPlane.currentSelectedNode = None

    def set_drawingPlane(self, drawingPlane):
        self.drawingPlane = drawingPlane

    def delete(self):
        self.reset_button()
        self.drawingPlane.remove_widget(self)
        self.drawingPlane.nodeList.remove(self)
