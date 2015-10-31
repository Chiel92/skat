__version__ = '1.0'

# Enable importing modules from graph-problems folder
# import sys
# import os
# current_dir = os.path.dirname(os.path.realpath(__file__))
# sys.path.insert(0, current_dir + '/graph-problems')




from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty
from kivy.clock import Clock
from kivy.core.audio import SoundLoader


class Cell(Widget):
    status = 0
    next_status = 0

    color = NumericProperty(0.0)
    color_transition_speed = 4
    _color_delta = 0

    row = NumericProperty(0)
    col = NumericProperty(0)
    margin = NumericProperty(5)

    skatgame = ObjectProperty(None)

    def proceed(self):
        self.set_status(self.next_status)

    def set_status(self, status):
        self.status = status
        self.refresh_color()

    def refresh_color(self):
        if self.color != self.status:
            d = self.status - self.color
            self._color_delta = d / abs(d) * self.color_transition_speed

    def update_color(self, dt):
        self.color += self._color_delta * dt
        if not 0 < self.color < 1:
            self.color = round(self.color)
            self._color_delta = 0

    def step(self):
        nr_neighbors = self.count_neighbors()
        if self.status == 1:
            if nr_neighbors not in [2, 3]:
                self.next_status = 0
        elif nr_neighbors == 3:
            self.next_status = 1

    def count_neighbors(self):
        count = 0
        for rowd in [-1, 0, 1]:
            for cold in [-1, 0, 1]:
                if not (cold == 0 and rowd == 0):
                    nrow = self.row + rowd
                    ncol = self.col + cold
                    if 0 <= nrow < self.skatgame.rows and 0 <= ncol < self.skatgame.cols:
                        count += self.skatgame.grid[(nrow, ncol)].status
        return count


class SkatGame(Widget):
    cell_size = NumericProperty(0)

    rows = 16
    cols = 20

    stepnumber = NumericProperty(0)
    gameoflife_interval = 4

    sound_col = NumericProperty(0)

    def __init__(self):
        Widget.__init__(self)
        self.grid = {}

        for row in range(self.rows):
            for col in range(self.cols):
                cell = Cell(skatgame=self, row=row, col=col)
                self.add_widget(cell)
                self.grid[(row, col)] = cell

    def update_color(self, dt):
        for cell in self.grid.values():
            cell.update_color(dt)

    def gameoflife_step(self):
        for cell in self.grid.values():
            cell.step()
        for cell in self.grid.values():
            cell.proceed()

    def sound_step(self, dt):
        print('Start step')
        for row in range(self.rows):
            cell = self.grid[(row, self.sound_col)]
            if cell.status == 1:
                self.sounds[cell.col].play()
                print('Playing {},{}'.format(cell.row, cell.col))
        self.sound_col = (self.sound_col + 1) % self.rows
        self.stepnumber += 1

        if self.gameoflife_interval == self.stepnumber:
            self.gameoflife_step()
            self.stepnumber = 0

    def on_touch_move(self, touch):
        for child in self.children:
            if child.collide_point(touch.x, touch.y):
                child.set_status(1)


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
        Clock.schedule_interval(game.update_color, 1.0 / 60.0)
        Clock.schedule_interval(game.sound_step, .5)
        return game


if __name__ == '__main__':
    SkatApp().run()
