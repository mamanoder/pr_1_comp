import socket
import threading
try:
    # Get the local hostname
    hostname = socket.gethostname()

    # Get the IP address associated with the hostname
    ip_address = socket.gethostbyname(hostname)
    IP = ip_address
    print(IP)

except Exception as e:
    print(f"An error occurred: {e}")


PORT = 8888
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))

server.listen()
print(f"[*] Listening on {IP}:{PORT}")

client_sockets = set()
