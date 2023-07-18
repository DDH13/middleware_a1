# Server

import socket
import sys
import signal
import threading

server_socket = None

def main():

    if len(sys.argv) != 2:
        print("Correct usage: python3 server.py <port>")
    

    ADDRESS = 'localhost'
    PORT = int(sys.argv[1])

    # socket creation
    try:
        print("Creating socket...")
        server_socket = socket.socket()
    except socket.error as err:
        print(f"Socket creation failed with error: {err}")
        exit()
    
    print("Socket created successfully.")
    
    # forcefully bind socket to address and port
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # bind socket to address and port
    try:
        print("Binding socket...")
        server_socket.bind((ADDRESS, PORT))
    except socket.error as err:
        print(f"Socket binding failed with error: {err}")
        exit()
        
    print("Socket binded successfully.")
    
    # listen for incoming connections
    try:
        server_socket.listen(5)
    except socket.error as err:
        print(f"Socket listening failed with error: {err}")
        exit()
    
    print("Socket is listening.")

    # client list
    global client_list
    client_list = {
        'PUBLISHER': [],
        'SUBSCRIBER': []
    }
    client_topics = {}
        
    while True:
        # accept connection
        client_socket, client_address = server_socket.accept()
        print(f"Connected to {client_address[0]}:{client_address[1]}")
        
        # create thread for client
        client_thread = threading.Thread(target=client_handler, args=(client_socket, client_address, client_list, client_topics))
        client_thread.start()


def client_handler(client_socket, client_address, client_list, client_topics):

    # receive client details from client (client type)
    client_details = None
    try:
        client_details = client_socket.recv(1024).decode()
        client_type, client_topic = client_details.split('-')
        print (f'client details: {client_details}')
        # client_topic = client_socket.recv(1024).decode()
        if client_type != 'PUBLISHER' and client_type != 'SUBSCRIBER':
            client_socket.send("Invalid client type.".encode())
            client_socket.close()
            return

        client_list[client_type].append(client_socket)
        print(f'client topic: {client_topic}')
        client_topics[client_socket] = client_topic

    except socket.error as err:
        print(f"Socket error: {err}")
        client_socket.close()
        return
        
    while True:
        try:
            # receive data from client
            data = client_socket.recv(1024)
            if not data or data.decode() == 'terminate':
                break
            print(f"Received data from {client_address[0]}:{client_address[1]}")
            
            # send data to all clients in subscribe list with same topic
            for client in client_list['SUBSCRIBER']:
                if client != client_socket and client_topics[client] == client_topics[client_socket]:
                    client.send(data)
        
        except socket.error as err:
            print(f"Socket error: {err}")
            break
    
    print(f"Disconnected from {client_address[0]}:{client_address[1]}")
    client_socket.close()

    if client_details:
        client_type, client_topic = client_details.split('-')
        client_list[client_type].remove(client_socket)
        del client_topics[client_socket]

def sigint_handler(signal, frame):
    print("\nAdios Amigos...")

    # close all pub and sub sockets
    for client in client_list['PUBLISHER']:
        client.send("terminate".encode())
        client.close()
    for client in client_list['SUBSCRIBER']:
        client.send("terminate".encode())
        client.close()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, sigint_handler)
    main()