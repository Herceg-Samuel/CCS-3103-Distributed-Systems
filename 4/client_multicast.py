import socket
import struct
import threading
import sys
from cryptography.fernet import Fernet

MULTICAST_GROUP = '224.1.1.1'
MULTICAST_PORT = 5007
BROADCAST_PORT = 6000


KEY = b'4wsIUHdeEWmzdYtFHwcdwv4RN64_-Kc9rrkqGXuP7zc='
cipher = Fernet(KEY)

username = input("Enter username: ")


# MULTICAST SOCKET (chat)
mcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
mcast_sock.bind(('', MULTICAST_PORT))

group = socket.inet_aton(MULTICAST_GROUP)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)

mcast_sock.setsockopt(socket.IPPROTO_IP,
                      socket.IP_ADD_MEMBERSHIP,
                      mreq)


# BROADCAST SOCKET (server messages)
bcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
bcast_sock.bind(('', BROADCAST_PORT))


# SEND SOCKET (reuse instead of creating every message)
send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



# RECEIVE MULTICAST
def receive_multicast():
    while True:
        try:
            encrypted_data, addr = mcast_sock.recvfrom(4096)

            # Decrypt message
            decrypted = cipher.decrypt(encrypted_data).decode()

            print(f"\n[CHAT]: {decrypted}")

        except Exception:
            break



# RECEIVE BROADCAST
def receive_broadcast():
    while True:
        try:
            data, addr = bcast_sock.recvfrom(1024)
            print(f"\n{data.decode()}")

        except Exception:
            break



# SEND MULTICAST
def send_multicast():
    while True:
        try:
            msg = input()

            if msg.lower() == "/exit":
                leave_notify()
                sys.exit()

            full_msg = f"{username}: {msg}"

            # Encrypt before sending
            encrypted = cipher.encrypt(full_msg.encode())

            send_sock.sendto(
                encrypted,
                (MULTICAST_GROUP, MULTICAST_PORT)
            )

        except KeyboardInterrupt:
            leave_notify()
            sys.exit()



# JOIN NOTIFICATION
def join_notify():
    message = f"[SYSTEM] {username} joined the chat"

    encrypted = cipher.encrypt(message.encode())

    send_sock.sendto(
        encrypted,
        (MULTICAST_GROUP, MULTICAST_PORT)
    )



# LEAVE NOTIFICATION
def leave_notify():
    message = f"[SYSTEM] {username} left the chat"

    encrypted = cipher.encrypt(message.encode())

    send_sock.sendto(
        encrypted,
        (MULTICAST_GROUP, MULTICAST_PORT)
    )



# MAIN
join_notify()

threading.Thread(
    target=receive_multicast,
    daemon=True
).start()

threading.Thread(
    target=receive_broadcast,
    daemon=True
).start()

try:
    send_multicast()

except KeyboardInterrupt:
    leave_notify()
    print("\nLeaving chat...")