from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty

from kivy.lang import Builder

Builder.load_file('ui/kv/visualwidgetborder.kv')

class VisualWidgetBorder(Widget):
    border_width = NumericProperty(1)
    cross_width = NumericProperty(1)
    border_color = ListProperty()