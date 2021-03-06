from enum import Enum

from lib.math.angle_deg import AngleDeg
from lib.parser.cmd_line_parser import CmdLineParser
from lib.player.object_ball import BallObject
from lib.player.object_player import PlayerObject
from lib.rcsc.game_mode import GameMode
from lib.rcsc.game_time import GameTime
from lib.rcsc.types import SideID, GameModeType, Card
from typing import List

class InterceptTable:
    def self_reach_cycle(self) -> int: ...

    def self_exhaust_reach_cycle(self) -> int: ...

    def teammate_reach_cycle(self) -> int: ...

    def second_teammate_reach_cycle(self) -> int: ...

    def goalie_reach_cycle(self) -> int: ...

    def opponent_reach_cycle(self) -> int: ...

    def second_opponent_reach_cycle(self) -> int: ...

    def self_cache(self) -> list: ...

    def update(self, wm): ...


class WorldModel:
    def ball(self) -> BallObject: ...

    def self(self) -> PlayerObject: ...

    def our_side(self) -> SideID: ...

    def our_player(self, unum) -> PlayerObject: ...

    def their_player(self, unum) -> PlayerObject: ...

    def time(self) -> GameTime: ...

    def team_name(self) -> str: ...

    def game_mode(self) -> GameMode: ...

    def our_goalie_unum(self) -> int: ...

    def _set_our_goalie_unum(self): ...

    def teammates_from_ball(self) -> List[PlayerObject]: ...

    def opponents_from_ball(self) -> List[PlayerObject]: ...

    def _set_teammates_from_ball(self): ...

    def last_kicker_side(self) -> SideID: ...

    def exist_kickable_opponents(self): ...

    def exist_kickable_teammates(self): ...

    def intercept_table(self) -> InterceptTable: ...

    def offside_line_x(self) -> float: ...

    def their_goalie_unum(self): ...

    def get_opponent_goalie(self) -> PlayerObject: ...

    def get_opponent_nearest_to_self(self, count_thr: int, with_goalie: bool = True) -> PlayerObject: ...

    def self_unum(self): ...


class ClientMode(Enum):
    offline = 0
    Online = 1


class BasicClient:
    def __init__(self): ...

    def connect_to(self,
                   host_port: tuple,
                   interval_ms=None): ...

    def run(self, agent): ...

    def run_online(self, agent): ...

    def set_server_alive(self, mode: bool): ...

    def send_message(self, msg): ...

    def recv_message(self): ...

    def message(self): ...

    def client_mode(self): ...

    def is_server_alive(self): ...


class SoccerAgent:
    def __init__(self): ...

    def init(self,
             client: BasicClient,
             argv: list) -> bool: ...

    def init_impl(self,
                  cmd_parser: CmdLineParser) -> bool: ...

    def handle_start(self) -> bool: ...

    def handle_message(self): ...

    def handle_exit(self): ...


class DebugClient:
    def add_message(self, msg): ...

    def set_target(self, p): ...

    def add_line(self, start, end): ...

    def add_triangle(self, v1=None, v2=None, v3=None, tri=None): ...

    def add_rectangle(self, rect): ...

    def add_circle(self, center=None, radius=None, circle=None): ...


class PlayerAgent(SoccerAgent):
    def do_dash(self, power, angle=0) -> bool: ...

    def do_turn(self, angle) -> bool: ...

    def do_move(self, x, y) -> bool: ...

    def do_kick(self, power: float, rel_dir: AngleDeg) -> bool: ...

    def do_tackle(self, power_or_dir: float, foul: bool) -> bool: ...

    def do_turn_neck(self, moment: AngleDeg) -> bool: ...

    def world(self) -> WorldModel: ...

    def full_world(self) -> WorldModel: ...

    def init_dlog(self, message: str): ...

    def debug_client(self) -> DebugClient: ...
