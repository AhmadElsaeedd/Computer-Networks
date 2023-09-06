# import libaries (used pyshark instead of dpkm) (used Counter for easy frequency counting)
import pyshark
from collections import Counter

# read the pcapng file
cap = pyshark.FileCapture('Lab2.pcapng')

# reading done
print("Done")

# initialize the MAC addresses table
destination_MAC_addresses = Counter()
print("Initialized first table")
# initialize the IP classification table
IP_classification = Counter()
print("Initialized second table")
# initialize the transport protocol table
Transport_protocols = Counter()
print("Initialized third table")
# initialize the layer4 and layer5 tables
layers45_frequency = Counter()
print("Initialized fourth table")
# initialize the application layer tables
application_layer = Counter()
print("Initialized fifth table")

# start parsing data and generate table for MAC addresses
for packet in cap:
    # check that the packet is an IP layer packet
    if 'IP' in packet:
        # check that the packet comes from my computer
        if packet.ip.src == '10.225.26.197':
            # getting the count of packets sent to a destination MAC address
            destination_MAC_addresses[packet.eth.dst] += 1

            # classifying the types of IP addresses encountered
            ip_key = f"{'private' if packet.ip.dst.startswith(('192.168.', '10.', '172.')) else 'public'}-{packet.ip.dst}"
            IP_classification[ip_key] += 1

            # getting the transport protocol used
            if 'TCP' in packet:
                Transport_protocols['TCP'] += 1
            elif 'UDP' in packet:
                Transport_protocols['UDP'] += 1
            # 6 is for TCP and 17 is for UDP
            elif hasattr(packet.ip, 'p') and packet.ip.p not in (6, 17):
                Transport_protocols['Other'] += 1
            else:
                Transport_protocols['None'] += 1

            # getting the layer 4 and 5 counts according to the conditions in the lab manual
            if 'TCP' in packet or 'UDP' in packet:
                #get the length of the payload
                transport_protocol = 'TCP' if 'TCP' in packet else 'UDP'
                if transport_protocol == 'TCP':
                    # depending on the payload length, decide whether its layer 4 or 5
                    if int(packet.tcp.len) > 0:
                        layers45_frequency['Layer 5'] += 1
                    else:
                        layers45_frequency['Layer 4'] += 1
                elif transport_protocol == 'UDP':
                    # UPD header is 8 bytes, anything more than that is payload
                    if int(packet.udp.length) > 8:
                        layers45_frequency['Layer 5'] += 1
                    else:
                        layers45_frequency['Layer 4'] += 1

            # get which application layer protocol is used
            if 'HTTP' in packet:
                application_layer['HTTP'] += 1
            elif 'TLS' in packet or 'SSL' in packet:
                application_layer['TLS/SSL'] += 1
            elif 'DNS' in packet:
                application_layer['DNS'] += 1
            else:
                application_layer['Other'] += 1

# print the frequency table of destination MAC addresses
print(f"Destination MAC Frequency Table: {destination_MAC_addresses}")
# awesome
# print the frequency table of the private/public IP addresses
print(f"IP classification Frequency Table: {IP_classification}")
# print the frequency table of the transport protocols used
print(f"Transport protocols Frequency Table: {Transport_protocols}")
# print the frequency table of layer 4 or layer 5
print(f"Layer 4 or 5 protocols Frequency Table: {layers45_frequency}")
# print the frequency table of each application layer protocol
print(f"Application layer protocols Frequency Table: {application_layer}")