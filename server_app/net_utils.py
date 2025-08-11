# net_utils.py

import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80)) # connect to google dns server to get local ip
        ip = s.getsockname()[0]
    except Exception: # if google dns server broken, use localhost ip (won't work for other devices in the network)
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip