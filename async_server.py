# Made by https://github.com/PinkMath/Chat
import socket
import threading
import json

HOST = "0.0.0.0"
PORT = 5000

clients = {}  
# conn -> {"username": str, "room": str or None}

rooms = {}  
# room_name -> {"clients": [], "password": str or None}


def send_system(conn, text):
    try:
        conn.sendall(json.dumps({
            "type": "system",
            "content": text
        }).encode())
    except:
        pass


def broadcast(room, message, exclude=None):
    if room not in rooms:
        return

    for conn in rooms[room]["clients"]:
        if conn != exclude:
            try:
                conn.sendall(message)
            except:
                remove_client(conn)


def remove_client(conn):
    if conn in clients:
        username = clients[conn]["username"]
        room = clients[conn]["room"]

        if room and room in rooms:
            if conn in rooms[room]["clients"]:
                rooms[room]["clients"].remove(conn)

                msg = json.dumps({
                    "type": "system",
                    "content": f"{username} left the room."
                }).encode()
                broadcast(room, msg)

        del clients[conn]

    conn.close()


def handle_client(conn):
    try:
        data = conn.recv(4096)
        message = json.loads(data.decode())

        if message["type"] != "join":
            conn.close()
            return

        username = message["user"]
        clients[conn] = {"username": username, "room": None}

        send_system(conn, "Connected. Use /rooms to list rooms.")

        while True:
            data = conn.recv(10_000_000)
            if not data:
                break

            message = json.loads(data.decode())

            if message["type"] == "exit":
                break

            if message["type"] == "list_rooms":
                room_list = []
                for r in rooms:
                    lock = "🔒" if rooms[r]["password"] else "🌐"
                    room_list.append(f"{r} {lock}")

                send_system(conn, "Rooms:\n" + "\n".join(room_list) if room_list else "No rooms available.")
                continue

            if message["type"] == "join_room":
                room_name = message["room"]
                password = message.get("password")

                if room_name not in rooms:
                    send_system(conn, "Room does not exist.")
                    continue

                room_data = rooms[room_name]

                if room_data["password"]:
                    if password != room_data["password"]:
                        send_system(conn, "Incorrect password.")
                        continue

                old_room = clients[conn]["room"]
                if old_room and conn in rooms[old_room]["clients"]:
                    rooms[old_room]["clients"].remove(conn)

                clients[conn]["room"] = room_name
                room_data["clients"].append(conn)

                send_system(conn, f"You joined '{room_name}'.")

                broadcast(room_name, json.dumps({
                    "type": "system",
                    "content": f"{username} joined the room."
                }).encode(), conn)

                continue

            if message["type"] == "leave_room":
                current_room = clients[conn]["room"]
                if not current_room:
                    send_system(conn, "You are not in a room.")
                    continue

                rooms[current_room]["clients"].remove(conn)
                clients[conn]["room"] = None
                send_system(conn, "You left the room.")
                continue

            current_room = clients[conn]["room"]
            if not current_room:
                send_system(conn, "Join a room first.")
                continue

            broadcast(current_room, data, conn)

    except:
        pass

    remove_client(conn)


def admin_console():
    while True:
        cmd = input()

        if cmd.startswith("/create "):
            parts = cmd.split()

            if len(parts) < 2:
                print("Usage: /create <room> [password]")
                continue

            room_name = parts[1]
            password = parts[2] if len(parts) >= 3 else None

            if room_name in rooms:
                print("Room already exists.")
                continue

            rooms[room_name] = {
                "clients": [],
                "password": password
            }

            if password:
                print(f"Protected room '{room_name}' created.")
            else:
                print(f"Public room '{room_name}' created.")


def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print("Server started.")
    print("Use /create <room> [password]\n")

    threading.Thread(target=admin_console, daemon=True).start()

    while True:
        conn, _ = server.accept()
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()


if __name__ == "__main__":
    start()

# to get the ip
# --- windows
# 1. open cmd
# 2. run "ipconfig"
# 3. look for "IPv4 Address . . . . . . . . . . : 192.168.x.x"
# That 192.168.x.x (or sometimes 10.x.x.x) is your IP.
# NOTE: If you're in a server the IP'll be different

# --- macOS
# 1. open cmd
# 2. run "ifconfig" or "ipconfig getifaddr en0"
# 3. Look under en0 (Wi-Fi) for: "inet 192.168.x.x".
# NOTE: If you're in a server the IP'll be different

# --- Linux
# 1. open terminal
# 2. run "ip a | grep inet"
# 3. Look for "inet 192.168.x.x"
# NOTE: If you're in a server the IP'll be different

# === and give the IP to the who you want to join ===
# Made by https://github.com/PinkMath/Chat
