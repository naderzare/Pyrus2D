import logging
import time

from base.decision import *
from lib.debug.logger import setup_logger
from lib.player.world_model import WorldModel
from lib.network.udp_socket import UDPSocket, IPAddress
from lib.player_command.player_command import PlayerInitCommand
from lib.player_command.player_command_body import PlayerTurnCommand, PlayerDashCommand, PlayerMoveCommand
from lib.player_command.player_command_support import PlayerDoneCommand
from lib.player_command.player_command_sender import PlayerSendCommands, PlayerCommandReverser
from lib.rcsc.server_param import ServerParam
from lib.rcsc.types import SideID


class PlayerAgent:
    def __init__(self):
        self._socket = UDPSocket(IPAddress('localhost', 6000))
        self._world = WorldModel()
        self._full_world = WorldModel()
        self._think_mode = True
        self._is_synch_mode = True
        self._server_param = ServerParam()
        self._last_body_command = []
        self._logger = logging.Logger("2") # make debug folder in Pyrus directory

    def run(self, team_name, goalie):
        self.connect(team_name, goalie)
        while True:
            message_and_address = []
            message_count = 0
            while self._socket.recieve_msg(message_and_address) > 0:
                message = message_and_address[0]
                server_address = message_and_address[1]
                self.parse_message(message.decode())
                message_count += 1

            if message_count > 0:
                self.action()
            elif self._think_mode:
                cycle_start = time.time()

                self.action()
                self._think_mode = False

                cycle_end = time.time()
                print(f"run-time: {cycle_end-cycle_start}s")

    def connect(self, team_name, goalie, version=15):
        self._socket.send_msg(PlayerInitCommand(team_name, 15, goalie).str())

    def parse_message(self, message):
        self._think_mode = False
        if message.find("(init") is not -1:
            self.init_logger(message)
        if message.find("server_param") is not -1:
            print(message)
            self._server_param.parse(message)
        elif message.find("fullstate") is not -1 or message.find("player_type") is not -1 or message.find(
                "sense_body") is not -1 or message.find("(init") is not -1:
            self._full_world.parse(message)
        elif message.find("think") is not -1:
            self._think_mode = True

    def do_dash(self, power, angle):
        self._last_body_command.append(PlayerDashCommand(power, float(angle)))

    def do_turn(self, angle):
        self._last_body_command.append(PlayerTurnCommand(float(angle)))

    def do_move(self, x, y):
        self._last_body_command.append(PlayerMoveCommand(x, y))

    def world(self) -> WorldModel:
        return self._full_world

    def full_world(self) -> WorldModel:
        return self._full_world

    def logger(self):
        return self._logger

    def debug(self, msg):
        self.logger().debug(msg)

    def action(self):
        get_decision(self)
        commands = self._last_body_command
        # if self.world().our_side() == SideID.RIGHT:
            # PlayerCommandReverser.reverse(commands) # unused :\ # its useful :) # nope not useful at all :(
        if self._is_synch_mode:
            commands.append(PlayerDoneCommand())
        self._socket.send_msg(PlayerSendCommands.all_to_str(commands))
        self._last_body_command = []

    def init_logger(self, message: str):
        message = message.split(" ")
        unum = int(message[2])
        side = message[1]
        self._logger = setup_logger(f"dlog{unum}", f"debug/{side}{unum}.log", level=logging.DEBUG)