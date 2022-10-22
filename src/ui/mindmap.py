from ui.node import *
from ui.bottombar import BottomBar, BottomPanelButton
from ui.sidebar import SideBar
from ui.drawregion import DrawRegion

from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty

from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang import Builder

Builder.load_file('ui/kv/mindmap.kv')

Window.minimum_height = 400     
Window.minimum_width = 500
Window.size = (1280, 800)

class MainScreen(RelativeLayout):
    # References to window widgets
    toolBar = ObjectProperty(None)
    leftSideBar = ObjectProperty(None)
    rightSideBar = ObjectProperty(None)
    bottomBar = ObjectProperty(None)
    drawRegion = ObjectProperty(None)

class MindMapApp(App):
    def build(self):
        mainScreen = MainScreen()
        Clock.schedule_interval(mainScreen.bottomBar.display_position, 1.0/60.0)
        return mainScreen