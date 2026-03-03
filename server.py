# Made by https://github.com/PinkMath/Chat
import socket
import threading
from datetime import datetime

HOST = '0.0.0.0'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
usernames = {}

def timestamp():
    return datetime.now().strftime("%H:%M")

def broadcast(message, sender=None):
    """Send message to all clients except sender."""
    for client in clients[:]:
        if client != sender:
            try:
                client.send(message)
            except:
                remove_client(client)

def remove_client(client):
    username = usernames.get(client, "Unknown")
    if client in clients:
        clients.remove(client)
    if client in usernames:
        del usernames[client]
    client.close()
    print(f"[{timestamp()}] {username} disconnected")

def handle_client(client):
    username = usernames[client]
    while True:
        try:
            message = client.recv(4096).decode().strip()
            if not message:
                continue  # ignore empty messages
            if message == "/exit":
                # client handles leaving; do not broadcast
                remove_client(client)
                break
            # Broadcast message to others
            full_message = f"{username}: {message}"
            broadcast(full_message.encode(), sender=client)
        except:
            remove_client(client)
            break

def receive_connections():
    print(f"[{timestamp()}] Server running on port {PORT}...")
    while True:
        client, address = server.accept()
        client.send("USERNAME".encode())
        username = client.recv(1024).decode().strip()

        clients.append(client)
        usernames[client] = username

        print(f"[{timestamp()}] {username} joined from ---")
        broadcast(f"{username} joined the chat!".encode(), sender=None)

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive_connections()

# to get the ip
# --- windows
# 1. open cmd
# 2. run "ipconfig"
# 3. look for "IPv4 Address . . . . . . . . . . : 192.168.x.x"
# That 192.168.x.x (or sometimes 10.x.x.x) is your IP.

# --- macOS
# 1. open cmd
# 2. run "ifconfig" or "ipconfig getifaddr en0"
# 3. Look under en0 (Wi-Fi) for: "inet 192.168.x.x".

# --- Linux
# 1. open terminal
# 2. run "ip a | grep inet"
# 3. Look for "inet 192.168.x.x"

# === and give the IP to the who you want to join ===
# Made by https://github.com/PinkMath/Chat
