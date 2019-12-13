import socket
import PlayerState
import json
import arcade
from typing import Dict
import datetime

SERVER_PORT = 25001

all_players:Dict[str, PlayerState.PlayerState] = {}  #key is IP address, value is PlayerState.PlayerState

def find_server_address():
    """returns the LAN IP address of the current machine as a string
    A minor revision of this answer:
    https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib#28950776"""
    server_address = ""
    connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        connection.connect(('10.255.255.255', 1))
        server_address = connection.getsockname()[0]
    except IOError:
        server_address = '127.0.0.1'
    finally:
        connection.close()
    return server_address


def process_player_move(player_move: PlayerState.PlayerMovement, client_addr: str):
    #don't process events too fast, only once every 20 miliseconds
    player_info = all_players[client_addr]
    now = datetime.datetime.now()
    if player_info.last_update +datetime.timedelta(milliseconds=20)  > now:
        return
    player_info.last_update = now
    delta_x = 0
    delta_y = 0
    if player_move.keys[str(arcade.key.UP)]:
        delta_y = 3
    elif player_move.keys[str(arcade.key.DOWN)]:
        delta_y = -3
    if player_move.keys[str(arcade.key.LEFT)]:
        delta_x = -3
    elif player_move.keys[str(arcade.key.RIGHT)]:
        delta_x = 3
    all_players[client_addr].x_loc += delta_x
    if all_players[client_addr].x_loc < 0:
        all_players[client_addr].x_loc = 20
    elif all_players[client_addr].x_loc > PlayerState.WINDOW_WIDTH:
        all_players[client_addr].x_loc = PlayerState.WINDOW_WIDTH - 20
    if all_players[client_addr].y_loc < 0:
        all_players[client_addr].y_loc = 20
    elif all_players[client_addr].y_loc > PlayerState.WINDOW_HEIGHT:
        all_players[client_addr].y_loc = PlayerState.WINDOW_HEIGHT - 20
    all_players[client_addr].y_loc += delta_y
 #   print(all_players[client_addr])


def run_server():
    server_address = find_server_address()
    print(f" Server Address is: {server_address}, on prt {SERVER_PORT}")
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind((server_address, SERVER_PORT))
    while(True):
        data_packet = UDPServerSocket.recvfrom(1024)
        message = data_packet[0]  # data is first in tuple
        client_addr = data_packet[1]  # client IP is second
        if not client_addr in all_players:  # first time this client connected
            offset = len(all_players)+1
            #create new player with x and y positions, 0 points and a last update of now
            new_player:PlayerState.PlayerState = PlayerState.PlayerState(200*offset, 200*offset, 0, datetime.datetime.now())
            all_players[client_addr] = new_player
#        print(f"Debug got {message} from {client_addr}")
        json_data = json.loads(message)
#       print(json_data)
        player_move: PlayerState.PlayerMovement = PlayerState.PlayerMovement()
        player_move.keys = json_data
        process_player_move(player_move, client_addr)
        print(F"Debug: the player was: {all_players[client_addr]}")
        response = all_players[client_addr].to_json()
        print(f"DEbug server about to send response: {response}")
        UDPServerSocket.sendto(str.encode(response), client_addr)


if __name__ == '__main__':
    run_server()
