import socket
import struct
import time
import random

#this is already known
dns_server = "8.8.8.8"
dns_port = 53

#function that initializes the client using UDP
def initialize_client():
    return socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

#function that structures the message
def construct_message(domain):
    #construct the header of the message
    identifier = random.randint(0,65535)
    id_bytes = identifier.to_bytes(2,'big')
    #header: identifier, flags, qdcount, ancount, nscount, arcount
    header = struct.pack(">2s2sHHHH",id_bytes, b'\x01\x00', 1, 0, 0, 0)

    #construct the question: qname, qtype, qclass
    qname = b''.join([bytes([len(part)]) + part.encode() for part in domain.split('.')]) + b'\x00'
    qtype = struct.pack(">H", 1)  # Type A
    qclass = struct.pack(">H", 1)  # Class IN (Internet)

    return header + qname + qtype + qclass

#function to resolve the domain name and returns it to the client socket
def resolve_domain(domain, client_socket):
    message = construct_message(domain)
    
    #send the message
    client_socket.sendto(message, (dns_server,dns_port))

    #receive the message
    data,address = client_socket.recvfrom(512)

    #skip the header of the request
    offset = 12
    offset = data.index(b'\x00',offset) + 5

    #find the ttl and the ip address
    ttl = struct.unpack(">I", data[offset+6:offset+10])[0]
    formated_ttl = format_ttl(ttl)
    ip_address = socket.inet_ntoa(data[offset+12:offset+16])

    #get the response code to see if there is an error
    _, flags, _, _, _, _ = struct.unpack(">H2sHHHH", data[:12])
    rcode = flags[1] & 0x0F

    #check what the rcode is and what that means according to the RFC
    if rcode != 0:
        error_messages = {
            1: "Format error: The name server was unable to interpret the query.",
            2: "Server failure: The name server was unable to process this query due to a problem with the name server.",
            3: "Name Error: The domain name does not exist.",
            4: "Not Implemented: The name server does not support the requested kind of query.",
            5: "Refused: The name server refuses to perform the specified operation for policy reasons."
        }
        print(f"Error {rcode} occurred: {error_messages.get(rcode, 'Unknown error')}")
        return None, None    

    return ip_address, formated_ttl



#function to format the TTL
def format_ttl(ttl):
    mins, sec = divmod(ttl, 60)
    hour, mins = divmod(mins, 60)
    day, hour = divmod(hour, 24)
    return "{:02d}:{:02d}:{:02d}:{:02d}".format(day, hour, mins, sec)

#ask user for input of domain
requested_domain = input("Enter a domain name: ")
client_socket = initialize_client()
ip_address, formatted_ttl = resolve_domain(requested_domain, client_socket)
print("The ip address is: ", ip_address)
print("The ttl is: ", formatted_ttl)
