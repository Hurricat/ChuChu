import socket

def status(ip, port):
    sock = socket.socket()
    sock.settimeout(2)

    if sock.connect_ex((ip, port)):
        return 'KDW is Offline.'
    else:
        return 'KDW is Online.'
