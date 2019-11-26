import socket
import PlayerState

SERVER_PORT = 25001

all_players = {} #key is IP address, value is PlayerState.PlayerState

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

def run_server():
    server_address = find_server_address()
    print(f" Server Address is: {server_address}, on prt {SERVER_PORT}")
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind((server_address, SERVER_PORT))
    while(True):
        data_packet = UDPServerSocket.recvfrom(1024)
        message = data_packet[0] #data is first in tuple
        client_addr = data_packet[1] #client IP is second
        if not client_addr in all_players: #first time this client connected
            offset = len(all_players)+1
            new_player = PlayerState.PlayerState(200*offset, 200*offset)
            all_players[client_addr] = new_player
        print(f"Debug got {message} from {client_addr}")
        UDPServerSocket.sendto(str.encode("Got it - more to come"), client_addr)


if __name__ == '__main__':
    run_server()
