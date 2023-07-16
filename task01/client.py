# Client

import socket
import sys

def main():
    
    if len(sys.argv) != 3:
        print("Correct usage: python3 client.py <address> <port>")
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
    
    while True:
        
        # send data to server
        data = input("Enter data to send: ")
        client_socket.send(data.encode())
        
        if data == 'terminate':
            break
    
    print("Closing socket...")
    client_socket.close() 

    
if __name__ == "__main__":
    main()