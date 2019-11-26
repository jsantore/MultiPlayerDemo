from dataclasses import dataclass
import json
from typing import List
import arcade

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000


@dataclass
class PlayerState:
    x_loc: int
    y_loc: int
    def to_json(self):
        json.dumps({"x_loc": self.x_loc,
                    "y_loc": self.y_loc})




@dataclass
class PlayerMovement:
    keys = {
    arcade.key.UP: False,
    arcade.key.DOWN: False,
    arcade.key.LEFT: False,
    arcade.key.RIGHT: False}

@dataclass
class GameState:
    player_states: List[PlayerState]

    def from_json(self, data):
        json_data = json.loads(data)
        for loc, player in enumerate(json_data['player_states']):
            self.player_states[loc] = PlayerState(**player)