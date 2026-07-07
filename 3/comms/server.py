import socket
import struct

MULTICAST_GROUP = '224.1.1.1'
PORT = 5007

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind(('', PORT))

group = socket.inet_aton(MULTICAST_GROUP)

server_socket.setsockopt(
    socket.IPPROTO_IP,
    socket.IP_ADD_MEMBERSHIP,
    group + socket.inet_aton('0.0.0.0')
)

print(f"Listening on {MULTICAST_GROUP}:{PORT}")

while True:
    data, addr = server_socket.recvfrom(1024)
    print(f"{addr}: {data.decode()}")