import socket
from _thread import *
from time import sleep

rasp_pi = False
if rasp_pi:
	# Set up pins
	from machine import Pin
	onboard_led = Pin("LED", Pin.OUT)
	external_led = Pin(1, Pin.OUT)

# Get host and ip
import network
from secrets import secrets
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ssid = secrets['ssid']
pw = secrets['pw']

wlan.connect(ssid, pw)

# Wait for connection with 10 second timeout
timeout = 10
while timeout > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    timeout -= 1
    print('Waiting for connection...')
    time.sleep(1)
    

wlan_status = wlan.status()

if wlan_status != 3:
    raise RuntimeError('Wi-Fi connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])
    

# Declare host and port
host = status[0]
port = 8080

# How to interact with client
def client_handler(connection):
    connection.send(str.encode('You are now connected to the replay server...'))
    connected = True
    while connected:
        data = connection.recv(2048)
        message = data.decode('utf-8')
        reply = f'Message recieved: {message}'

        if message == 'P1-hit' and rasp_pi:
            onboard_led.on()
            print("Player 1 hit")
            sleep(2)
            onboard_led.off()

        if message == 'P2-hit' and rasp_pi:
            external_led.on()
            print("Player 2 hit")
            sleep(2)
            external_led.off()

        if message == "All" and rasp_pi:
        	onboard_led.on()
        	external_led.on()
        	sleep(2)
        	onboard_led.off()
        	external_led.off()

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
    print(f'host = {host}')
    ServerSocket.listen()

    while True:
        accept_connections(ServerSocket)

start_server(host, port)


