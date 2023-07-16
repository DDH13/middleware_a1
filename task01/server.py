# Server

import socket
import sys

def main():
   
    if len(sys.argv) != 2:
        print("Correct usage: python3 server.py <port>")
        exit()
    
    PORT = int(sys.argv[1]) 
    ADDRESS = 'localhost'
    
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
        
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address[0]}:{client_address[1]}")

    while True:
        
        # receive data from client
        data = client_socket.recv(1024).decode()
        print(f"Received data: {data}")
        
        
        if data == 'terminate':
            client_socket.close()
            break
    
    print("Closing socket...")
    server_socket.close()
    
if __name__ == '__main__':
    main()