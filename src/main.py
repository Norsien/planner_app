from node import *
from hoverabletogglebutton import HoverableToggleButton
from bottombar import BottomBar, BottomPanelButton
from sidebar import SideBar

from multiprocessing.sharedctypes import Value
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.stencilview import StencilView
from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty, ListProperty, OptionProperty
from kivy.graphics.transformation import Matrix

from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang import Builder

from math import floor

Builder.load_file('bottombar.kv')
Builder.load_file('sidebar.kv')

Window.minimum_height = 400     
Window.minimum_width = 500
Window.size = (1280, 800)

class MainScreen(RelativeLayout):
    # References to other widgets
    drawingPlane = ObjectProperty(None)
    bottomBar = ObjectProperty(None)
    rightSideBar = ObjectProperty(None)

class ToolBar(Widget):
    pass

class DrawRegion(StencilView):
    def __init__(self, **kwargs):
        self.bind(size=self.drawRegion_size_changed)
        super().__init__(**kwargs)

    def drawRegion_size_changed(self, instance, value):
        if self.size[0] > 100 and self.size[1] > 100:
            self.drawingPlane.recenter_plane()

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

class PlannerApp(App):
    def build(self):
        mainScreen = MainScreen()
        Clock.schedule_interval(mainScreen.bottomBar.display_position, 1.0/60.0)
        return mainScreen

class WidgetBorder(Widget):
    border_width = NumericProperty(1)
    cross_width = NumericProperty(1)
    border_color = ListProperty()

if __name__ == '__main__':
    PlannerApp().run()