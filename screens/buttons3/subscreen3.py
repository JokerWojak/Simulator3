from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class SubScreen3(Screen):
    def __init__(self, **kwargs):
        super(SubScreen3, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text="SubScreen 3", font_size='24sp'))
        self.add_widget(layout)
