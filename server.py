import socket
import threading
from classifier import Classifier
from encryptor import Encryptor

classifier = Classifier()
encryptor = Encryptor()

label_mapping_face = {
    0: "Shalom",
    1: "Person 2",
    2: "Unknown"
}

label_mapping_voice = {
    0: "Background noise",
    1: "Shalom",
    2: "Person 2"
}

def recvall(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def handle_client(client_socket):
    try:
        # קבלת מפתח ציבורי מהלקוח
        key_len = int(client_socket.recv(16).decode().strip())
        client_socket.send(b'OK')
        client_public_key = recvall(client_socket, key_len)
        encryptor.load_peer_public_key(client_public_key)

        # קבלת גודל תמונה
        img_size = int(client_socket.recv(16).decode().strip())
        client_socket.send(b'OK')
        img_data = recvall(client_socket, img_size)
        with open("received_face.jpg", "wb") as f:
            f.write(img_data)

        # קבלת גודל קול
        voice_size = int(client_socket.recv(16).decode().strip())
        client_socket.send(b'OK')
        voice_data = recvall(client_socket, voice_size)
        with open("received_voice.wav", "wb") as f:
            f.write(voice_data)

        # חיזוי
        face_preds = classifier.predict_face("received_face.jpg")
        voice_preds = classifier.predict_voice("received_voice.wav")
        face_label = face_preds.argmax()
        voice_label = voice_preds.argmax()

        face_name = label_mapping_face.get(face_label, "Unknown")
        voice_name = label_mapping_voice.get(voice_label, "Unknown")

        if face_name == voice_name and face_name != "Unknown":
            response = f"Authentication successful: Face={face_name}, Voice={voice_name}"
        else:
            response = f"Authentication failed: Face={face_name}, Voice={voice_name}"

        # הצפנת התשובה ושליחתה
        encrypted_response = encryptor.encrypt(response.encode())
        client_socket.send(str(len(encrypted_response)).ljust(16).encode())
        ack = client_socket.recv(2)
        if ack == b'OK':
            client_socket.sendall(encrypted_response)

    except Exception as e:
        print(f"[-] Exception: {e}")
    finally:
        client_socket.close()
        print("[*] Client disconnected")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 12345))
    server.listen(5)
    print("[*] Server listening on 0.0.0.0:12345")

    while True:
        client_socket, addr = server.accept()
        print(f"[+] Connected: {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    main()
