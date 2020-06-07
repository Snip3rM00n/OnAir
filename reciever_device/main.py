try:
    import usocket as socket
except:
    import socket

import machine  # Built into MicroPython
from machine import Pin

RED_PIN = Pin(5, Pin.OUT)   # On Air!
GREEN_PIN = Pin(4, Pin.OUT) # Off Air!
ACCEPTABLE_IPS = ["192.168.0.110"]  # Update this with the Switcher's IP Address

def get_socket():
    listen_socket = socket.socket()
    port = 8080
    addr_info = socket.getaddrinfo("0.0.0.0", port)
    addr = addr_info[0][-1]

    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(addr)
    listen_socket.listen(5)

    print("Listening on: {}:{}".format(addr, port))
    return listen_socket

def on_air():
    RED_PIN.value(1)
    GREEN_PIN.value(0)
    print("ON AIR!")

def off_air():
    RED_PIN.value(0)
    GREEN_PIN.value(1)
    print("OFF AIR!")

def handle_requests(listen_socket):
    handles = {"on_air": on_air, "off_air": off_air}

    while True:
        resp = listen_socket.accept()
        client = resp[0]
        client_addr = resp[1]
        req = client.recv(1024)
        print(client_addr[0])

        if str(client_addr[0]) in ACCEPTABLE_IPS:
            try:
                path = req.decode().split("\r\n")[0].split(" ")[1]
                path = path.replace('/', '')
                handles[path]()
                response = b"HTTP/1.0 200 OK\r\n"
            except:
                response = b"HTTP/1.0 400 BAD REQUEST\r\n"
        else:
            response = b"HTTP/1.0 401 UNAUTHORIZED\r\n"
        
        print(response)
        client.send(response)
        client.close()

def main():
    print("THIS IS THE RECEIVER DEVICE!")
    RED_PIN.value(1)
    GREEN_PIN.value(1)
    listener = get_socket()
    handle_requests(listener)

if __name__ == "__main__":
    main()
