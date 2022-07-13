import socket
from _thread import *
#from machine import Pin
from time import sleep

# Set up pins
#onboard_led = Pin("LED", Pin.OUT)

# Declare host and port
host = '127.0.0.1'
port = 8080

# How to interact with client
def client_handler(connection):
    connection.send(str.encode('You are now connected to the replay server...'))
    connected = True
    while connected:
        data = connection.recv(2048)
        message = data.decode('utf-8')
        reply = f'Message recieved: {message}'

        if message == 'P1-hit':
            #onboard_led.on()
            print("Player 1 hit")
            sleep(10)
        if message == 'P2-hit':
            #onboard_led.on()
            print("Player 2 hit")
            sleep(10)
        if message == 'BYE':
            connected = False

        #print(f'Client: {message}')
        connection.sendall(str.encode(reply))
    connection.close()

# Open new thread for each client
def accept_connections(ServerSocket):
    Client, address = ServerSocket.accept()
    print(f'Connected to: {address[0]}:{str(address[1])}')
    start_new_thread(client_handler, (Client, ))

# Run server forever
def start_server(host, port):
    ServerSocket = socket.socket()
    try:
        ServerSocket.bind((host, port))
    except socket.error as e:
        print(str(e))
    print(f'Server is listing on the port {port}...')
    ServerSocket.listen()

    while True:
        accept_connections(ServerSocket)

start_server(host, port)


