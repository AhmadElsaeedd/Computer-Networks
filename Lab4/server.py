import socket

print("Done")

# HTML data for the web pages
home_page = """<!DOCTYPE html>
<HTML><HEAD><TITLE>HTTP Homework</TITLE></HEAD><BODY><H3><CENTER>HTTP Homework</CENTER></H3>This is the main page<P>You can click on <A HREF="/page2">page 2</A> or <A HREF="/page3">or Page 3</A><P><CENTER>This server has been used N times</CENTER></BODY></HTML>"""

page1 = """<!DOCTYPE html>
<HTML><HEAD><TITLE>HTTP Homework</TITLE></HEAD><BODY><H3><CENTER>HTTP Homework</CENTER></H3>This is page2<P>You can go <A HREF="/">back</A> <P><CENTER>This server has been used N times</CENTER></BODY></HTML>"""

page2 = """<!DOCTYPE html>
<HTML><HEAD><TITLE>HTTP Homework</TITLE></HEAD><BODY><H3><CENTER>HTTP Homework</CENTER></H3>This is page3<P>You can go <A HREF="/">back</A> <P><CENTER>This server has been used N times</CENTER></BODY></HTML>"""

#counter for get requests
counter = 0

print("Done initializations")

#instantiating a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Done 2")

#bind the socket to a specific address and port
sock.bind(('localhost',8080))

print("Done 3")

#listen for incoming connections
sock.listen(1)

while True:
    #accept a connection from a client
    #2 objects are instantiated when a connection is established
    conn, addr = sock.accept()
    print(f"Got connection from {addr}")

    request = conn.recv(1024).decode('utf-8')
    print("Received request:", request)

    counter += 1

     # Parse the request
    lines = request.split('\n')
    if lines:
        request_line = lines[0]
        method, path, _ = request_line.split(' ')

        # Prepare the HTTP response
        if method == 'GET':
            if path == '/':
                response_body = home_page.replace("N", str(counter)) # this statement is not working properly
            elif path == '/page2':  # Make sure the path matches what's in your HTML
                response_body = page1.replace("N", str(counter)) # this statement is not working properly
            elif path == '/page3':  # Make sure the path matches what's in your HTML
                response_body = page2.replace("N", str(counter)) # this statement is not working properly
            else:
                response_body = '<h1>404 Not Found</h1>'
                header = 'HTTP/1.0 404 Not Found\n'
                header += f'Server: ae2200\n'
                header += f'Content-Length: {len(response_body)}\n'
                header += 'Content-Type: text/html\n'
                header += 'Connection: Closed\n\n'
                conn.sendall((header + response_body).encode())
                conn.close()
                continue

            # Create HTTP headers
            header = 'HTTP/1.0 200 OK\n'
            header += f'Server: ae2200\n'
            header += f'Content-Length: {len(response_body)}\n'
            header += 'Content-Type: text/html\n'
            header += 'Connection: Closed\n\n'

            # Send the HTTP response
            conn.sendall((header + response_body).encode())

    conn.close()
