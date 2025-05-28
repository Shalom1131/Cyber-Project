import socket
import cv2
import sounddevice as sd
import wavio
import threading
import tkinter as tk
from tkinter import messagebox
import numpy as np
from encryptor import Encryptor

SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345
encryptor = Encryptor()

def capture_image(filename="face.jpg"):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Cannot open camera")
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise Exception("Failed to capture image")
    cv2.imwrite(filename, frame)
    return filename

def record_audio(filename="voice.wav", duration=3, fs=44100):
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    wavio.write(filename, recording, fs, sampwidth=2)
    return filename

def send_file(sock, filepath):
    with open(filepath, "rb") as f:
        data = f.read()
    size_str = str(len(data)).ljust(16)
    sock.send(size_str.encode())
    ack = sock.recv(2)
    if ack != b'OK':
        raise Exception("No ACK from server")
    sock.sendall(data)

def authenticate():
    try:
        img_file = capture_image()
        audio_file = record_audio()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((SERVER_IP, SERVER_PORT))

        # שליחת מפתח ציבורי
        pubkey = encryptor.export_public_key()
        sock.send(str(len(pubkey)).ljust(16).encode())
        ack = sock.recv(2)
        if ack != b'OK':
            raise Exception("Server didn't ack public key")
        sock.sendall(pubkey)

        status_label.config(text="[*] Sending image...")
        send_file(sock, img_file)

        status_label.config(text="[*] Sending audio...")
        send_file(sock, audio_file)

        status_label.config(text="[*] Waiting for encrypted result...")

        # קבלת תשובה מוצפנת
        resp_len = int(sock.recv(16).decode().strip())
        sock.send(b'OK')
        encrypted_response = recvall(sock, resp_len)

        decrypted = encryptor.decrypt(encrypted_response).decode()
        status_label.config(text=f"[+] Server response: {decrypted}")
        messagebox.showinfo("Authentication Result", decrypted)

    except Exception as e:
        status_label.config(text=f"[-] Error: {str(e)}")
        messagebox.showerror("Error", str(e))

def recvall(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def on_authenticate_click():
    threading.Thread(target=authenticate).start()

root = tk.Tk()
root.title("Face & Voice Authentication")

auth_button = tk.Button(root, text="Authenticate", command=on_authenticate_click, width=20, height=2)
auth_button.pack(pady=20)

status_label = tk.Label(root, text="Ready", fg="blue")
status_label.pack()

root.mainloop()
