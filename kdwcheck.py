import socket

def sockcheck(ip, port, servername):
    sock = socket.socket()
    sock.settimeout(2)

    if sock.connect_ex((ip, port)):
        return servername + ' is Offline.'
    else:
        return servername + ' is Online.'
