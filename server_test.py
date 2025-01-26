from simple_game_network import *
import time

obj_network = clsSimpleGameNetwork()
obj_network.init_server('localhost', 10000)

time.sleep(3)

obj_client_socket = obj_network.init_client()

while True:
    obj_network.print_client_list()
    time.sleep(2)