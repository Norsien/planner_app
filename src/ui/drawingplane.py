from ui.node import *
from ui.bottombar import BottomBar, BottomPanelButton
from ui.sidebar import SideBar
from ui.visualwidgetborder import VisualWidgetBorder

from kivy.uix.scatterlayout import ScatterLayout
from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty, ListProperty, OptionProperty
from kivy.graphics.transformation import Matrix

from math import floor

from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang import Builder

from kivy.lang import Builder

Builder.load_file('ui/kv/drawingplane.kv')

class DrawingPlane(ScatterLayout):
    # References to other widgets
    mainScreen = ObjectProperty(None)
    drawingPlane = ObjectProperty(None)
    backgroundImage = ObjectProperty(None)

    initialRecenterDone = BooleanProperty(False)
    previousParentWidth = NumericProperty()
    previousParentHeight = NumericProperty()
    zoomOptions = ListProperty((0.5, 0.7, 0.85, 1, 1.2, 1.4, 1.7, 2.0))
    currentZoomLevel = NumericProperty(3)

    currentNodeMode = OptionProperty("None", options=["None", "Add", "Connect", "Delete"])
    borderVisible = BooleanProperty(False)
    currentCursorPosition = ListProperty(None)

    nodesList = ListProperty(None)
    currentSelectedNode = ObjectProperty(None, allownone = True)

    def __init__(self, **kwargs):
        super(DrawingPlane, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.get_coordinates)
        self.bind(currentSelectedNode=self.when_node_selected_behaviour)

    # should be limited to once every 1/30 sec
    def recenter_plane(self):
        if not self.initialRecenterDone:
            pos_x = (self.width/2 - self.parent.pos[0] - self.parent.width/2)
            pos_y = (self.height/2 - self.parent.pos[1] - self.parent.height/2)
            self.pos = (-pos_x, -pos_y)
            self.initialRecenterDone = True
            self.previousParentWidth = self.parent.width
            self.previousParentHeight = self.parent.height
        else:
            self.apply_transform(Matrix().translate((self.parent.width - self.previousParentWidth)/2, \
                                                    (self.parent.height - self.previousParentHeight)/2, 0))
            self.previousParentWidth = self.parent.width
            self.previousParentHeight = self.parent.height

    def when_node_selected_behaviour(self, instance, value):
        if self.currentSelectedNode == None:
            self.mainScreen.rightSideBar.close_sideBar()
        else:
            self.mainScreen.rightSideBar.set_node_to_edit(self.currentSelectedNode.nodeData)
            self.mainScreen.rightSideBar.open_sideBar()      
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.currentNodeMode == "Add":
                if touch.button == "left":
                    self.create_new_node(self.to_local(touch.x, touch.y))
                    self.reset_mode()
                    self.mainScreen.bottomBar.createNodeButton.reset_button()
            if touch.is_mouse_scrolling:
                if touch.button == 'scrollup':
                    self.change_scale(touch, -1)
                elif touch.button == 'scrolldown':
                    self.change_scale(touch, 1)
            else:
                ScatterLayout.on_touch_down(self, touch)

    def change_scale(self, touch, val):
        newZoomLevel = self.currentZoomLevel + val
        if newZoomLevel < 0:
            newZoomLevel = 0
        elif newZoomLevel >= len(self.zoomOptions):
            newZoomLevel = len(self.zoomOptions) - 1
        scale = self.zoomOptions[newZoomLevel]/self.zoomOptions[self.currentZoomLevel]
        self.apply_transform(Matrix().scale(scale, scale, scale), anchor=touch.pos)
        self.currentZoomLevel = newZoomLevel

    def create_new_node(self, pos):
        newNode = Node(pos)
        self.draw_a_node(newNode)

    def draw_a_node(self, node):
        if node.visualNode.pos != None:
            node.visualNode.set_drawingPlane(self)
            self.add_widget(node.visualNode)

    def enable_mode(self, mode):
        self.currentNodeMode = mode

    def reset_mode(self):
        self.currentNodeMode = "None"

    def toggle_border_visibility(self):
        self.borderVisible = not self.borderVisible

    def get_coordinates(self, window, pos):
        if self.collide_point(*pos):
            pos_x = (self.to_local(pos[0], pos[1])[0])
            pos_y = (self.to_local(pos[0], pos[1])[1])
            pos = floor(pos_x), floor(pos_y)
            self.currentCursorPosition = pos
            self.mainScreen.bottomBar.set_positionDisplay_value(pos)