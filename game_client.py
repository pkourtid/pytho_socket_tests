import socket
import threading
import time
from random import randrange

# =============================================================================
# =============================================================================
def thread_server(client_ip, client_port):

    print ("The client IP is " + client_ip)
    print ("The server will be started on port " + str(client_port))
    
    # Set up a TCP/IP server
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
    # Bind the socket to server address and port
    server_address = (client_ip, client_port)
    tcp_socket.bind(server_address)
    tcp_socket.listen(1)
    
    client_connection, client_info = tcp_socket.accept()
    
    client_ip = client_info[0]
    client_port = client_info[1]
    print("Server connected from IP: {}".format(client_ip)) 
    print("Server connected from Port: {}".format(client_port))

    while True:
        data_received = client_connection.recv(32).decode('utf-8')
        print("Data received: " + data_received)

    print("Closing server connection")
    tcp_socket.close()
# =============================================================================
# =============================================================================
    
# Select the local IP address
client_ip_list = socket.gethostbyname_ex(socket.gethostname())[-1]
client_ip = client_ip_list[0]

# Select a random port between 10000 to 20000
client_port = 10000 + randrange(10000)

# Start a thread to listenfor the server connection
x = threading.Thread(target=thread_server, args=(client_ip,client_port,))
x.start()

# Create a connection to the server application
tcp_client_socket = socket.create_connection(('localhost', 10000))

# We will send our client connection info to the server
data = str.encode("[S][M1]"+client_ip+":"+str(client_port)+"[E]")
tcp_client_socket.sendall(data)

# We can now use the tcp_client_socket to send info to the server
# Create a signature
str_signature = "<" + client_ip + str(client_port) + ">"
while True:
    print("Heartbeat...")
    data = str.encode("[S][M2]"+str_signature+"[E]")
    tcp_client_socket.sendall(data)
    time.sleep(0.05)
    
#print("Closing client socket")
tcp_client_socket.close()
    
x.join()