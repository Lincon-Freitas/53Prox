import socket
import threading
import ssl
import logging
import json

PORT = 53
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

# Function to load configurations
def load_config():
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    return config

config = load_config()

# Configure logging
logging.basicConfig(
    level=config["logging"]["level"],
    format=config["logging"]["format"],
    datefmt=config["logging"]["datefmt"],
)

# Receives the request message and sends it over to the DNS Resolver
# Gets the response from the DNS Resolver
def handle_request(msg, *args):
    if msg:
        try:
          context = ssl.create_default_context()

          targetSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

          tlsTargetSocket = context.wrap_socket(targetSocket, server_hostname=config["target"])
          tlsTargetSocket.connect((config["target"], 853))
          tlsTargetSocket.sendall(msg) # Sends the request to the DNS resolver

          resp = tlsTargetSocket.recv(1024)

          threading.current_thread().resp = resp # Gets the response from DNS resolver and adds it to the thread - Dynamic property

        except Exception as e:
            logging.error(str(e))

def tcp():
    tcpServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpServerSocket.bind(ADDR)
    tcpServerSocket.listen()
    logging.info(f"[LISTENING] Server is listening on {SERVER} tcp/{PORT}")

    listening = True
    while listening:
        try:
          conn, addr = tcpServerSocket.accept()
          logging.info(f"[NEW TCP CONNECTION] {addr} connected.") # Displays TCP interaction

          msg = conn.recv(1024)

          thread = threading.Thread(target=handle_request, args=(msg, ))
          thread.start()
          thread.join()

          conn.sendall(thread.resp) # Sends the response back to client
          conn.close()

        except Exception as e:
            logging.error(str(e))

def udp():
    udpServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpServerSocket.bind(ADDR)
    logging.info(f"[LISTENING] Server is listening on {SERVER} udp/{PORT}")

    receiving = True
    while receiving:
        try:
          msg, addr = udpServerSocket.recvfrom(1024)
          logging.info(f"[NEW UDP CONNECTION] {addr} connected.") # Displays UDP interaction

          msg = (len(msg)).to_bytes(2, byteorder='big') + msg # Append the header size to convert it to a TCP-like request

          thread = threading.Thread(target=handle_request, args=(msg, ))
          thread.start()
          thread.join()

          udpServerSocket.sendto(thread.resp[2:], addr) # Slice the answer to remove the extra transaction ID

        except Exception as e:
            logging.error(str(e))

# Initiate each protocol function as a thread
def start():
    tcpThread = threading.Thread(target=tcp)
    tcpThread.start()

    udpThread = threading.Thread(target=udp)
    udpThread.start()

logging.info("[STARTING] Server is starting...")
start()
