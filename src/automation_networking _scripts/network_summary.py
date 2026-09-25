import socket

# Return the machine hostname.
def get_hostname():
    return socket.gethostname()

# Return the local IPv4 address assigned to the hostname.
def get_local_ip():
    return socket.gethostbyname(socket.gethostname())

# Print basic network identity information.
def main():
    hostname = get_hostname()
    local_ip = get_local_ip()
    print(f"Hostname: {hostname}")
    print(f"Local IP: {local_ip}")


if __name__ == "__main__":
    main()
