import imp
from kivy.uix.stencilview import StencilView

from ui.drawingplane import DrawingPlane

from kivy.lang import Builder

Builder.load_file('ui/kv/drawregion.kv')

class DrawRegion(StencilView):
    def __init__(self, **kwargs):
        self.bind(size=self.drawRegion_size_changed)
        super().__init__(**kwargs)

    def drawRegion_size_changed(self, instance, value):
        if self.size[0] > 100 and self.size[1] > 100:
            self.drawingPlane.recenter_plane()