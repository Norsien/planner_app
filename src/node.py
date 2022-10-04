from hoverabletogglebutton import HoverableToggleButton

from kivy.properties import NumericProperty, StringProperty, ListProperty, ObjectProperty

from kivy.lang import Builder

Builder.load_file('node.kv')

class VisualNode(HoverableToggleButton):
    node = ObjectProperty()

    def reset_highligt(self):
        self.button_color = 0.4, 0.7, 0.4, .4

    def mouseover_highlight(self):
        self.button_color = 0.6, 0.9, 0.6, .5

    def pressed_highlight(self):
        self.button_color = 0.6, 0.9, 0.6, .8

class Node:
    def __init__(self, pos):
        self.name = StringProperty()
        self.name = "New node"
        self.id = NumericProperty()

        self.shortDescription = StringProperty()
        self.detailedDescription = StringProperty()

        self.pos = ListProperty()
        self.visualNode = ObjectProperty()


        newVisualNode = VisualNode()
        self.visualNode = newVisualNode
        self.pos = (pos[0] - newVisualNode.size[0]/2, pos[1] - newVisualNode.size[1]/2)
        newVisualNode.node = self

        # position has to be bound
        newVisualNode.pos = self.pos
        print(self.pos, self.visualNode)



