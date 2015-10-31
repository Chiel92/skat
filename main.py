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
    state = 0
    next_state = 0

    color = NumericProperty(0.0)
    color_transition_speed = 4
    _color_delta = 0

    row = NumericProperty(0)
    col = NumericProperty(0)
    margin = NumericProperty(5)

    skatgame = ObjectProperty(None)

    def proceed(self):
        self.set_state(self.next_state)

    def set_state(self, state):
        self.state = state
        self.refresh_color()

    def refresh_color(self):
        if self.color != self.state:
            d = self.state - self.color
            self._color_delta = d / abs(d) * self.color_transition_speed

    def update_color(self, dt):
        self.color += self._color_delta * dt
        if not 0 < self.color < 1:
            self.color = round(self.color)
            self._color_delta = 0

    def step(self):
        nr_neighbors = self.count_neighbors()
        if self.state == 1:
            if nr_neighbors not in [2, 3]:
                self.next_state = 0
        elif nr_neighbors == 3:
            self.next_state = 1

    def count_neighbors(self):
        count = 0
        for rowd in [-1, 0, 1]:
            for cold in [-2, 0, 2]:
                if not (cold == 0 and rowd == 0):
                    nrow = (self.row + rowd) % self.skatgame.rows
                    ncol = (self.col + cold) % self.skatgame.cols
                    count += self.skatgame.grid[(nrow, ncol)].state
        return count


class SkatGame(Widget):
    cell_size = NumericProperty(0)

    rows = 20
    cols = 16

    stepnumber = NumericProperty(0)
    gameoflife_interval = 16  # Number of steps between each game of life update

    currently_playing_col = NumericProperty(0)
    current_soundboard_index = 0

    def __init__(self):
        Widget.__init__(self)
        self.grid = {}

        for row in range(self.rows):
            for col in range(self.cols):
                cell = Cell(skatgame=self, row=row, col=col)
                self.add_widget(cell)
                self.grid[(row, col)] = cell

        self.soundboards = []
        soundboard = {}
        for col in range(self.cols):
            soundboard[col] = {
                0: SoundLoader.load('sound/c4.wav'),
                1: SoundLoader.load('sound/d4.wav'),
                2: SoundLoader.load('sound/e4.wav'),
                3: SoundLoader.load('sound/g4.wav'),
                4: SoundLoader.load('sound/a4.wav'),
                5: SoundLoader.load('sound/c5.wav'),
                6: SoundLoader.load('sound/d5.wav'),
                7: SoundLoader.load('sound/e5.wav'),
                8: SoundLoader.load('sound/g5.wav'),
                9: SoundLoader.load('sound/a5.wav'),
                10: SoundLoader.load('sound/c6.wav'),
                11: SoundLoader.load('sound/d6.wav'),
                12: SoundLoader.load('sound/e6.wav'),
                13: SoundLoader.load('sound/g6.wav'),
                14: SoundLoader.load('sound/a6.wav'),
                15: SoundLoader.load('sound/c7.wav'),
                16: SoundLoader.load('sound/d7.wav'),
                17: SoundLoader.load('sound/e7.wav'),
                18: SoundLoader.load('sound/g7.wav'),
                19: SoundLoader.load('sound/a7.wav'),
            }
        self.soundboards.append(soundboard)

    def update_color(self, dt):
        for cell in self.grid.values():
            cell.update_color(dt)

    def gameoflife_step(self):
        # Compute next state
        for cell in self.grid.values():
            cell.step()
        # Proceed to next state
        for cell in self.grid.values():
            cell.proceed()

        # Load next soundboard
        self.current_soundboard_index = ((self.current_soundboard_index + 1) %
                                         len(self.soundboards))

    def sound_step(self, dt):
        soundboard = self.soundboards[self.current_soundboard_index]
        current_col_cells = [self.grid[(row, self.currently_playing_col)] for row in
                             range(self.rows)]
        to_play = [soundboard[cell.col][cell.row] for cell in current_col_cells if cell.state]

        # Seperate loop for playing, to minimize latency between tones
        for s in to_play:
            s.play()

        self.currently_playing_col = (self.currently_playing_col + 1) % self.cols
        self.stepnumber += 1

        # Advance game of life if a new interval starts
        if self.gameoflife_interval == self.stepnumber:
            self.gameoflife_step()
            self.stepnumber = 0

    def on_touch_move(self, touch):
        for cell in self.grid.values():
            if cell.collide_point(touch.x, touch.y):
                cell.set_state(1)


class SkatApp(App):

    def build(self):
        game = SkatGame()
        Clock.schedule_interval(game.update_color, 1.0 / 60.0)
        Clock.schedule_interval(game.sound_step, .15)
        return game


if __name__ == '__main__':
    SkatApp().run()
