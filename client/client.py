import socket
import ssl
import os

CERTS_DIR = "../certs"

def echo_client(server_host='127.0.0.1', server_port=8443, certfile='server.crt'):
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations(os.path.join(CERTS_DIR, certfile))
    context.check_hostname = False
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        secure_socket = context.wrap_socket(client_socket, server_hostname=server_host)
        secure_socket.connect((server_host, server_port))
        print("Connected to server with SSL")
        try:
            while True:
                message = input("Enter message (or type 'exit' to quit): ")
                if message.lower() == 'exit':
                    print("Exiting")
                    break
                secure_socket.sendall(message.encode())
                data = secure_socket.recv(1024)
                print(f"Received from server: {data.decode()}")
        except Exception as e:
            print("Error:", e)
        finally:
            secure_socket.close()
            print("Closing connection.")

if __name__ == "__main__":
    echo_client()