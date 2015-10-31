__version__ = '1.0'

# Enable importing modules from graph-problems folder
import sys
import os
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, current_dir + '/graph-problems')




from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty
from kivy.clock import Clock
from kivy.core.audio import SoundLoader


class Cell(Widget):
    status = 0
    nextstatus = 0

    color = NumericProperty(0.0)
    color_delta = 0
    speed = 5

    row = NumericProperty(0)
    col = NumericProperty(0)
    margin = NumericProperty(5)

    skatgame = ObjectProperty(None)

    def toggle(self):
        self.status = 1 - self.status
        self.refresh_colordelta()

    def refresh_colordelta(self):
        if self.color != self.status:
            d = self.status - self.color
            self.color_delta = d / abs(d) * self.speed

    def update(self, dt):
        self.color += self.color_delta * dt
        if not 0 < self.color < 1:
            self.color = round(self.color)
            self.color_delta = 0

    def step(self):
        nr_neighbors = self.count_neighbors()
        if self.status == 1:
            if nr_neighbors not in [2, 3]:
                self.status = 0
        elif nr_neighbors == 3:
            self.status = 1
        self.refresh_colordelta()

    def count_neighbors(self):
        count = 0
        for rowd in [-1, 0, 1]:
            for cold in [-1, 0, 1]:
                if not (cold == 0 and rowd == 0):
                    nrow = self.row + rowd
                    ncol = self.col + cold
                    if 0 <= nrow < self.skatgame.rows and 0 <= ncol < self.skatgame.cols:
                        count += self.skatgame.grid[nrow][ncol].status
        return count


class SkatGame(Widget):
    cell_size = NumericProperty(0)

    rows = 20
    cols = 20

    sound_row = NumericProperty(0)

    def __init__(self):
        Widget.__init__(self)
        self.grid = [[None] * self.cols for _ in range(self.rows)]

        for row in range(self.rows):
            for col in range(self.cols):
                cell = Cell(skatgame=self, row=row, col=col)
                self.add_widget(cell)
                self.grid[row][col] = cell


    def update(self, dt):
        for child in self.children:
            child.update(dt)

    def gameoflife_step(self, dt):
        for child in self.children:
            child.step()
        # for child in self.children:
            # child.status = child.nextstatus
            # child.refresh_colordelta()

    def sound_step(self, dt):
        for cell in self.grid[self.sound_row]:
            if cell.status == 1:
                self.sounds[cell.col].play()
        self.sound_row = (self.sound_row + 1) % self.rows

    def on_touch_move(self, touch):
        for child in self.children:
            if child.collide_point(touch.x, touch.y):
                child.toggle()


class SkatApp(App):

    def build(self):
        game = SkatGame()
        game.sounds = {
            0 : SoundLoader.load('sound/c4.wav'),
            1 : SoundLoader.load('sound/d4.wav'),
            2 : SoundLoader.load('sound/e4.wav'),
            3 : SoundLoader.load('sound/g4.wav'),
            4 : SoundLoader.load('sound/a4.wav'),
            5 : SoundLoader.load('sound/c5.wav'),
            6 : SoundLoader.load('sound/d5.wav'),
            7 : SoundLoader.load('sound/e5.wav'),
            8 : SoundLoader.load('sound/g5.wav'),
            9 : SoundLoader.load('sound/a5.wav'),
            10 : SoundLoader.load('sound/c6.wav'),
            11 : SoundLoader.load('sound/d6.wav'),
            12 : SoundLoader.load('sound/e6.wav'),
            13 : SoundLoader.load('sound/g6.wav'),
            14 : SoundLoader.load('sound/a6.wav'),
            15 : SoundLoader.load('sound/c7.wav'),
            16 : SoundLoader.load('sound/d7.wav'),
            17 : SoundLoader.load('sound/e7.wav'),
            18 : SoundLoader.load('sound/g7.wav'),
            19 : SoundLoader.load('sound/a7.wav'),
        }
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        dt = .25
        Clock.schedule_interval(game.sound_step, dt)
        Clock.schedule_interval(game.gameoflife_step, dt)
        return game


if __name__ == '__main__':
    SkatApp().run()
