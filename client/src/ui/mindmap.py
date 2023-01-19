from ui.topbar import TopBar
from ui.bottombar import BottomBar #, BottomPanelButton
from ui.sidebar import NodeListSideBar, PlaneListSideBar, RightSideBar
from ui.drawregion import DrawRegion
from ui.drawingplane import DrawingPlane
from ui.planepackage import PlanePackage
from ui.saveloadpopup import SaveReminderPopup, SavePlanePackagePopup

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
    nodeListSideBar: NodeListSideBar = ObjectProperty(None)
    planeListSideBar: PlaneListSideBar = ObjectProperty(None)
    rightSideBar: RightSideBar = ObjectProperty(None)
    bottomBar: BottomBar = ObjectProperty(None)
    drawRegion: DrawRegion = ObjectProperty(None)

    planePackage: PlanePackage = ObjectProperty(None)

    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        Window.bind(on_request_close = self.ask_before_closing)

    def set_planePackage(self, planePackage: planePackage) -> None:
        if self.planePackage:
            self.planePackage.unbind(planeList = self.when_plane_list_changed)
        self.planePackage = planePackage
        self.change_planeList(planePackage.planeList)
        planePackage.bind(planeList = self.when_plane_list_changed)
        self.drawRegion.display_topPlane()

    def get_default_package(self) -> PlanePackage:
        if False:
            return PlanePackage()
        return PlanePackage()

    def set_planePackage_default(self) -> None:
        self.set_planePackage(self.get_default_package())

    def when_plane_list_changed(self, planePackage: PlanePackage, planeList: list[DrawingPlane]) -> None:
        self.change_planeList(planeList)

    def change_planeList(self, planeList: list[DrawingPlane]) -> None:
        self.planeListSideBar.update_planes(planeList)

    def ask_before_closing(self, source) -> bool:
        saveReminderPopup = SaveReminderPopup(self)
        saveReminderPopup.open()
        saveReminderPopup.bind(on_dismiss = self.handle_saveReminderPopup)
        return True

    def handle_saveReminderPopup(self, saveReminderPopup: SaveReminderPopup):
        answer: str = saveReminderPopup.answer
        if answer == "no":
            Window.unbind(on_request_close = self.ask_before_closing)
            App.get_running_app().stop()
        if answer == "yes":
            savePlanePackagePopup: SavePlanePackagePopup = SavePlanePackagePopup(mainScreen=self)
            savePlanePackagePopup.open()
            savePlanePackagePopup.bind(on_dismiss = self.resolve_leave_afterSaving)

    def resolve_leave_afterSaving(self, savePlanePackagePopup: SavePlanePackagePopup):
        if not savePlanePackagePopup.saveSuccess:
            return
        Window.unbind(on_request_close = self.ask_before_closing)
        App.get_running_app().stop()

        
class MindMapApp(App):
    def build(self) -> MainScreen:
        mainScreen: MainScreen = MainScreen()
        Clock.schedule_interval(mainScreen.bottomBar.display_position, 1.0/60.0)
        return mainScreen