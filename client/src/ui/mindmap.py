from ui.topbar import TopBar
from ui.bottombar import BottomBar #, BottomPanelButton
from ui.sidebar import SideBar
from ui.drawregion import DrawRegion

from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty

from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang import Builder

Builder.load_file('ui/kv/mindmap.kv')

Window.minimum_height = 480     
Window.minimum_width = 600
Window.size = (1280, 800)

class MainScreen(RelativeLayout):
    topBar: TopBar = ObjectProperty(None)
    leftSideBar: SideBar = ObjectProperty(None)
    rightSideBar: SideBar = ObjectProperty(None)
    bottomBar: BottomBar = ObjectProperty(None)
    drawRegion: DrawRegion = ObjectProperty(None)

class MindMapApp(App):
    def build(self) -> MainScreen:
        mainScreen: MainScreen = MainScreen()
        Clock.schedule_interval(mainScreen.bottomBar.display_position, 1.0/60.0)
        return mainScreen