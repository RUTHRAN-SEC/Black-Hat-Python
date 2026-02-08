import os              # Used for file path handling
import paramiko        # Used to create SSH server and handle SSH protocol
import socket          # Used for network socket communication
import sys             # Used for system-level operations like exit
import threading       # Used for thread synchronization

# Get the current working directory of this file
CWD = os.path.dirname(os.path.realpath(__file__))

# Load the RSA host key for the SSH server
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, "test_rsa.key"))

# Define a custom SSH server class
class Server(paramiko.ServerInterface):
    def __init__(self):
        # Event used to manage threading synchronization
        self.event = threading.Event()

    # Handle incoming channel requests
    def check_channel_request(self, kind, chanid):
        # Allow only "session" type channels
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    # Authenticate user using username and password
    def check_auth_password(self, username, password):
        # Hardcoded credentials for authentication
        if (username == "tim") and (password == "seccrret"):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    # Allow opening of the SSH channel
    def check_channel_opened(self, kind, chanid):
        return paramiko.OPEN_SUCCEEDED

if __name__ == "__main__":
    # Define SSH server host and port
    HOST = "localhost"
    ssh_port = 2222

    try:
        # Create a TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Allow socket reuse to avoid address already in use error
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind socket to host and port
        sock.bind((HOST, ssh_port))
    except Exception as e:
        # Print error if socket binding fails
        print("[-] listen failed: " + str(e))
        sys.exit(1)
    
    # Start listening for incoming connections
    sock.listen(100)
    print("[+] Listening on port", ssh_port)

    # Accept an incoming client connection
    client, addr = sock.accept()
    print("[+] Got a connection from", addr)

    # Create an SSH transport session using the accepted socket
    bhSession = paramiko.Transport(client)

    # Add the server host key to the SSH session
    bhSession.add_server_key(HOSTKEY)

    # Create server handler instance
    server_handler = Server()

    # Start the SSH server
    bhSession.start_server(server=server_handler)

    # Accept an SSH channel with a timeout
    chan = bhSession.accept(20)
    if chan is None:
        print("[-] No channel.")
        sys.exit(1)

    # Authentication successful
    print("[+] Authenticated!")

    # Receive initial data sent by client
    print(chan.recv(1024).decode())

    # Send welcome message to the client
    chan.send(b"Welcome to bh_ssh")

    try:
        while True:
            # Take command input from server-side user
            command = input("Enter command: ")

            if command != "exit":
                # Send command to SSH client
                chan.send(command.encode())

                # Receive command output from client
                response = chan.recv(1024)
                if response:
                    print(response.decode())
            else:
                # Send exit command and close session
                chan.send(b"exit")
                print("exiting.")
                bhSession.close()
                break
    except KeyboardInterrupt:
        # Close SSH session on keyboard interrupt
        bhSession.close()
