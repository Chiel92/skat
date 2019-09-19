__version__ = '1.0'

# Enable importing modules from graph-problems folder
# import sys
# import os
# current_dir = os.path.dirname(os.path.realpath(__file__))
# sys.path.insert(0, current_dir + '/graph-problems')

from datetime import datetime

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty
from kivy.clock import Clock

from pythonosc import osc_message_builder
from pythonosc import udp_client
osc_client = udp_client.UDPClient('localhost', 5005)


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
            if nr_neighbors in [2, 3]:
                self.next_state = 1
            else:
                self.next_state = 0
        else:
            if nr_neighbors == 3:
                self.next_state = 1
            else:
                self.next_state = 0

    def count_neighbors(self):
        count = 0
        for rowd in [-1, 0, 1]:
            for cold in [-1, 0, 1]:
                if not (cold == rowd == 0):
                    nrow = (self.row + rowd) % self.skatgame.rows
                    ncol = (self.col + cold) % self.skatgame.cols
                    count += self.skatgame.grid[(nrow, ncol)].state
        return count


class SkatGame(Widget):
    cell_size = NumericProperty(0)

    rows = 12
    cols = 16

    stepnumber = NumericProperty(0)
    gameoflife_interval = 16  # Number of steps between each game of life update

    currently_playing_col = NumericProperty(0)

    def __init__(self):
        self.colors = [(.6, .4, .4), (.4, .6, .4), (.4, .4, .6), (.6, .6, .4)]
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
        # Compute next state
        for cell in self.grid.values():
            cell.step()
        # Proceed to next state
        for cell in self.grid.values():
            cell.proceed()

    def sound_step(self, dt):
        current_col_cells = [self.grid[(row, self.currently_playing_col)] for row in
                             range(self.rows)]

        # Send messages to chuck
        rows_on = [cell.row for cell in current_col_cells if cell.state]
        if rows_on:
            row_to_play = max(rows_on)
            row_to_play2 = min(rows_on)
            row_to_play3 = rows_on[1] if len(rows_on) > 1 else rows_on[0]
            freq_map = {
                    0 : 100.0,
                    1 : 200.0,
                    2 : 300.0,
                    3 : 400.0,
                    4 : 500.0,
                    5 : 600.0,
                    6 : 800.0,
                    7 : 900.0,
                    8 : 1000.0,
                    9 : 1200.0,
                    10 : 1500.0,
                    11 : 1600.0,
                }
            # osc_client.send(osc_message_builder.OscMessageBuilder(address="/debug").build())
            msg = osc_message_builder.OscMessageBuilder(address="/frequency")
            msg.add_arg(freq_map[row_to_play])
            msg.add_arg(freq_map[row_to_play2])
            msg = msg.build()
            print(msg.dgram)
            print('Sending at', datetime.now())
            osc_client.send(msg)

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
