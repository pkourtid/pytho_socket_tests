import socket
import threading
import time

class clsMessageEngine:

    #def resource_path(self, relative_path):
	#	base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
	#	return os.path.join(base_path, relative_path)
    
    def __init__(self, spec_reference):
        print("msge> Init...")
        self.str_message_start = "[S]"
        self.str_message_end = "[E]"
        
    def process(self, str_messages):
        str_final_message = ""
        int_search_result = str_messages.find(self.str_message_end)
        
        while (int_search_result > -1):
            str_message = str_messages[:int_search_result]
            if (str_message[:3] == self.str_message_start):
                str_message = str_message[3:]
                str_message_type = str_message[:4]
                str_message = str_message[4:]
                # print("Got a valid message of type " + str_message_type)
                if (str_message_type == "[M1]"):
                    print("Connection message: ")
                    client_info = str_message.split(":")
                    client_ip = client_info[0]
                    client_port = int(client_info[1])
                    print("IP: " + client_info[0])
                    print("PORT: " + client_info[1])
                    x = threading.Thread(target=thread_server, args=(client_ip,client_port,))
                    x.start()
                elif (str_message_type == "[M2]"):
                    print(str_message)
            str_messages = str_messages[int_search_result+len(self.str_message_end):]
            int_search_result = str_messages.find(self.str_message_end)

        return str_messages
            
# =============================================================================
# This function will be used for communication between the connected client
# and the server.
def thread_server(client_ip, client_port):

    # Create a connection to the server application
    tcp_client_socket = socket.create_connection((client_ip, client_port))

    # We will send our client connection info to the server
    data = str.encode("[S][M1]I AM THE SERVER [E]")
    tcp_client_socket.sendall(data)

    # Create a signature
    str_signature = "<" + client_ip + str(client_port) + ">"

    # We can now use the tcp_client_socket to send info to the server
    while True:
        data = str.encode("[S][M2]I AM THE SERVER [E]")
        tcp_client_socket.sendall(data)
        time.sleep(2)
    
    #print("Closing client socket")
    tcp_client_socket.close()

# =============================================================================
# The client Thread ===========================================================

def thread_client(socket_connection):
    
    print(f"Started Client Thread")
    
    # Set variables
    obj_client_messages = clsMessageEngine("")
    client_connection = socket_connection[0]
    client_info = socket_connection[1]
    client_ip = client_info[0]
    client_port = client_info[1]
    print("Connected to client IP: {}".format(client_ip)) 
    print("Connected to client Port: {}".format(client_port))
    
    data_received = ""
    
    while True:
        data_received = data_received +client_connection.recv(32).decode('utf-8')
        # process messages up to this point
        data_received = obj_client_messages.process(data_received)
        
# Set up a TCP/IP server
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
# Bind the socket to server address and port
server_address = ('localhost', 10000)
tcp_socket.bind(server_address)
 
# Listen on port
tcp_socket.listen(1)
 
while True:
    print("Waiting for connection")
    threading.Thread(target=thread_client, args=(tcp_socket.accept(),)).start()
 
