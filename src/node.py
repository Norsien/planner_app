from kivy.properties import NumericProperty, StringProperty

class Node:
    def __init__(self):
        self.name = StringProperty("New Node")
        self.id = NumericProperty()

        self.shortDescription = StringProperty("")
        self.detailedDescription = StringProperty("")

