from dataclasses import dataclass
import json
from typing import List
import arcade
import datetime

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000


@dataclass
class PlayerState:
    x_loc: int
    y_loc: int
    points: int
    last_update: datetime.datetime
    def to_json(self):
        return json.dumps({"x_loc": self.x_loc,
                    "y_loc": self.y_loc,
                    "points": self.points})

@dataclass
class TargetState:
    xLoc: int
    yloc: int


@dataclass
class PlayerMovement:
    keys = {
    arcade.key.UP: False,
    arcade.key.DOWN: False,
    arcade.key.LEFT: False,
    arcade.key.RIGHT: False}
    # to string is purely for debugging
    def __str__(self):
        return f"UP: {self.keys[arcade.key.UP]}, Down: {self.keys[arcade.key.DOWN]}, Left: {self.keys[arcade.key.LEFT]}, Right: {self.keys[arcade.key.RIGHT]}, "

@dataclass
class GameState:
    player_states: List[PlayerState]
    target: TargetState
    def from_json(self, data):
        json_data = json.loads(data)
        for loc, player in enumerate(json_data['player_states']):
            self.player_states[loc] = PlayerState(**player)