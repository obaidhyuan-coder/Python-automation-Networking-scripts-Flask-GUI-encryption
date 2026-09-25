import socket

# Send an empty UDP packet and infer whether the port is responsive.
def scan_udp_port(host, port, timeout):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.sendto(b"", (host, port))
            return True
        except OSError:
            return False

# Prompt the user for a hostname and port range, then scan each UDP port.
def main():
    host = input("Enter your host: ")
    start_port = int(input("Enter your start port: "))
    end_port = int(input("Enter your end port: "))
    timeout = 1.0
    for port in range(start_port, end_port + 1):
        if scan_udp_port(host, port, timeout):
            print(f"Port {port} is open")
        else:
            print(f"Port {port} is closed")

if __name__ == "__main__":
    main()



