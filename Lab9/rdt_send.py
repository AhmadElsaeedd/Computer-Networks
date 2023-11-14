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

def send_packet(sock, packet, addr):
    if random.random() > P_ERROR:
        sock.sendto(packet.encode(), addr)
        print(f"Packet sent: {packet}")
    else:
        print("Packet lost during sending")

def rdt_send():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)
    addr = (UDP_IP, UDP_PORT)

    # Sequence number mapping A=0, B=1, ..., H=7
    packets = "ABCDEFGH"
    seq_num = 0

    while seq_num < len(packets):
        packet = packets[seq_num]
        send_packet(sock, packet, addr)

        try:
            ack, _ = sock.recvfrom(1024)
            ack = ack.decode()
            if ack == f"ACK{seq_num}":
                print(f"ACK received for packet {packet}")
                seq_num += 1  # Move to next packet
            else:
                print(f"Incorrect ACK received: {ack}")
        except socket.timeout:
            print("Timeout occurred, resending packet")

    sock.close()

if __name__ == "__main__":
    rdt_send()