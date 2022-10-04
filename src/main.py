from node import *
from hoverabletogglebutton import HoverableToggleButton
from bottombar import BottomBar, BottomPanelButton, ButtonBox
from sidebar import SideBar

from multiprocessing.sharedctypes import Value
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.stencilview import StencilView
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty, NumericProperty, ListProperty
from kivy.graphics.transformation import Matrix

from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang import Builder

from math import floor

Builder.load_file('bottombar.kv')
Builder.load_file('sidebar.kv')

Window.minimum_height = 400     
Window.minimum_width = 300
Window.size = (1280, 800)

class MainScreen(RelativeLayout):
    # References to other widgets
    drawingPlane = ObjectProperty(None)
    bottomBar = ObjectProperty(None)

class ToolBar(Widget):
    pass

class DrawRegion(StencilView):
    pass

class DrawingPlane(ScatterLayout):
    # References to other widgets
    mainScreen = ObjectProperty(None)
    scatterLayout = ObjectProperty(None)
    backgroundImage = ObjectProperty(None)

    addingNewNodesMode = BooleanProperty(False)
    connectNodesMode = BooleanProperty(False)
    deleteNodesMode = BooleanProperty(False)
    borderVisible = BooleanProperty(False)

    currentCursorPosition = ListProperty(None)
    nodesList = ListProperty(None)

    def __init__(self, **kwargs):
        super(DrawingPlane, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.get_coordinates)

    def get_coordinates(self, window, pos):
        if self.collide_point(*pos):
            pos_x = (self.to_local(pos[0], pos[1])[0])
            pos_y = (self.to_local(pos[0], pos[1])[1])
            pos = floor(pos_x), floor(pos_y)
            self.currentCursorPosition = pos
            self.mainScreen.ids.bottomBar.set_positionDisplay_value(pos)


    zoomOptions = ListProperty((0.5, 0.7, 0.85, 1, 1.2, 1.4, 1.7, 2.0))
    currentZoomLevel = NumericProperty(3)

    def change_scale(self, touch, val):
        newZoomLevel = self.currentZoomLevel + val
        if newZoomLevel < 0:
            newZoomLevel = 0
        elif newZoomLevel >= len(self.zoomOptions):
            newZoomLevel = len(self.zoomOptions) - 1
        scale = self.zoomOptions[newZoomLevel]/self.zoomOptions[self.currentZoomLevel]
        self.apply_transform(Matrix().scale(scale, scale, scale), anchor=touch.pos)
        self.currentZoomLevel = newZoomLevel

    
    # def transform_with_touch(self, touch):
    #     # just do a simple one finger drag
    #     changed = False
    #     if len(self._touches) == self.translation_touches:
    #         # _last_touch_pos has last pos in correct parent space,
    #         # just like incoming touch
    #         dx = (touch.x - self._last_touch_pos[touch][0]) \
    #             * self.do_translation_x
    #         dy = (touch.y - self._last_touch_pos[touch][1]) \
    #             * self.do_translation_y
    #         dx = dx / self.translation_touches
    #         dy = dy / self.translation_touches
    #         if self.pos[0] + dx < 300 or self.pos[0] + dx > 1000:
    #             dx = 0
    #         print(dx)
    #         self.apply_transform(Matrix().translate(dx, dy, 0))
    #         changed = True

    #     if len(self._touches) == 1:
    #         return changed

    #     # # we have more than one touch... list of last known pos
    #     # points = [Vector(self._last_touch_pos[t]) for t in self._touches
    #     #           if t is not touch]
    #     # # add current touch last
    #     # points.append(Vector(touch.pos))

    #     # # we only want to transform if the touch is part of the two touches
    #     # # farthest apart! So first we find anchor, the point to transform
    #     # # around as another touch farthest away from current touch's pos
    #     # anchor = max(points[:-1], key=lambda p: p.distance(touch.pos))

    #     # # now we find the touch farthest away from anchor, if its not the
    #     # # same as touch. Touch is not one of the two touches used to transform
    #     # farthest = max(points, key=anchor.distance)
    #     # if farthest is not points[-1]:
    #     #     return changed
        
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.addingNewNodesMode:
                if touch.button == "left":
                    self.create_new_node(self.to_local(touch.x, touch.y))
                    self.reset_mode()
                    self.mainScreen.ids.bottomBar.ids.createNodeButton.reset_button()
            if touch.is_mouse_scrolling:
                if touch.button == 'scrollup':
                    self.change_scale(touch, -1)
                elif touch.button == 'scrolldown':
                    self.change_scale(touch, 1)
            else:
                ScatterLayout.on_touch_down(self, touch)
            print(self.children[0].children)

    def create_new_node(self, pos):
        newNode = Node(pos)
        self.draw_a_node(newNode)

    def draw_a_node(self, node):
        if node.visualNode.pos != None:
            self.add_widget(node.visualNode)

       
    def enable_addingNewNodesMode(self):
        self.reset_mode()
        self.addingNewNodesMode = True

    def enable_connectNodesMode(self):
        self.reset_mode()
        self.connectNodesMode = True

    def enable_deleteNodesMode(self):
        self.reset_mode()
        self.deleteNodesMode = True

    def reset_mode(self):
        self.addingNewNodesMode = False
        self.connectNodesMode = False
        self.deleteNodesMode = False

    def toggle_border_visibility(self):
        self.borderVisible = not self.borderVisible

class PlannerApp(App):
    def build(self):
        mainScreen = MainScreen()
        Clock.schedule_interval(mainScreen.ids.bottomBar.display_position, 1.0/60.0)
        return mainScreen

class WidgetBorder(Widget):
    border_width = NumericProperty(1)
    cross_width = NumericProperty(1)
    border_color = ListProperty()

if __name__ == '__main__':
    PlannerApp().run()