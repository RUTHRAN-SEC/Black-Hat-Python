import sys              # Provides access to command-line arguments and system exit
import socket           # Used for network communication (TCP sockets)
import threading        # Allows handling multiple connections at the same time


def hexdump(src, length=16, show=True):
    """
    Converts raw bytes into a readable hexadecimal + ASCII format.
    Useful for analyzing network traffic at byte level.
    """

    # If the input is a string, convert it to bytes
    if isinstance(src, str):
        src_bytes = src.encode(errors='replace')
    else:
        src_bytes = src  # If already bytes, keep as-is

    results = []  # List to store formatted hex dump lines

    # Process data in chunks (default 16 bytes per line)
    for i in range(0, len(src_bytes), length):
        chunk = src_bytes[i:i+length]               # Extract a chunk of bytes
        hexa = ' '.join(f'{b:02X}' for b in chunk)  # Convert bytes to hex
        printable = ''.join(
            (chr(b) if 32 <= b < 127 else '.') for b in chunk
        )                                           # Convert bytes to readable ASCII
        hexwidth = length * 3                       # Used for alignment
        results.append(f'{i:04X} {hexa:<{hexwidth}} {printable}')

    # Print output directly if show=True
    if show:
        for line in results:
            print(line)
    else:
        return results


def receive_from(connection):
    buffer = b''              # Store received data
    connection.settimeout(2)  # Stop waiting after 2 seconds

    try:
        while True:
            data = connection.recv(4096)  # Receive up to 4096 bytes
            if not data:
                break                     # Stop if no data is received
            buffer += data                # Append received data
    except socket.timeout:
        pass                              # Ignore timeout errors

    return buffer                         # Return all received data


def request_handler(buffer):
    # This function can be used to modify outgoing packets
    # Currently, it returns data without modification
    return buffer


def response_handler(buffer):
    # This function can be used to modify incoming packets
    # Currently, it returns data without modification
    return buffer


def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    # Create a socket to connect to the remote server
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))  # Connect to remote server

    remote_buffer = b''  # Buffer to store remote data

    # Some services send data first (like FTP banners)
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        if remote_buffer:
            hexdump(remote_buffer)                    # Display received data
            remote_buffer = response_handler(remote_buffer)
            if len(remote_buffer):
                print("[<==] Sending %d bytes to localhost." % len(remote_buffer))
                client_socket.send(remote_buffer)     # Send data to client

    # Main proxy loop
    while True:
        local_buffer = receive_from(client_socket)     # Receive data from client

        if len(local_buffer):
            line = "[==>] Received %d bytes from localhost." % len(local_buffer)
            print(line)
            hexdump(local_buffer)                      # Show client data
            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)           # Forward to remote server
            print("[==>] Sent to remote.")

        # Receive response from remote server
        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("[<==] Received %d bytes from remote." % len(remote_buffer))
            hexdump(remote_buffer)                     # Show server data
            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)          # Send back to client
            print("[<==] Sent to localhost.")

        # Close connection if no data from both sides
        if not len(local_buffer) and not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connections.")
            break


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    # Create a TCP server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host, local_port))  # Bind proxy to local IP and port
    except Exception as e:
        print('problem on bind: %r' % e)
        print("[!!] Failed to listen on %s:%d" % (local_host, local_port))
        print("[!!] Check for other listening sockets or correct permissions.")
        sys.exit(0)

    print("[*] Listening on %s:%d" % (local_host, local_port))
    server.listen(5)  # Allow up to 5 pending connections

    while True:
        client_socket, addr = server.accept()   # Accept incoming connection
        line = "[==>] Received incoming connection from %s:%d" % (addr[0], addr[1])
        print(line)

        # Handle each connection in a separate thread
        proxy_thread = threading.Thread(
            target=proxy_handler,
            args=(client_socket, remote_host, remote_port, receive_first)
        )
        proxy_thread.start()


def main():
    # Ensure correct number of command-line arguments
    if len(sys.argv[1:]) != 5:
        print("Usage: ./tcp_proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]")
        print("Example: ./tcp_proxy.py 127.0.0.1 9000 10.12.132.1 9001 True")
        sys.exit(0)

    # Read command-line arguments
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    receive_first = sys.argv[5]

    # Convert receive_first flag to boolean
    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    # Start the proxy server
    server_loop(local_host, local_port, remote_host, remote_port, receive_first)


# Entry point of the program
if __name__ == '__main__':
    main()
