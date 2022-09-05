from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty, NumericProperty, ListProperty

from kivy.graphics.transformation import Matrix
from kivy.graphics import Color, Ellipse


from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang import Builder

from math import floor


Builder.load_file('bottombar.kv')

Window.minimum_height = 400     
Window.minimum_width = 300
Window.size = (1280, 800)

class MainScreen(RelativeLayout):
    # References to other widgets
    drawingPlane = ObjectProperty(None)
    bottomBar = ObjectProperty(None)
    

class ToolBar(Widget):
    pass

class SideBar(Widget):
    pass

class DrawRegion(AnchorLayout):
    pass

class DrawingPlane(ScrollView):
    # References to other widgets
    mainScreen = ObjectProperty(None)
    scatterLayout = ObjectProperty(None)
    backgroundImage = ObjectProperty(None)

    addingNewNodesMode = BooleanProperty(False)
    connectNodesMode = BooleanProperty(False)
    deleteNodesMode = BooleanProperty(False)
    borderVisible = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(DrawingPlane, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.get_coordinates)

    def get_coordinates(self, window, pos):
        if self.collide_point(*pos):
            pos_x = (self.to_local(pos[0], pos[1])[0] - self.ids.backgroundImage.offset_x)/self.ids.scatterLayout.scale
            pos_y = (self.to_local(pos[0], pos[1])[1] - self.ids.backgroundImage.offset_y)/self.ids.scatterLayout.scale
            pos = floor(pos_x), floor(pos_y)
        else:
            pos = None
        self.mainScreen.ids.bottomBar.set_positionDisplay_value(pos)

    def window_to_background_position(self, pos):
        pos_x = (self.to_local(pos[0], pos[1])[0] - self.ids.backgroundImage.offset_x)/self.ids.scatterLayout.scale
        pos_y = (self.to_local(pos[0], pos[1])[1] - self.ids.backgroundImage.offset_y)/self.ids.scatterLayout.scale
        pos = floor(pos_x), floor(pos_y)
        return pos

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            relative_pos = self.window_to_background_position(touch.pos)

            if self.addingNewNodesMode:
                with self.canvas:
                    Color(1, 1, 0)
                    d = 30.
                    Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
                self.reset_mode()
                self.mainScreen.ids.bottomBar.ids.createNodeButton.reset_button()
            if touch.is_mouse_scrolling:
                if touch.button == 'scrollup':
                    mat = Matrix().scale(.9, .9, .9)
                    self.ids.scatterLayout.apply_transform(mat)
                elif touch.button == 'scrolldown':
                    mat = Matrix().scale(1/.9, 1/.9, 1/.9)
                    self.ids.scatterLayout.apply_transform(mat)
            else:
                ScrollView.on_touch_down(self, touch)
            print(touch.pos, relative_pos)
            print(self.scroll_x)

            

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

class BottomBar(BoxLayout):
    # References to other widgets
    mainScreen = ObjectProperty(None)
    createNodeButton = ObjectProperty(None)
    connectNodesButton = ObjectProperty(None)
    deleteNodeButton = ObjectProperty(None)
    positionDisplay = ObjectProperty(None)
    toggleBorderButton = ObjectProperty(None)

    lastPosition = StringProperty("")

    def manage_nodeOptions_buttons(self):
        if self.ids.createNodeButton.state == "down":
            print('+')
            self.mainScreen.ids.drawingPlane.enable_addingNewNodesMode()
        elif self.ids.connectNodesButton.state == "down":
            print('S')
            self.mainScreen.ids.drawingPlane.enable_connectNodesMode()
        elif self.ids.deleteNodeButton.state == "down":
            print("-")
            self.mainScreen.ids.drawingPlane.enable_deleteNodesMode()
        else:
            print("M")
            self.mainScreen.ids.drawingPlane.reset_mode()

    def manage_border_button(self):
        self.mainScreen.ids.drawingPlane.toggle_border_visibility()
        if self.ids.toggleBorderButton.state == "down":
            print('B+')
        else:
            print('B-')

    def set_positionDisplay_value(self, value):
        if value != None:
            self.lastPosition = str(value)

    def display_position(self, dt):
        self.ids.positionDisplay.text = self.lastPosition

class HoverButton(ToggleButton):
    # References to other widgets
    bottomBar = ObjectProperty(None)
    
    mouseOverButton = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(HoverButton, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouseover)

    def on_mouseover(self, window, pos):
        if self.collide_point(*pos):
            Window.set_system_cursor('hand')
            self.mouseOverButton = True
            if self.state == "normal":
                self.mouseover_highlight()
        elif self.mouseOverButton:
            Window.set_system_cursor('arrow')
            self.mouseOverButton = False
            if self.state == "normal":
                self.reset_highligt()

    def on_state(self, *args):
        if self.state == "down":
            self.pressed_highlight()
        else: 
            if self.mouseOverButton:
                self.mouseover_highlight()
            else:
                self.reset_highligt()
        

    def reset_highligt(self):
        self.size = (30, 30)
        self.button_color = 0.3, 0.4, 0.9, 1

    def mouseover_highlight(self):
        self.size = (34, 34)
        self.button_color = 0.36, 0.48, 0.99, 1

    def pressed_highlight(self):
        self.size = (34, 34)
        self.button_color = 0.7, 0.6, 0.2, 1

    def reset_button(self):
        self.state = "normal"
        

class ButtonBox(AnchorLayout):
    pass

class WidgetBorder(Widget):
    border_width = NumericProperty(1)
    cross_width = NumericProperty(1)
    border_color = ListProperty()


if __name__ == '__main__':
    PlannerApp().run()