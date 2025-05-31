import socket
import cv2
import sounddevice as sd
import wavio
import threading
import tkinter as tk
from encryptor import Encryptor
from filemanager import FileManager
from file_crypto import encrypt_file_hybrid

BG_COLOR = "#F4F6FA"
TITLE_COLOR = "#283593"
LABEL_COLOR = "#3F51B5"
BTN_COLOR = "#1976D2"
BTN_TEXT_COLOR = "#FFF"
RESULT_COLOR = "#444"
SUCCESS_COLOR = "#27ae60"
FAIL_COLOR = "#C62828"
STATUS_COLOR = "#000"

encryptor = Encryptor()

captured_image_path = None
recorded_audio_path = None

def load_server_public_key():
    with open("encryptor_keys/server_public_key.pem", "rb") as f:
        key = f.read()
    encryptor.load_peer_public_key(key)

def set_status(msg, color=STATUS_COLOR, show_status=True):
    if show_status:
        status_label.config(text=f"Status: {msg}", fg=color)
    else:
        status_label.config(text=msg, fg=color)
    root.update()

def capture_image_action():
    global captured_image_path
    try:
        set_status("Capturing image...")
        filepath = FileManager.get_temp_path("face.jpg")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise Exception("Cannot open camera")
        ret, frame = cap.read()
        cap.release()
        if not ret:
            raise Exception("Failed to capture image")
        cv2.imwrite(filepath, frame)
        captured_image_path = filepath
        set_status("Image captured!")
        capture_btn.config(state="disabled")
        check_ready_for_auth()
    except Exception as e:
        set_status(f"[-] Error: {str(e)}", color=FAIL_COLOR)

def record_audio_action():
    global recorded_audio_path
    try:
        set_status("Recording audio...")
        duration_str = duration_entry.get().strip()
        try:
            duration = int(duration_str)
            if duration < 1 or duration > 10:
                duration = 3
        except ValueError:
            duration = 3

        filepath = FileManager.get_temp_path("voice.wav")
        recording = sd.rec(int(duration * 44100), samplerate=44100, channels=1)
        sd.wait()
        wavio.write(filepath, recording, 44100, sampwidth=2)
        recorded_audio_path = filepath
        set_status("Audio recorded!")
        record_btn.config(state="disabled")
        check_ready_for_auth()
    except Exception as e:
        set_status(f"[-] Error: {str(e)}", color=FAIL_COLOR)

def check_ready_for_auth():
    if captured_image_path and recorded_audio_path:
        auth_button.config(state="normal")
        set_status("Ready")

def send_file(sock, filepath):
    load_server_public_key()
    with open(filepath, "rb") as f:
        data = f.read()
    encrypted_data = encrypt_file_hybrid(data, encryptor)
    size_str = str(len(encrypted_data)).ljust(16)
    sock.send(size_str.encode())
    ack = sock.recv(2)
    if ack != b'OK':
        raise Exception("No ACK from server")
    sock.sendall(encrypted_data)

def recvall(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def authenticate():
    global captured_image_path, recorded_audio_path
    try:
        if not captured_image_path or not recorded_audio_path:
            raise Exception("You must capture image and record audio first.")

        ip = ip_entry.get().strip() or "127.0.0.1"
        port_str = port_entry.get().strip() or "12345"
        try:
            port = int(port_str)
        except ValueError:
            raise Exception("Port must be a number!")

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))

        # Send client's public key to the server
        pubkey = encryptor.export_public_key()
        sock.send(str(len(pubkey)).ljust(16).encode())
        ack = sock.recv(2)
        if ack != b'OK':
            raise Exception("Server didn't ack public key")
        sock.sendall(pubkey)

        set_status("Sending image...")
        send_file(sock, captured_image_path)

        set_status("Sending audio...")
        send_file(sock, recorded_audio_path)

        set_status("Waiting for encrypted result...")

        resp_len = int(sock.recv(16).decode().strip())
        sock.send(b'OK')
        encrypted_response = recvall(sock, resp_len)

        decrypted = encryptor.decrypt(encrypted_response).decode()

        # Show result (no "Status:") in color, hide all except Try Again + Exit
        if "successful" in decrypted.lower():
            set_status(decrypted, color=SUCCESS_COLOR, show_status=False)
        else:
            set_status(decrypted, color=FAIL_COLOR, show_status=False)

        hide_input_fields()
        auth_button.pack_forget()
        try_again_button.pack(pady=8)
        exit_btn.pack(pady=(8, 12))

        FileManager.delete_files("face.jpg", "voice.wav")
        captured_image_path = None
        recorded_audio_path = None

    except Exception as e:
        hide_input_fields()
        set_status(f"[-] Error: {str(e)}", color=FAIL_COLOR)
        auth_button.pack_forget()
        try_again_button.pack(pady=8)
        exit_btn.pack(pady=(8, 12))

def on_authenticate_click():
    auth_button.config(state="disabled")
    threading.Thread(target=authenticate).start()

def on_try_again_click():
    global captured_image_path, recorded_audio_path
    show_input_fields()
    set_status("Waiting for user")
    try_again_button.pack_forget()
    # Exit button stays visible
    capture_btn.config(state="normal")
    record_btn.config(state="normal")
    auth_button.config(state="disabled")
    captured_image_path = None
    recorded_audio_path = None

def hide_input_fields():
    ip_label.pack_forget()
    ip_entry.pack_forget()
    port_label.pack_forget()
    port_entry.pack_forget()
    duration_label.pack_forget()
    duration_entry.pack_forget()
    capture_btn.pack_forget()
    record_btn.pack_forget()
    # auth_button ו־exit_btn לא מוסתרים כאן!

def show_input_fields():
    ip_label.pack(pady=5)
    ip_entry.pack(pady=6)
    port_label.pack(pady=2)
    port_entry.pack(pady=6)
    duration_label.pack(pady=2)
    duration_entry.pack(pady=10)
    capture_btn.pack(pady=10)
    record_btn.pack(pady=6)
    auth_button.pack(pady=32)
    exit_btn.pack(pady=(24, 12))

root = tk.Tk()
root.title("AI Face & Voice Authentication")
root.configure(bg=BG_COLOR)
root.geometry("1200x800")
root.resizable(True, True)
root.state('zoomed')  # windowed fullscreen

title_label = tk.Label(root, text="AI Face & Voice Authentication", font=("Arial", 24, "bold"), fg=TITLE_COLOR, bg=BG_COLOR)
title_label.pack(pady=(28, 20))

main_frame = tk.Frame(root, bg=BG_COLOR)
main_frame.pack(expand=True)

ip_label = tk.Label(main_frame, text="Server IP:", fg=LABEL_COLOR, bg=BG_COLOR, font=("Arial", 12, "bold"))
ip_label.pack()
ip_entry = tk.Entry(main_frame, font=("Arial", 12), width=25, relief="ridge", bd=2)
ip_entry.insert(0, "127.0.0.1")
ip_entry.pack(pady=6)

port_label = tk.Label(main_frame, text="Server Port:", fg=LABEL_COLOR, bg=BG_COLOR, font=("Arial", 12, "bold"))
port_label.pack()
port_entry = tk.Entry(main_frame, font=("Arial", 12), width=25, relief="ridge", bd=2)
port_entry.insert(0, "12345")
port_entry.pack(pady=6)

duration_label = tk.Label(main_frame, text="Voice recording time (seconds, 1-10):", fg=LABEL_COLOR, bg=BG_COLOR, font=("Arial", 12, "bold"))
duration_label.pack()
duration_entry = tk.Entry(main_frame, font=("Arial", 12), width=25, relief="ridge", bd=2)
duration_entry.insert(0, "3")
duration_entry.pack(pady=10)

capture_btn = tk.Button(main_frame, text="Capture Image", command=capture_image_action,
                        font=("Arial", 12, "bold"), width=20, height=1, bg="#4CAF50", fg=BTN_TEXT_COLOR, bd=0,
                        activebackground="#388E3C", activeforeground=BTN_TEXT_COLOR, relief="flat", cursor="hand2")
capture_btn.pack(pady=10)

record_btn = tk.Button(main_frame, text="Record Voice", command=record_audio_action,
                        font=("Arial", 12, "bold"), width=20, height=1, bg="#FF9800", fg=BTN_TEXT_COLOR, bd=0,
                        activebackground="#F57C00", activeforeground=BTN_TEXT_COLOR, relief="flat", cursor="hand2")
record_btn.pack(pady=6)

auth_button = tk.Button(main_frame, text="Authenticate", command=on_authenticate_click,
                        font=("Arial", 14, "bold"), width=20, height=2, bg=BTN_COLOR, fg=BTN_TEXT_COLOR, bd=0,
                        activebackground="#1565C0", activeforeground=BTN_TEXT_COLOR, relief="flat", cursor="hand2", state="disabled")
auth_button.pack(pady=32)

try_again_button = tk.Button(main_frame, text="Try Again", command=on_try_again_click,
                            font=("Arial", 14, "bold"), width=20, height=2, bg=BTN_COLOR, fg=BTN_TEXT_COLOR, bd=0,
                            activebackground="#1565C0", activeforeground=BTN_TEXT_COLOR, relief="flat", cursor="hand2")

exit_btn = tk.Button(main_frame, text="Exit", command=root.destroy,
                     font=("Arial", 12, "bold"), width=20, height=1,
                     bg="#B71C1C", fg="#FFF", bd=0,
                     activebackground="#D32F2F", activeforeground="#FFF", relief="flat", cursor="hand2")
exit_btn.pack(pady=(24, 12))

status_label = tk.Label(main_frame, text="Status: Waiting for user", fg=STATUS_COLOR, bg=BG_COLOR, font=("Arial", 14, "bold"))
status_label.pack(pady=14)

root.mainloop()
