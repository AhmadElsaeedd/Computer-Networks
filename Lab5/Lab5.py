"""
Comparison between SMTP and ESMTP:

SMTP (Simple Mail Transfer Protocol):
- Traditional protocol for sending emails on the Internet.
- Lacks built-in mechanisms for secure transmission of data.
- Does not support modern email features and enhancements natively.
- Uses standard port 25 for unencrypted transmission.
- Emails need to be ASCII encoded due to inability to handle binary data natively.

ESMTP (Extended Simple Mail Transfer Protocol):
- An extension of SMTP with added features and capabilities.
- Can negotiate encryption using STARTTLS for secure email transmission.
- Allows for protocol extensions without altering the core protocol (e.g., authentication, enhanced status codes).
- Uses standard port 465 for encrypted transmission using SSL.
- During an ESMTP session, the server indicates its supported extensions.

"""

import ssl
import socket
import base64

def send_email_ESMTP(sender_email, recipient_email, app_password, body):
    mailserver = 'smtp.gmail.com'
    mailPort = 465
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
            clientSocket.connect((mailserver, mailPort))
            
            context = ssl.create_default_context()
            sslClientSocket = context.wrap_socket(clientSocket, server_hostname='smtp.gmail.com')
            
            ehloCommand = 'EHLO Alice\r\n'
            sslClientSocket.send(ehloCommand.encode())
            recv = sslClientSocket.recv(1024).decode()
            print(recv)
            

            # Authenticate using app password
            authCommand = 'AUTH LOGIN\r\n'
            sslClientSocket.send(authCommand.encode())
            recv = sslClientSocket.recv(1024).decode()
            print(recv)

            sslClientSocket.send(base64.b64encode(sender_email.encode()) + b'\r\n')
            recv = sslClientSocket.recv(1024).decode()
            print(recv)

            sslClientSocket.send(base64.b64encode(app_password.encode()) + b'\r\n')
            recv = sslClientSocket.recv(1024).decode()
            print(recv)

            # Set MAIL FROM, RCPT TO, and DATA commands
            # Set MAIL FROM
            mail_from_command = f"MAIL FROM:<{sender_email}>\r\n"
            sslClientSocket.send(mail_from_command.encode())
            recv = sslClientSocket.recv(1024).decode()
            print(recv)

            # Set RCPT TO
            rcpt_to_command = f"RCPT TO:<{recipient_email}>\r\n"
            sslClientSocket.send(rcpt_to_command.encode())
            recv = sslClientSocket.recv(1024).decode()
            print(recv)

            # Send DATA command to signal start of email content
            data_command = "DATA\r\n"
            sslClientSocket.send(data_command.encode())
            recv = sslClientSocket.recv(1024).decode()
            print(recv)

            # Send email body
            # Ensure lines starting with . are prefixed with another . and handle lone dots
            modified_body = "\r\n".join(["." + line if line.startswith(".") or line == "." else line for line in email_body.split("\n")])
            sslClientSocket.send((modified_body + "\r\n.\r\n").encode()) # The . on a new line signifies end of message

            recv = sslClientSocket.recv(1024).decode()
            print(recv)

            # Optionally, you could send a QUIT command to gracefully close the session
            quit_command = "QUIT\r\n"
            sslClientSocket.send(quit_command.encode())
            recv = sslClientSocket.recv(1024).decode()
            print(recv)
            
    except socket.error as e:
        print("Socket error:", e)
    except ssl.SSLError as e:
        print("SSL error:", e)
    except Exception as e:
        print("Unexpected error:", e)


sender = "ahmednetworks8@gmail.com"
recipient = "ae2200@nyu.edu"
app_pass = "dgmawbikvcnaakxl"

# Read the email body from the file
with open('emailBody.txt', 'r') as file:
    email_body = file.read()

send_email_ESMTP(sender, recipient, app_pass, email_body)


import socket
import base64

def send_email_SMTP(sender_email, recipient_email, password, body):
    mailserver = 'smtp.gmail.com'  # Example SMTP server, change as needed
    mailPort = 25  # Standard SMTP port
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
            clientSocket.connect((mailserver, mailPort))
            recv = clientSocket.recv(1024).decode()
            print(recv)

            # Send EHLO command
            ehloCommand = f'EHLO {mailserver}\r\n'
            clientSocket.send(ehloCommand.encode())
            recv = clientSocket.recv(1024).decode()
            print(recv)

            # Authenticate
            authCommand = 'AUTH LOGIN\r\n'
            clientSocket.send(authCommand.encode())
            recv = clientSocket.recv(1024).decode()
            print(recv)

            clientSocket.send(base64.b64encode(sender_email.encode()) + b'\r\n')
            recv = clientSocket.recv(1024).decode()
            print(recv)

            clientSocket.send(base64.b64encode(password.encode()) + b'\r\n')
            recv = clientSocket.recv(1024).decode()
            print(recv)

            # Send MAIL FROM, RCPT TO, and DATA commands
            mail_from_command = f"MAIL FROM:<{sender_email}>\r\n"
            clientSocket.send(mail_from_command.encode())
            recv = clientSocket.recv(1024).decode()
            print(recv)

            rcpt_to_command = f"RCPT TO:<{recipient_email}>\r\n"
            clientSocket.send(rcpt_to_command.encode())
            recv = clientSocket.recv(1024).decode()
            print(recv)

            data_command = "DATA\r\n"
            clientSocket.send(data_command.encode())
            recv = clientSocket.recv(1024).decode()
            print(recv)

            # Send email body
            modified_body = "\r\n".join(["." + line if line.startswith(".") else line for line in body.split("\n")])
            clientSocket.send((modified_body + "\r\n.\r\n").encode())

            recv = clientSocket.recv(1024).decode()
            print(recv)

            quit_command = "QUIT\r\n"
            clientSocket.send(quit_command.encode())
            recv = clientSocket.recv(1024).decode()
            print(recv)

    except socket.error as e:
        print("Socket error:", e)
    except Exception as e:
        print("Unexpected error:", e)


sender = "ahmednetworks8@gmail.com"
recipient = "ae2200@nyu.edu"
password = "dgmawbikvcnaakxl"

with open('emailBody.txt', 'r') as file:
    body = file.read()

send_email_SMTP(sender, recipient, password, body)

