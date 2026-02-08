# SSH Paramiko Project

SSH Paramiko – Secure Remote Command Execution Using Python

## Project Description

This project demonstrates how two computers can securely communicate using SSH (Secure Shell) with Python.

SSH works like a secure and encrypted tunnel that allows one computer to send commands to another computer safely. 
Only users with the correct username and password can access the system.

In this project:
- A Python-based SSH server waits for connections
- A client connects securely to the server
- Commands are sent, executed, and results are returned safely

This project uses the Paramiko library, which allows SSH communication without using a traditional terminal.

## Project Structure
- ssh_server.py -> Custom SSH server implementation
- ssh_cmd.py -> Simple SSH client for single command execution
- ssh_rcmd.py -> Remote command execution client

## File Explanation

### ssh_server.py
- Acts as a custom SSH server
- Listens on port [ 2222 ]
- Authenticates users using username and password
- Sends commands to the client
- Receives command output securely

### ssh_cmd.py
- SSH client for single command execution
- Connects to the SSH server
- Executes one command
- Displays output and errors
- Closes the connection

### ssh_rcmd.py
- Interactive SSH client
- Maintains a persistent SSH session
- Receives commands from the server
- Executes them locally
- Sends output back to the server

## Learning Objectives
- Understand how SSH works
- Learn client–server communication
- Use Paramiko for secure connections
- Execute remote commands securely
- Understand authentication and encryption
- Learn basic SSH security concepts

## Project Requirements
- Basic Python knowledge
- Understanding of networking basics
- Familiarity with client–server architecture
- Interest in cybersecurity concepts


## Software Requirements
- Python 3.14
- Paramiko library
- Terminal / Command Prompt

Install Paramiko: pip install paramiko

## Python Libraries Used

- paramiko – SSH protocol handling
- socket – Network communication
- threading – Multi-threading support
- subprocess – Command execution
- shlex – Safe command parsing
- os – File system operations
- sys – System operations
- getpass – Secure password input

## System Requirements
- Any OS (Windows / Linux / macOS)
- Minimum 2 GB RAM
- Open port 2222
- Python installed

## Security Relevance
This project is important for cybersecurity learning, especially in:
- SOC Operations
- Penetration Testing
- Red Team / Blue Team activities
- Secure remote administration
- Understanding SSH vulnerabilities

## Security Concepts Covered:
- SSH authentication
- Encrypted communication
- Remote command execution risks
- Hardcoded credential dangers
- SSH server misconfiguration risks

## ⚠️ Disclaimer

This project is intended strictly for educational and ethical purposes.
All testing must be performed only on systems you own or have explicit authorization to test.
The author is not responsible for any misuse or illegal activity resulting from the use of this project.

## Author
### RUTHRAN-SEC
