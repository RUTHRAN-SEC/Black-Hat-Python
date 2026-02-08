import socket                              # Import socket module for network communication

# Host or an IP address to which data will be sent
target_host = "127.0.0.1"                  # Loopback address (local machine)
target_port = 9997                         # Target UDP port number

# Creating a socket object
client = socket.socket(
    socket.AF_INET,                        # Use IPv4 addressing
    socket.SOCK_DGRAM                     # Use UDP protocol (connection-less)
)

# We are not connecting because UDP is connection-less
# Data can be sent directly without establishing a session

# Sending some data
client.sendto(
    b"HELLLLLLOOOO",                       # Message sent to the server
    (target_host, target_port)             # Destination IP and port
)

# Receiving data
data, addr = client.recvfrom(5096)         # Receive data and sender's address

# Decode and print the received message
print(data.decode())

# Close the UDP socket
client.close()
