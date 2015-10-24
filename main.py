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


class ScreenCell(Widget):
    color = NumericProperty(0.0)
    color_delta = 0
    speed = 1

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
    cell1 = ObjectProperty(None)
    cell2 = ObjectProperty(None)

    def update(self, dt):
        self.cell1.update(dt)
        self.cell2.update(dt)

    def on_touch_down(self, touch):
        if self.cell1.collide_point(touch.x, touch.y):
            self.cell1.toggle()
        if self.cell2.collide_point(touch.x, touch.y):
            self.cell2.toggle()


class SkatApp(App):

    def build(self):
        game = SkatGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    SkatApp().run()
