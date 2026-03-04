# Local Terminal Chat

A simple **terminal-based chat application** for local networks, inspired by Discord but ultra-lightweight and clean.  
Supports multiple chat rooms (including password-protected), file and folder sharing, code sharing with syntax coloring, and more — all in your terminal!

---

## Features

- Terminal-based client and server with clean UI  
- Multiple chat rooms with `/create <room> [password]` (server only)  
- Join rooms with `/join <room> [password]`  
- List available rooms with `/rooms`  
- Leave rooms with `/leave`  
- Colored usernames for easy distinction  
- Share code snippets with `/code` (multi-line, ending with `/end`), displayed in cyan color  
- Send files (`/file <path>`) and folders (`/folder <path>`) as zipped archives  
- Download last received file or folder with `/download` (saved to system Downloads folder)  
- Exit cleanly with `/exit`  
- Cross-platform (Windows & Linux)

---

## Getting Started

### Requirements

- Python 3.7+  
- [colorama](https://pypi.org/project/colorama/) (optional, improves color support on Windows)

Install dependencies (optional):

```bash
pip install colorama
```

### Running the server

1. Run the server:
```bash
python async_server.py
```

2. Use the server console to create rooms:
```plain
/create <room_name>
/create <room_name> <password>
```
- Rooms without password are public (🌐), with password are locked (🔒).

### Running the Client

1. Run the client:
```bash
python async_client.py
```

2. Enter the server IP and your username when prompted.
3. Use commands inside the client:

Command | Description
--- | ---
/rooms | List available rooms
/join <room_name> [password] | Join a room (with password if needed)
/leave | Leave current room
/code | Start code input mode; end with `/end`
/file <path> | Send a file
/folder <path> | Send a folder (zipped automatically)
/download | Download last received file/folder
/exit | Disconnect from the server

## How It Works

- When you join a room, the terminal clears and shows the room name as a header.

- Incoming messages show username in color.

- Code blocks appear in bright cyan for easy reading.

- Files and folders can be shared and downloaded easily.

- Only one active room per client at a time.

- You cannot chat unless you have joined a room.

## Project Structure

- `async_server.py` — Server application managing clients, rooms, and commands.

- `async_client` — Client application connecting to the server, sending/receiving messages and files.

## Notes

- The server must be running and accessible to clients.

- Passwords are stored in plaintext in memory for simplicity (not secure for production).

- Designed for trusted local environments and learning/demo purposes.

Enjoy your local chat! 🚀

### Screenshot

<img width="1899" height="1026" alt="2026-03-04-171423_hyprshot" src="https://github.com/user-attachments/assets/20a7ecb9-de3e-4a40-baf0-4412e4ab078b" />

