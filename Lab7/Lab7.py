import socket
import threading

users = {
    "ahmed" : ("127.0.0.1", 5002),
    "ahmed2" : ("127.0.0.1", 5003)
}

username = input("enter ur username: ")

localhost = '127.0.0.1'
port_2 = users[username][1]

def send_message():
    while True:
        message = input()
        # Split the message to get the receiver's username
        target_username, actual_message = message.split(">", 1)
        if target_username in users:
            target_ip, target_port = users[target_username]
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((target_ip, target_port))
                formatted_message = f"{username}>{actual_message}"
                s.sendall(formatted_message.encode('utf-8'))
        else:
            print(f"User {target_username} not found!")

def handle_client(conn):
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(data.decode('utf-8'))

def receive_message():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as receive_socket:
        receive_socket.bind((localhost, port_2))
        receive_socket.listen()
        while True:
            conn, addr = receive_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn,))
            client_thread.start()

if __name__ == "__main__":
    try:
        # Start the receiving thread
        receive_thread = threading.Thread(target=receive_message)
        receive_thread.start()

        # Start the sending thread
        send_thread = threading.Thread(target=send_message)
        send_thread.start()
    except KeyboardInterrupt:
        print("closing application")
