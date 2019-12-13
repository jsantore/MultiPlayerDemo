import asyncio
import threading
import arcade
import PlayerState
import pathlib
import socket
import Server
import json


class GameClient(arcade.Window) :
    def __init__(self, server, client_ip_addr):
        super().__init__(PlayerState.WINDOW_WIDTH, PlayerState.WINDOW_HEIGHT)
        self.ip_addr = client_ip_addr
        self.image_path = pathlib.Path.cwd() / 'Assets' / 'captain1.png'
        self.player = arcade.Sprite(self.image_path)
        self.target = arcade.Sprite(str(pathlib.Path.cwd()/'Assets'/'gold-coins.png'))
        self.server_address = server
        self.player_list = arcade.SpriteList()
        self.target_list = arcade.SpriteList()
        self.target_list.append(self.target)
        self.player_list.append(self.player)
#        self.player_state_list = PlayerState.GameState(player_states=[])
        self.actions = PlayerState.PlayerMovement()

    def setup(self):
        self.player = arcade.Sprite(self.image_path)
        self.player_list.append(self.player)
        self.from_server = ""

    def on_update(self, delta_time: float):
        pass

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()
        self.target_list.draw()
        arcade.draw_text(f"Your Score {self.from_server}", 100, 900, color=(240, 30, 30), font_size=24)

    def on_key_press(self, key: int, modifiers: int):
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
        data = data_packet[0] #get the encoded string
        decoded_data:PlayerState.GameState = PlayerState.GameState.from_json(data)
        player_dict = decoded_data.player_states
        target:PlayerState.TargetState = decoded_data.target
        client.target.center_x = target.xLoc
        client.target.center_y = target.yloc
        player_info:PlayerState.PlayerState = player_dict[client.ip_addr]
        client.from_server = player_info.points
        client.player.center_x = player_info.x_loc
        client.player.center_y = player_info.y_loc

def main():
    client_address = Server.find_ip_address()
    server_address = input("what is the IP address of the server:")
    game = GameClient(server_address, client_address)
    game.setup()
    client_thread = threading.Thread(target=setup_client_connection, args=(game,), daemon=True)
    client_thread.start()
    arcade.run()

if __name__ == '__main__':
    main()



