import time
import socket
import random


#error probability
P_ERROR = 0.3
#prop delay
PROP_D = 2
#timeout
TIMEOUT = 5

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

def rdt_receive():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((UDP_IP, UDP_PORT))

    expected_seq_num = 0

    while expected_seq_num < 8:  # Total 8 packets (A-H)
        data, addr = sock.recvfrom(1024)
        packet = data.decode()
        actual_seq_num = ord(packet) - ord('A')  # Deduce sequence number

        if actual_seq_num == expected_seq_num:
            print(f"Received packet: {packet} with expected sequence number")
            expected_seq_num += 1
        else:
            print(f"Received packet: {packet} with unexpected sequence number")

        # Send ACK
        if random.random() > P_ERROR:
            ack = f"ACK{actual_seq_num}"
            sock.sendto(ack.encode(), addr)
            print(f"ACK sent for packet: {packet}")
        else:
            print("ACK lost")

    sock.close()

if __name__ == "__main__":
    rdt_receive()
