import socket
import argparse
import time 

def scan_port(host,port):
    try:
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
            
             sock.connect_ex(host,port)
             return  socket.gethostbyname(host)
                
              
        time.sleep(0.5)
         
    except Exception as e:
        return ("there is not host to scan",e)





def parse_args():
    parser = argparse.ArgumentParser(description="Port scanner")
    parser.add_argument("host",help= "target host")
    parser.add_argument("port",help = "number of ports")
    return parser.parse_args()



def main():
    args = parse_args()
    host = args.host
    port = args.port

    result = scan_port(host, port)

    print("target host:", host)
    print("port checked:", port)
    print(result)





if __name__=="__main__":
    main()

