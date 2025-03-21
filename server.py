import socket
import ssl
import threading
import os
import RPi.GPIO as GPIO

# Setup GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)
LED_PIN = 17
GPIO.setup(LED_PIN, GPIO.OUT)

CERTS_DIR = "certs"
SERVER_CERT = "server.crt"
SERVER_KEY = "server.key"

def handle_client(secure_socket, client_address):
    print(f"Accepted connection from {client_address}")
    try:
        while True:
            data = secure_socket.recv(1024)
            if not data:
                break
            command = data.decode().strip().lower()
            print(f"Received command: {command}")
            if command == "led on":
                GPIO.output(LED_PIN, GPIO.HIGH)
                secure_socket.sendall(b"LED turned ON")
            elif command == "led off":
                GPIO.output(LED_PIN, GPIO.LOW)
                secure_socket.sendall(b"LED turned OFF")
            elif command == "exit":
                secure_socket.sendall(b"Closing connection")
                break
            else:
                secure_socket.sendall(b"Unknown command")
    except Exception as e:
        print("Error in client thread:", e)
    finally:
        secure_socket.close()
        print(f"Closed connection with {client_address}")

def start_server(server_host='0.0.0.0', server_port=8443):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=os.path.join(CERTS_DIR, SERVER_CERT),
                            keyfile=os.path.join(CERTS_DIR, SERVER_KEY))
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen(5)
    print(f"Server listening on {server_host}:{server_port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            secure_socket = context.wrap_socket(client_socket, server_side=True)
            client_thread = threading.Thread(target=handle_client, args=(secure_socket, client_address))
            client_thread.daemon = True
            client_thread.start()
    except ssl.SSLError as e:
        print(f"SSL error: {e}")
    except socket.error as e:
        print(f"Socket error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        server_socket.close()
        GPIO.cleanup()

if __name__ == "__main__":
    start_server()