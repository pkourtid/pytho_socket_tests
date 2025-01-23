import socket
import threading
import pickle
import time

class clsSimpleGameNetwork:
    lock_client_access = threading.Lock()
    
    def __init__(self):
        print("Created an instance of clsSimpleGameNetwork")
        self.bln_server_start = False
        # Create set to hold thread references for all the client threads
        self.set_client_threads = set()
        
    def resource_path(self, relative_path):
        # This function returns the full path to the current directory
        # It can be used to help find and read the messaging profile
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    # =========================================================================
    def server_message_thread(self, client_ip, client_port):
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
        
        
    # =========================================================================
    def client_message_thread(self, socket_connection):
        # Client code for all client threads
        client_connection = socket_connection[0]
        client_info = socket_connection[1]
        client_ip = client_info[0]
        client_port = client_info[1]
        print(" - New client connection ("+client_ip+","+str(client_port)+")")
        
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
                        print("Connection message: ")
                        client_info = str_message.split(":")
                        client_ip = client_info[0]
                        client_port = int(client_info[1])
                        print("IP: " + client_info[0])
                        print("PORT: " + client_info[1])
                        # threading.Thread(target=self.server_message_thread, args=(client_ip,client_port,)).start()
                    elif (str_message_type == "[M2]"):
                        print(str_message)
                str_messages = str_messages[int_search_result+len(self.str_message_end):]
                int_search_result = str_messages.find(self.str_message_end)
                
            data_received = str_messages
    
    # =========================================================================
    def server_working_thread(self,interface,port):
        # Set up a TCP/IP server
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
        # Bind the socket to server address and port
        server_address = ('localhost', 10000)
        self.tcp_socket.bind(server_address)
 
        # Listen on port
        self.tcp_socket.listen(1)
        print(" - Listening on port " + str(port))
        
        while True:
            print(" - Sever is waiting for connections")
            # Start a new thread to handle connected client
            thread_instance = threading.Thread(target=self.client_message_thread, args=(self.tcp_socket.accept(),))
            self.set_client_threads.add(thread_instance)
            thread_instance.start()
    
    # =========================================================================
    def init_server(self, interface, port):
        if (self.bln_server_start == False):
            print(" - Starting a server work thread")
            self.bln_server_start = True
            threading.Thread(target=self.server_working_thread, args=(interface, port,)).start()
        else:
            print(" - Server work thread already running")
    
     # =========================================================================
    def print_client_list(self):
        
        print(self.set_client_threads)
    
    
       
    