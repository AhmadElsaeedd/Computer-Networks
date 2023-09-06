#ToDo: import packages
import dpkt
import os

#ToDo: read the pcap file from the same folder of the python file
with open(os.path.join(os.path.dirname(__file__), 'Lab2.pcapng'), 'rb') as f:
    pcap = dpkt.pcap.Reader(f)

#ToDo: start parsing through it
for timestamp, buf in pcap:
    eth = dpkt.ethernet.Ethernet(buf)

    print("Ethernet frame type:", eth.type)

    if eth.type == dpkt.ethernet.ETH_TYPE_IP:
        ip = eth.data

        print(f"Source IP: {ip.src}, Destination IP: {ip.dst}")