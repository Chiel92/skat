__version__ = '1.0'

# Enable importing modules from graph-problems folder
import sys
import os
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, current_dir + '/graph-problems')


import pixelgraph


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty
from kivy.clock import Clock


class Cell(Widget):
    color = NumericProperty(0.0)
    color_delta = 0
    speed = 1

    row = NumericProperty(0)
    col = NumericProperty(0)

    skatgame = ObjectProperty(None)

    def toggle(self):
        if self.color == 0:
            self.color_delta = self.speed
        elif self.color == 1:
            self.color_delta = -self.speed
        else:
            self.color_delta *= -1

    def update(self, dt):
        self.color += self.color_delta * dt
        if not 0 < self.color < 1:
            self.color = round(self.color)
            self.color_delta = 0


class SkatGame(Widget):
    rows = 20
    cols = 20

    def __init__(self):
        Widget.__init__(self)

        for row in range(self.rows):
            for col in range(self.cols):
                cell = Cell(skatgame=self, row=row, col=col)
                self.add_widget(cell)


    def update(self, dt):
        for child in self.children:
            child.update(dt)

    def on_touch_down(self, touch):
        for child in self.children:
            if child.collide_point(touch.x, touch.y):
                child.toggle()


class SkatApp(App):

    def build(self):
        game = SkatGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    SkatApp().run()
