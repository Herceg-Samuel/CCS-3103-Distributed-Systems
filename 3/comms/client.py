import socket
import struct

MULTICAST_GROUP = "224.1.1.1"
PORT = 5007

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

ttl = struct.pack('b', 1)
client.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

while True:
    msg = input("Message: ")
    client.sendto(msg.encode(), (MULTICAST_GROUP, PORT))