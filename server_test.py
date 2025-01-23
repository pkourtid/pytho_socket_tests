from simple_game_network import *

obj_network = clsSimpleGameNetwork()
obj_network.init_server('localhost', 10000)

while True:
    obj_network.print_client_list()
    time.sleep(2)