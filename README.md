## LAN Terminal Chat

A simple terminal-based chat application for your local network, built with Python. Features include colored usernames, timestamps, multi-line code blocks (/code), and Discord-style chat layout — all in the terminal.

## Features

✅ Real-time chat over LAN

✅ Colored usernames for each user

✅ Timestamps for each message [HH:MM]

✅ Multi-line code blocks using /code

✅ Graceful exit with /exit

✅ Auto-scroll terminal display

✅ Join/leave notifications in the server console

✅ Clean, Discord-like layout

## Screenshot

<img width="1915" height="1042" alt="2026-03-03-042546_hyprshot" src="https://github.com/user-attachments/assets/36c3de06-311e-4d40-b838-cc7b35526337" />

## Requirements

- Python 3.8+
- blessed (pip install blessed)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/PinkMath/Chat.git
cd Chat
```

2. Install depencies:
```bash
pip install blessed
```

## Usage
1. Start the server
```bash
python server.py
```
- The server listens on `0.0.0.0:5000 by` default.
- Logs client joins and disconnections.

2. Start the client
```bash
python client.py
```
- Enter a username when prompted.
- Type messages and press Enter to send.
- Use commands:

Command | Description
--- | ---
/exit | Exit the chat gracefully
/code | Enter multi-line mode; end with `/end`
