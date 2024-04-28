import socket
import threading
import ssl
import logging

PORT = 53
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
TARGET = "1.1.1.1"

LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.DEBUG,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
)

# Receives the request from the client and sends it over to the DNS Resolver
# Gets the response from the DNS Resolver
def handle_request(msg, *args):
    if msg:
        context = ssl.create_default_context()

        targetSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        tlsTargetSocket = context.wrap_socket(targetSocket, server_hostname=TARGET)
        tlsTargetSocket.connect((TARGET, 853))
        tlsTargetSocket.sendall(msg) # Sends the request to the DNS resolver

        resp = tlsTargetSocket.recv(1024)

        threading.current_thread().resp = resp # Gets the response from DNS resolver and adds it to the thread - Dynamic property

# Creates the listening socket to accept DNS queries from clients
# Also sets the threading configuration
def tcp():
    tcpServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpServerSocket.bind(ADDR)
    tcpServerSocket.listen()
    logging.info(f"[LISTENING] Server is listening on {SERVER} tcp/{PORT}")

    listening = True
    while listening:
        conn, addr = tcpServerSocket.accept()
        logging.info(f"[NEW TCP CONNECTION] {addr} connected.")

        msg = conn.recv(1024)

        thread = threading.Thread(target=handle_request, args=(msg, ))
        thread.start()
        thread.join()

        conn.sendall(thread.resp) # Sends the response back to client
        conn.close()

def udp():
    udpServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpServerSocket.bind(ADDR)
    logging.info(f"[LISTENING] Server is listening on {SERVER} udp/{PORT}")

    listening = True
    while listening:
        msg, addr = udpServerSocket.recvfrom(1024)
        logging.info(f"[NEW UDP CONNECTION] {addr} connected.")
        logging.info(f"[UDP MESSAGE IN]: {msg}")

        thread = threading.Thread(target=handle_request, args=(msg, ))
        thread.start()
        thread.join()

        logging.info(f"[UDP MESSAGE OUT]: {thread.resp}")

        udpServerSocket.sendto(thread.resp, addr)

def start():
    tcpThread = threading.Thread(target=tcp)
    tcpThread.start()

    udpThread = threading.Thread(target=udp)
    udpThread.start()

logging.info("[STARTING] Server is starting...")
start()
