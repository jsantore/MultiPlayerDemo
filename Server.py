import socket

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
    print(f" Server Address is: {server_address}")
    

if __name__ == '__main__':
    run_server()
