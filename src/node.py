from hoverabletogglebutton import HoverableToggleButton

from kivy.properties import NumericProperty, StringProperty, ListProperty, ObjectProperty

from kivy.lang import Builder
from kivy.core.window import Window

Builder.load_file('node.kv')

class VisualNode(HoverableToggleButton):

    nodeData = ObjectProperty()
    drawingPlane = ObjectProperty()

    def __init__(self, **kwargs):
        super(VisualNode, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouseover)

    def on_mouseover(self, window, pos):
        pos = self.drawingPlane.to_local(pos[0], pos[1])
        super(VisualNode, self).on_mouseover(window, pos)

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

class Node:
    def __init__(self, pos):
        self.name = StringProperty(defaultvalue = '?')
        self.name = "New node"
        self.nodeId = NumericProperty()
        self.nodeId = 1
        self.shortDescription = StringProperty()
        self.shortDescription = "This is a new node."
        self.detailedDescription = StringProperty()

        self.pos = ListProperty()
        self.visualNode = ObjectProperty()

        newVisualNode = VisualNode()
        self.visualNode = newVisualNode
        self.pos = (pos[0] - newVisualNode.size[0]/2, pos[1] - newVisualNode.size[1]/2)
        newVisualNode.nodeData = self

        # position has to be bound
        newVisualNode.pos = self.pos



