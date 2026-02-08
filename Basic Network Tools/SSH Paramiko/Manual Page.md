# SSH Paramiko – Manual Page

## NAME
**ssh-paramiko** — Python-based SSH client and server for secure remote command execution

---

## SYNOPSIS

```bash
python ssh_server.py
python ssh_cmd.py
python ssh_rcmd.py
DESCRIPTION
This project provides a simple SSH implementation using Python and Paramiko.

It allows:

Secure authentication using username and password

Encrypted communication between two systems

Remote command execution

Interactive command exchange

The project consists of three scripts:

SSH Server

Single-command SSH Client

Interactive Remote Command Client

FILES
ssh_server.py
Creates a custom SSH server that listens for incoming SSH connections.

Default Host: localhost

Default Port: 2222

Authentication: Username & Password

Uses RSA key for encryption

ssh_cmd.py
A basic SSH client used to:

Connect to the SSH server

Execute one command

Display output and errors

Close the connection

ssh_rcmd.py
An interactive SSH client that:

Keeps the SSH session open

Receives commands from the server

Executes them locally

Sends results back

INSTALLATION
1️⃣ Install Python (if not installed)
python --version
2️⃣ Install Required Library
pip install paramiko
3️⃣ Generate SSH Host Key (Required)
ssh-keygen -t rsa -f test_rsa.key
USAGE
🔹 Start the SSH Server
python ssh_server.py
Output:

[+] Listening on port 2222
🔹 Execute a Single Command (Client)
python ssh_cmd.py
User input:

Username: tim
Password:
Enter Server IP: localhost
Enter Port or <CR>: 2222
Enter Command or <CR>: id
🔹 Start Interactive Remote Command Client
python ssh_rcmd.py
User input:

Enter server IP : localhost
Enter port : 2222
AUTHENTICATION
Default credentials (configured in server):

Username: tim
Password: seccrret
⚠️ Change credentials before real usage.

COMMAND FLOW
Client connects to SSH server

Server authenticates the client

Encrypted session is established

Commands are exchanged securely

Output is returned to the sender

EXITING
To terminate an SSH session:

exit
Or press:

Ctrl + C
TROUBLESHOOTING
Port already in use
Address already in use
➡ Change port number or close existing service

Authentication failed
Authentication failed
➡ Verify username and password

No channel error
[-] No channel.
➡ Check SSH key and Paramiko version

SECURITY NOTES
Communication is encrypted using SSH

Hardcoded credentials are insecure

Do NOT expose this server to the internet

Use strong passwords and key-based auth in production

DISCLAIMER
This project is for educational and lab use only.

Do NOT use on unauthorized systems.
The author is not responsible for misuse.
