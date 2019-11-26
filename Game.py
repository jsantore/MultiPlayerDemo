import asyncio
import threading
import arcade
import PlayerState
import pathlib
import socket
import Server
import json

class GameClient(arcade.Window) :
    def __init__(self, server):
        super().__init__(PlayerState.WINDOW_WIDTH, PlayerState.WINDOW_HEIGHT)
        self.image_path = pathlib.Path.cwd() / 'Assets' / 'captain1.png'
        self.player = None
        self.server_address = server
        self.player_list = arcade.SpriteList()
        self.player_state_list = PlayerState.GameState(player_states=[PlayerState.PlayerState(0, 0)])
        self.actions = PlayerState.PlayerMovement()

    def setup(self):
        self.player = arcade.Sprite(self.image_path)
        self.player_list.append(self.player)
        self.from_server = ""

    def on_update(self, delta_time: float):
        pass

    def on_draw(self):
        self.player_list.draw()
        arcade.draw_text(f"Got {self.from_server} from server", 200, 200, color=(240, 30, 30), font_size=24)

    def on_key_press(self, key: int, modifiers: int):
        print(f"DEBUG key press{key}")
        if(key in self.actions.keys):
            self.actions.keys[key] = True

    def on_key_release(self, symbol: int, modifiers: int):
        if(symbol in self.actions.keys):
            self.actions.keys[symbol] = False


def setup_client_connection(client: GameClient):
    client_event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(client_event_loop)
    client_event_loop.create_task(communication_with_server(client, client_event_loop))
    client_event_loop.run_forever()


async  def communication_with_server(client: GameClient, event_loop):
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    while True:
        keystate = json.dumps(client.actions.keys)
        UDPClientSocket.sendto(str.encode(keystate), (client.server_address, Server.SERVER_PORT))
        data_packet = UDPClientSocket.recvfrom(1024)
        data = data_packet[0]
        client.from_server = data

def main():
    server_address = input("what is the IP address of the server:")
    game = GameClient(server_address)
    game.setup()
    client_thread = threading.Thread(target=setup_client_connection, args=(game,), daemon=True)
    client_thread.start()
    arcade.run()

if __name__ == '__main__':
    main()



