import paramiko            # Paramiko is used to handle SSH connections in Python


def ssh_command(ip, port, user, passwd, cmd):
    # Create an SSH client object
    client = paramiko.SSHClient()

    # Automatically add unknown SSH host keys (no manual verification)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the remote SSH server using IP, port, username, and password
    client.connect(ip, port=port, username=user, password=passwd)

    # Execute the command on the remote server
    _, stdout, stderr = client.exec_command(cmd)

    # Read command output from stdout
    output = stdout.read().decode()

    # Read error output from stderr
    error = stderr.read().decode()

    # Print command output if available
    if output:
        print('--- Output ---')
        for line in output.splitlines():
            print(line)

    # Print error messages if any occurred
    if error:
        print('--- Error ---')
        for line in error.splitlines():
            print(line)

    # Close the SSH connection
    client.close()


# Main entry point of the script
if __name__ == '__main__':
    import getpass          # Used to securely take password input without showing it

    # Prompt user for SSH username
    user = input('Username: ')

    # Prompt user for password (hidden input)
    password = getpass.getpass()

    # Prompt for server IP, default to localhost if empty
    ip = input('Enter Server IP: ') or 'localhost'

    # Prompt for SSH port, default to 2222 if empty
    port = int(input('Enter Port or <CR>: ') or 2222)

    # Prompt for command to execute, default to 'id' if empty
    cmd = input('Enter Command or <CR>: ') or 'id'

    # Call the SSH command execution function
    ssh_command(ip, port, user, password, cmd)
