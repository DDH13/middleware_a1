# Client

import socket
import sys

def main():
    
    if len(sys.argv) != 4:
        print("Correct usage: python3 client.py <address> <port> <PUBLISHER | SUBSCRIBER>")
        exit()
    
    ADDRESS = sys.argv[1]
    PORT = int(sys.argv[2])
    
    # socket creation
    try:
        print("Creating socket...")
        client_socket = socket.socket()
    except socket.error as err:
        print(f"Socket creation failed with error: {err}")
        exit()
        
    print("Socket created successfully.")
    
    # connect to server
    try:
        print("Connecting to server...")
        client_socket.connect((ADDRESS, PORT))
    except socket.error as err:
        print(f"Socket connection failed with error: {err}")
        exit()
    
    print("Connected to server successfully.")

    # send client type to server
    client_socket.send(sys.argv[3].encode())
    
    while True:
        
        if sys.argv[3] == 'PUBLISHER':
            # send data to server
            data = input("Enter data to send: ")
            client_socket.send(data.encode())
            
            if data == 'terminate':
                break
        else:
            # receive data from server
            data = client_socket.recv(1024).decode()
            print(f"Received data: {data}")
                
            if data == 'terminate':
                break        
    
    print("Closing socket...")
    client_socket.close() 

    
if __name__ == "__main__":
    main()