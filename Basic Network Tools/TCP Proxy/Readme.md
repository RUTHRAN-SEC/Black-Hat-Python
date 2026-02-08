# **TCP Proxy – Network Traffic Interception Tool (Python)**


## Project Description
This project is a TCP Proxy, which works like a middleman between two computers communicating over a network.

Instead of connecting directly, all data passes through the proxy. This allows the proxy to view, log, and analyze the data being exchanged. 
The proxy can also display traffic in hexadecimal format, making it useful for understanding low-level network communication.

- A client sends data
- The proxy receives it
- The proxy forwards it to the server
- The server’s response comes back through the proxy

This project is mainly built for learning networking and cybersecurity concepts, not for production use.

## Learning Objectives
By completing this project, you will learn:
- How TCP communication works
- How proxy servers intercept network traffic
- How data flows between client and server
- How to analyze raw network data using hex dumps
- How threading helps manage multiple connections
- Core concepts used in SOC and security tools

## Requirements for the Project
- Basic knowledge of Python programming
- Understanding of TCP/IP networking
- Familiarity with client-server architecture
- A safe lab or local network environment for testing

## Software Requirements
- Python 3.14
- Command-line terminal
- Code editor (VS Code recommended)

## Python Libraries Used
This project uses only built-in Python libraries:
- `socket` – for network communication
- `threading` – for handling multiple connections
- `sys` – for command-line arguments
- No external libraries are required.


## System Requirements
- Operating System: Windows / Linux / macOS
- Minimum 4 GB RAM (recommended)
- Python 3 installed and configured
- Network access (local or lab setup)

## Security Relevance
This TCP Proxy is useful in cybersecurity for:
- Network traffic monitoring
- Malware analysis labs
- Penetration testing practice
- Understanding how attacks intercept data
- SOC and DFIR learning environments

It helps security professionals understand how data moves across a network and how it can be inspected.

## ⚠️ Disclaimer

This project is intended strictly for educational and ethical purposes.
All testing must be performed only on systems you own or have explicit authorization to test.
The author is not responsible for any misuse or illegal activity resulting from the use of this project.

## Author
### RUTHRAN-SEC

