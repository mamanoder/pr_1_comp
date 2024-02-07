import socket
import threading
import pickle
import queue
import checking_if_port_sus
from checking_network import handle_packet_summary
from open_server import *


def return_command(Type, port):
    answear = checking_if_port_sus.check_port_sus(port)
    data = {"type": Type, "number": port, "answar": answear}
    print(data)
    try:
        client_socket.send(pickle.dumps(data))
    except Exception as e:
        print(f"Error sending data to client: {e}")
        # Optionally, you may want to close the client socket or take other appropriate actions





def handle_client(client_socket, address):
    ports = queue.Queue()
    while True:
        try:
            data = client_socket.recv(3000)
            if not data:
                break

            # Assuming the data is received in chunks, keep collecting until a complete object is received
            complete_data = b""
            while True:
                complete_data += data
                try:
                    # Try to unpickle the data
                    decoded_data = pickle.loads(complete_data)
                    break  # Break the inner loop if successful
                except pickle.UnpicklingError:
                    # If not successful, continue receiving data
                    data = client_socket.recv(3000)
                    if not data:
                        break  # Break the inner loop if no more data is received

            if not decoded_data:
                break  # Break the outer loop if no more data is received

            # Handle the decoded data as needed
            if decoded_data["type"] == "message":
                message = decoded_data["content"]
                print(f"[{address}] Message: {message}")
                data = {"type": "answear", "answear": "answear"}
                # print(data)
                client_socket.send(pickle.dumps(data))

            elif decoded_data["type"] == "check":
                print(decoded_data)
                print("sended")
                traffic = decoded_data["content"]
                print(traffic)
                check_trafic = threading.Thread(target=handle_packet_summary, args=(traffic,))
                check_trafic.run()


            elif decoded_data["type"] == "port" or decoded_data["type"] == "port+":
                # Handle port-related data
                port = decoded_data["number"]
                ports.put(port)

                print(f"Port: {port} is open")
                # answer = input("True or False?").encode()
                sug = "port"
                check_ports = threading.Thread(target=return_command, args=(sug, port))
                check_ports.run()
                print("success")


        except Exception as e:
            print(f"Error handling client {address}: {e}")
            break


    print(f"[*] Client {address} disconnected")
    client_sockets.remove(client_socket)
    client_socket.close()

while True:
    client_socket, address = server.accept()
    print(f"[*] Connected to {address}")
    client_sockets.add(client_socket)
    threading.Thread(target=handle_client, args=(client_socket, address)).start()
