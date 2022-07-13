import socket
host = '192.168.1.219'
port = 8080

# Connect to server
ClientSocket = socket.socket()
print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except:
    print("error with socket")

# Communicate with socket
Response = ClientSocket.recv(2048)

while True:
    message = input('Your message: ')
    ClientSocket.send(str.encode(message))
    reply = ClientSocket.recv(2048)
    decoded_reply = reply.decode('utf-8')
    print(decoded_reply)
    if decoded_reply == 'BYE':
      break

# Close socket, will probably be removed in the future
ClientSocket.close()
