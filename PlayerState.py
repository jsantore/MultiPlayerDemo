from dataclasses import dataclass
import json
from typing import Dict
import arcade
import datetime
from dataclasses_json import dataclass_json
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000


# a major breakthrough was to find the dataclasses_json package which automatically converted between json and
# dataclasses. My commented out methods worked fine for individual atomic types, but it fell apart for lists
# and other collection types as instance variables in the data classes. using the @dataclass took care of that.

@dataclass_json
@dataclass
class PlayerState:
    x_loc: int
    y_loc: int
    points: int
    last_update: datetime.datetime
    # def to_json(self):
    #     return json.dumps({"x_loc": self.x_loc,
    #                 "y_loc": self.y_loc,
    #                 "points": self.points})

@dataclass_json
@dataclass
class TargetState:
    xLoc: int
    yloc: int
    # def to_json(self):
    #     return json.dumps({"xLoc": self.xLoc,
    #                        "yLoc": self.yloc})


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


@dataclass_json
@dataclass
class GameState:
    player_states: Dict[str, PlayerState]
    target: TargetState

    # def from_json(self, data):
    #     json_data = json.loads(data)
    #     for loc, player in enumerate(json_data['player_states']):
    #         self.player_states[loc] = PlayerState(**player)