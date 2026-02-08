import socket                          # Import the socket module for network communication

# Creating a host and port to connect
target_host = "www.google.com"         # Target domain name to connect to
target_port = 80                      # Port 80 is used for HTTP traffic

# Creating a socket object
client = socket.socket(
    socket.AF_INET,                   # Use IPv4 addressing
    socket.SOCK_STREAM                # Use TCP (connection-oriented protocol)
)

# Connecting to the target host and port
client.connect((target_host, target_port))

# Sending some data
client.send(
    b"GET / HTTP/1.1\r\n"              # HTTP GET request for the root page
    b"Host:google.com\r\n"             # Host header specifying the domain
    b"\r\n"                            # Blank line indicating end of HTTP headers
)

# Receiving some data
response = client.recv(4096)           # Receive up to 4096 bytes of data from the server

# Decode and print the server response
print(response.decode())

# Close the socket connection
client.close()
