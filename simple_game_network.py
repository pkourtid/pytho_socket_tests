import socket
import threading
import time
from random import randrange

class clsSimpleGameNetwork:
    lock_client_access = threading.Lock()
    
    def __init__(self):
        print("*** __init__: Created an instance of clsSimpleGameNetwork")
        self.bln_server_start = False
        self.bln_client_start = False
        # Create set to hold thread references for all the client threads
        self.set_client_threads = set()
        
    def resource_path(self, relative_path):
        # This function returns the full path to the current directory
        # It can be used to help find and read the messaging profile
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
    # =========================================================================
    # SERVER CODE
    # =========================================================================
    # =========================================================================
    def server_message_thread(self, client_ip, client_port):
        print("The server is trying to connect to " + client_ip + " at port " + str(client_port))
        
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
            time.sleep(1)
    
        #print("Closing client socket")
        tcp_client_socket.close()
        
        
    # /////////////////////////////////////////////////////////////////////////
    # Used to receive data from each client thread
    def server_receiver(self, socket_connection):
        # Client code for all client threads
        client_connection = socket_connection[0]
        client_info = socket_connection[1]
        client_ip = client_info[0]
        client_port = client_info[1]
        print("*** client_message_thread: New client connection ("+client_ip+","+str(client_port)+")")
                
        self.str_message_start = "[S]"
        self.str_message_end = "[E]"
        
        data_received = ""
        
        while True:
            data_received = data_received +client_connection.recv(32).decode('utf-8')
            str_final_message = ""
            str_messages = data_received
            int_search_result = str_messages.find(self.str_message_end)
                
            while (int_search_result > -1):
                str_message = str_messages[:int_search_result]
                if (str_message[:3] == self.str_message_start):
                    str_message = str_message[3:]
                    str_message_type = str_message[:4]
                    str_message = str_message[4:]
                    # print("Got a valid message of type " + str_message_type)
                    if (str_message_type == "[M1]"):
                        #print("Connection message: ")
                        client_info = str_message.split(":")
                        client_ip = client_info[0]
                        client_port = int(client_info[1])
                        #print("IP: " + client_info[0])
                        #print("PORT: " + client_info[1])
                        threading.Thread(target=self.server_message_thread, args=(client_ip,client_port,)).start()
                    elif (str_message_type == "[M2]"):
                        print(str_message)
                str_messages = str_messages[int_search_result+len(self.str_message_end):]
                int_search_result = str_messages.find(self.str_message_end)
                
            data_received = str_messages
 
    # /////////////////////////////////////////////////////////////////////////
    def init_server(self, server_address, sever_port):
        # We will check if the server is already started
        if (self.bln_server_start == False):
            print("*** init_server: Starting a server...")
            self.bln_server_start = True
            threading.Thread(target=self.server_working_thread, args=(server_address, sever_port,)).start()
        else:
            print("*** init_server: Already started...")
            
    # /////////////////////////////////////////////////////////////////////////
    def server_working_thread(self, server_address, server_port):
        # Set up a TCP/IP server
        server_receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
        # Bind the socket to server address and port
        server_connection = (server_address, server_port)
        server_receiver_socket.bind(server_connection)
 
        # Listen on port
        server_receiver_socket.listen(1)
        print("*** server_working_thread: Waiting for connections on port " + str(server_port))
        while True:
            
            # Start a new thread to handle connected client
            thread_instance = threading.Thread(target=self.server_receiver, args=(server_receiver_socket.accept(),))
            self.set_client_threads.add(thread_instance)
            thread_instance.start()
 
    # =========================================================================
    # CLIENT CODE
    # =========================================================================
    
    # /////////////////////////////////////////////////////////////////////////
    # Used to receive data from the server (the server will connect to the receiver)
    def init_client(self, client_address='localhost', client_port=0, server_address='localhost', server_port=10000):
        print("*** init_client: Starting a client...")
        
        # Select a random port between 10000 to 20000
        if (client_port == 0):
            client_port = 10000 + randrange(10000)
            
        # Select the local IP address
        client_ip_list = socket.gethostbyname_ex(socket.gethostname())[-1]
        client_ip = client_ip_list[0]
        
        # Establish the server connection
        threading.Thread(target=self.client_receiver, args=(client_ip,client_port,)).start()
        time.sleep(3)
        # Start the connections to the server
        client_sender_socket = socket.create_connection((server_address, server_port))

        # As a client we will send a message to the server to tell it what port to connect to
        connect_to_me_message = "[S][M1]"+client_ip+":"+str(client_port)+"[E]"
        print("*** init_client: Sending message ["+connect_to_me_message+"]")
        client_sender_socket.sendall(connect_to_me_message.encode(encoding='UTF-8'))

        # return the socket to the caller so the 
        return client_sender_socket

    # /////////////////////////////////////////////////////////////////////////
    # Used to receive message from the server and communicate them to the client
    def client_receiver (self, client_address, client_port):
        print("*** client_receiver: Starting thread...")
        
        # Set up a TCP/IP server
        client_receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
        # Bind the socket to server address and port
        receiver_address = (client_address, client_port)
        client_receiver_socket.bind(receiver_address)
 
        # Listen on port
        client_receiver_socket.listen(1)
        print("*** client_receiver: Listening on port " + str(client_port))
        
        # listen for server connection
        socket_connection = client_receiver_socket.accept()
        
        # Client code for all client threads
        client_connection = socket_connection[0]
        client_info = socket_connection[1]
        client_ip = client_info[0]
        client_port = client_info[1]
        print("*** client_receiver: New connection ("+client_ip+","+str(client_port)+")")
        data_received = ""  
        
        # We can now receive data from the server        
        while True:
            data_received = client_connection.recv(32).decode('utf-8')
            print ("*** client_receiver: Received <"+data_received+">")
            data_received = ""
            
     # =========================================================================
    def print_client_list(self):
        print(self.set_client_threads)
    
    
       
    