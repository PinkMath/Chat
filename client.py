# Made by https://github.com/PinkMath/Chat
import socket
import threading
import random
from blessed import Terminal
from datetime import datetime

# -------------------- CONFIG --------------------
HOST = '192.168.x.xx'  # Change to the server's hoster IP
PORT = 5000 # The PORT need to be the same as in the server

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

term = Terminal()

# -------------------- COLORS --------------------
user_colors = {}
available_colors = [term.red, term.green, term.yellow, term.blue, term.magenta, term.cyan]

# -------------------- USER SETUP --------------------
username = input("Choose your username: ")
user_color = random.choice(available_colors)

# -------------------- GLOBALS --------------------
messages = []
lock = threading.Lock()

# -------------------- UTILITIES --------------------
def timestamp():
    return datetime.now().strftime("%H:%M")

def redraw(input_text=""):
    """Redraw chat window with messages and input line."""
    with lock:
        print(term.home + term.clear)
        print(term.bold_cyan("        💬  LAN TERMINAL CHAT  💬"))
        print()
        max_lines = term.height - 4
        for msg in messages[-max_lines:]:
            print(msg)
        print(term.move(term.height-1, 0) + f"> {input_text}", end="", flush=True)

def add_message(raw_msg):
    """Add a message to the chat with timestamp and colored username."""
    if ": " in raw_msg:
        username_part, message_part = raw_msg.split(": ", 1)
    else:
        # Fallback for messages without normal format
        messages.append(raw_msg)
        redraw()
        return

    # Assign color if new user
    if username_part not in user_colors:
        user_colors[username_part] = random.choice(available_colors)

    color = user_colors[username_part]
    time_str = timestamp()

    # Code block formatting
    if message_part.startswith("Code :") or message_part.startswith("Code ("):
        formatted = f"\n-{color}[{time_str}]\n{username_part}{term.normal}: Code:\n---START---\n{term.yellow}{message_part}---END---{term.normal}"
    else:
        formatted = f"\n-{color}[{time_str}]\n{username_part}{term.normal}: {message_part}"

    messages.append(formatted)
    redraw()

# -------------------- RECEIVE THREAD --------------------
def receive_messages():
    while True:
        try:
            message = client.recv(4096).decode()
            if message == "USERNAME":
                client.send(username.encode())
            else:
                # Skip own messages (already displayed locally)
                if message.startswith(f"{username}:"):
                    continue
                add_message(message)
        except:
            add_message(term.red("Disconnected from server"))
            break

# -------------------- WRITE INPUT --------------------
def write_messages():
    input_text = ""
    redraw(input_text)

    while True:
        key = term.inkey()
        if not key:
            continue

        if key.name == "KEY_ENTER":
            text = input_text.strip()
            if text == "":
                input_text = ""
                redraw(input_text)
                continue

            # -------------------- EXIT --------------------
            if text == "/exit":
                client.close()
                break

            # -------------------- CODE MODE --------------------
            elif text.startswith("/code"):
                print(f"\n{term.magenta}Entering code mode. Type '/end' to finish.{term.normal}\n")
                lines = []
                while True:
                    line = input(f"{term.cyan}... {term.normal}")
                    if line.strip().lower() == "/end":
                        break
                    lines.append(line)

                if not lines:
                    print(f"{term.yellow}No code entered.{term.normal}")
                else:
                    # Compose code message with proper labels
                    user_input = "Code:\n---START---\n" + "\n".join(lines) + "\n---END---"
                    client.send(user_input.encode())
                    # Display locally
                    add_message(f"{username}: {user_input}")

                input_text = ""
                redraw(input_text)

            # -------------------- NORMAL MESSAGE --------------------
            else:
                client.send(text.encode())
                # Display locally as received message
                add_message(f"{username}: {text}")
                input_text = ""
                redraw(input_text)

        elif key.name == "KEY_BACKSPACE":
            input_text = input_text[:-1]
            redraw(input_text)
        elif key.is_sequence:
            continue
        else:
            input_text += key
            redraw(input_text)

# -------------------- START CLIENT --------------------
threading.Thread(target=receive_messages, daemon=True).start()
write_messages()
# Made by https://github.com/PinkMath/Chat
