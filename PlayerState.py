from dataclasses import dataclass

@dataclass
class PlayerUpdate:
    xChange: int
    ychange: int

@dataclass
class PlayerMovement:
    up_key: bool
    down_key: bool
    left_key: bool
    right_key: bool