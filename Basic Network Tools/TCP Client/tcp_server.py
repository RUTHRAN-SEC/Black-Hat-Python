import socket              # Imports the socket module to enable network communication
import threading           # Imports threading to handle multiple clients simultaneously

ip = "0.0.0.0"             # Binds the server to all available network interfaces
port = 9999                # Port number on which the server will listen

def main():
    # Create a TCP socket using IPv4 addressing
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the specified IP address and port
    server.bind((ip, port))
    
    # Put the server into listening mode (max 5 queued connections)
    server.listen(5)
    
    # Display server listening status
    print(f"[*] Listening on {ip}:{port}")
    
    # Infinite loop to keep the server running
    while True:
        # Accept an incoming client connection
        client, addr = server.accept()
        
        # Print the connected client's IP address and port
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        
        # Create a new thread to handle the client connection
        client_handler = threading.Thread(
            target=handle_client,     # Function to handle client communication
            args=(client,)            # Pass the client socket as an argument
        )
        
        # Start the client handler thread
        client_handler.start()

def handle_client(client_socket):
    # Use context manager to automatically close the socket after use
    with client_socket as sock:
        
        # Receive up to 1024 bytes of data from the client
        request = sock.recv(1024)
        
        # Decode and print the received data
        print(f"[*] Received: {request.decode('utf-8')}")
        
        # Send an acknowledgment message back to the client
        sock.send(b"ACK")

# Check if the script is being run directly
if __name__ == "__main__":
    main()                  # Call the main function to start the server
