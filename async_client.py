# Made byhhttps://github.com/PinkMath/Chat
import socket
import threading
import json
import os
import base64
import zipfile
import random
from pathlib import Path

# Clear terminal on start
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

clear_screen()

# Enable Windows colors
try:
    from colorama import init
    init()
except:
    pass

HOST = input("Server IP: ")
PORT = 5000
USERNAME = input("Username: ")

last_file_data = None
last_file_name = None
current_room = None

COLORS = [
    "\033[96m",
    "\033[92m",
    "\033[95m",
    "\033[94m",
    "\033[91m",
]

RESET = "\033[0m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
GRAY = "\033[90m"
CODE_COLOR = "\033[96m"

color_map = {}


def get_download_folder():
    home = Path.home()
    downloads = home / "Downloads"
    return downloads if downloads.exists() else home


def get_color(username):
    if username not in color_map:
        color_map[username] = random.choice(COLORS)
    return color_map[username]

def receive(sock):
    global last_file_data, last_file_name, current_room

    while True:
        try:
            data = sock.recv(10_000_000)
            message = json.loads(data.decode())

            if message["type"] == "system":
                content = message["content"]

                if content.startswith("You joined"):
                    current_room = content.split("'")[1]
                    clear_screen()
                    print(f"=== Room: {current_room} ===\n")

                elif content == "You left the room.":
                    current_room = None
                    clear_screen()
                    print("=== No Room ===\n")

                print(f"{GRAY}[SYSTEM]{RESET} {content}")

            elif message["type"] == "chat":
                color = get_color(message["user"])
                print(f"{color}[{message['user']}]{RESET} {message['content']}")

            elif message["type"] == "code":
                print(f"{GREEN}\n[{message['user']} - CODE]{RESET}")
                print(f"{CODE_COLOR}{message['content']}{RESET}\n")

            elif message["type"] == "file":
                last_file_data = message["content"]
                last_file_name = message["filename"]
                print(f"{YELLOW}[{message['user']}] sent file: {last_file_name} (use /download){RESET}")

        except:
            break

def send(sock):
    global last_file_data, last_file_name, current_room

    sock.sendall(json.dumps({
        "type": "join",
        "user": USERNAME
    }).encode())

    while True:
        msg = input("> ")

        if msg == "/exit":
            sock.sendall(json.dumps({"type": "exit"}).encode())
            print("Disconnected.")
            sock.close()
            break

        elif msg.startswith("/download"):
            if not last_file_data:
                print("No file available.")
                continue

            download_path = get_download_folder() / last_file_name

            with open(download_path, "wb") as f:
                f.write(base64.b64decode(last_file_data))

            print(f"Downloaded to {download_path}")
            continue

        elif msg == "/rooms":
            sock.sendall(json.dumps({
                "type": "list_rooms"
            }).encode())
            continue

        elif msg == "/leave":
            sock.sendall(json.dumps({
                "type": "leave_room"
            }).encode())
            current_room = None
            continue

        elif msg.startswith("/join "):
            parts = msg.split()

            room_name = parts[1]
            password = parts[2] if len(parts) >= 3 else None

            sock.sendall(json.dumps({
                "type": "join_room",
                "room": room_name,
                "password": password
            }).encode())
            continue

        # Block talking if not in room
        if not current_room:
            print("You must /join <room> first.")
            continue

        elif msg.startswith("/code"):
            print("Paste code. End with /end")
            lines = []
            while True:
                line = input()
                if line == "/end":
                    break
                lines.append(line)

            payload = {
                "type": "code",
                "user": USERNAME,
                "content": "\n".join(lines)
            }

        elif msg.startswith("/file"):
            path = msg.split(" ", 1)[1]
            if not os.path.isfile(path):
                print("File not found.")
                continue

            with open(path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()

            payload = {
                "type": "file",
                "user": USERNAME,
                "filename": os.path.basename(path),
                "content": encoded
            }

        elif msg.startswith("/folder"):
            path = msg.split(" ", 1)[1]
            if not os.path.isdir(path):
                print("Folder not found.")
                continue

            zip_name = "temp_folder.zip"
            with zipfile.ZipFile(zip_name, "w") as zipf:
                for root, _, files in os.walk(path):
                    for file in files:
                        zipf.write(os.path.join(root, file))

            with open(zip_name, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()

            os.remove(zip_name)

            payload = {
                "type": "file",
                "user": USERNAME,
                "filename": os.path.basename(path) + ".zip",
                "content": encoded
            }

        else:
            payload = {
                "type": "chat",
                "user": USERNAME,
                "content": msg
            }

        sock.sendall(json.dumps(payload).encode())


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    threading.Thread(target=receive, args=(client,), daemon=True).start()
    send(client)


if __name__ == "__main__":
    main()
# Made by https://github.com/PinkMath/Chat
