import socket

# Look up the IPv4 address for a hostname.
def lookup_host(hostname):
    return socket.gethostbyname(hostname)



def main():

    hostname = input("Enter a hostname:")
    print(socket.gethostbyname(hostname))

    
  


if __name__ == "__main__":
    main()
