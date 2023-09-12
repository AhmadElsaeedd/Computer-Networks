#importing libraries
import socket

print("Done")

#instantiating a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Done 2")

#bind the socket to a specific address and port
sock.bind(('localhost',12345))

print("Done 3")

#listen for incoming connections
sock.listen(1)

print("Done 4")

#accept a connection from a client
#2 objects are instantiated when a connection is established
conn, addr = sock.accept()
print(f"Got connection from {addr}")

#flag for when to exit the connection
keep_going = True

#buffer to store incoming characters from telnet
#telnet sends character by character
buffer = ""

while keep_going:
    #start receiving data from the client
    data = conn.recv(1024).decode('utf-8')
    print(f"Received data: {data}")

    buffer += data

    #check for a newline in the data
    #this is a way to mark that this is the end of an expression
    if '\n' in buffer:
        expression = buffer.split('\n')[0].strip()

        #clear the buffer for the next expression
        buffer = ""

        #check for the termination condition
        if expression == '1 / 0':
            print("Okay bye. I'm leaving")
            conn.close()
            break

        #parse the received data in a try except block
        try:
            print("Expression is:", expression)
            operand1, operator, operand2 = expression.split(' ')
            operand1 = float(operand1)
            operand2 = float(operand2)
        except ValueError:
            conn.send(b"Invalid expression\n")
            continue

        #perform the calculation
        if operator == '+':
            result = operand1 + operand2
        elif operator == '-':
            result = operand1 - operand2
        elif operator == '*':
            result = operand1 * operand2
        elif operator == '/':
            if operand2 == 0:
                conn.send(b"Cannot divide by zero\n")
                continue
            result = operand1 / operand2
        elif operator == '^':
            result = operand1 ** operand2
        elif operator == '%':
            result = operand1 % operand2
        else:
            conn.send(b"Invalid operator\n")
            continue

        #send the result back to the client
        response = f"{expression} = {result}\n"
        conn.send(response.encode())