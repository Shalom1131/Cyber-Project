# 🔐 Cyber Security Final Project – Face & Voice Authentication System

## 📌 Description
This project implements a secure **authentication system using face and voice recognition** via **Google Teachable Machine** models.  
It includes a **TCP-based client-server architecture** with **hybrid RSA + AES encryption** for all sensitive data, and a modern GUI.  
Designed as part of a final cybersecurity assignment.

---

## ✅ Features

- 📸 Face and 🎤 Voice recognition using custom-trained Teachable Machine models  
- 🖥️ **Client-server architecture** with encrypted TCP socket communication
- 🔐 **Hybrid encryption:**  
  - AES for encrypting all transmitted files (face and voice)  
  - RSA for encrypting session keys and authentication results  
- 🧵 **Multithreaded server** to support multiple clients simultaneously  
- 👨‍💻 **Object-oriented design** (`Classifier`, `Encryptor`, `FileManager`, `AuthResult` classes)  
- 🖼️ Modern **Tkinter GUI** for user interaction (windowed fullscreen, colored status, error handling, dynamic controls)
- 📁 Temp files managed via `FileManager` (auto-cleaning)
- 🗝️ Server uses persistent RSA keypair, client generates a new keypair per session

---

## 🗂️ File Structure

- project/
- │
- ├── client.py # Client application with GUI
- ├── server.py # Multithreaded server
- ├── classifier.py # Loads face/voice models and performs prediction
- ├── encryptor.py # Handles RSA/AES key generation, encryption, decryption
- ├── protocol.py # (Optional) handles message structure (currently unused)
- ├── filemanager.py # Handles temp file creation and cleanup
- ├── file_crypto.py # Hybrid (AES+RSA) encryption/decryption for files
- ├── authresult.py # Auth result class for clear logic/results
- │
- ├── encryptor_keys/
- │ ├── server_private_key.pem # Server's private key (server only)
- │ └── server_public_key.pem # Server's public key (copy to each client)
- │
- ├── models/
- │ ├── face_model.h5 # Trained face recognition model
- │ └── voice_model.h5 # Trained voice recognition model
- │
- ├── temp/ # Temp files for runtime (auto-cleaned)
- │ ├── face.jpg
- │ └── voice.wav
- │
- └── README.md

---

## 🔐 Encryption Strategy

- **Hybrid Encryption for all sensitive communication:**
  - **AES** encrypts each file (face image & voice recording)
  - **RSA** encrypts the random AES key (session-based)
  - Authentication result message (success/fail) is always RSA-encrypted per session
- **Client generates a new RSA keypair for each session**
- **Server keeps a permanent keypair (`encryptor_keys/`)**

---

## 💻 Technologies Used

| Purpose           | Technology             |
|-------------------|------------------------|
| GUI               | Tkinter                |
| Face capture      | OpenCV (`cv2`)         |
| Audio recording   | sounddevice + wavio    |
| ML Inference      | TensorFlow/Keras       |
| Audio processing  | Librosa                |
| Encryption        | PyCryptodome (RSA, AES)|
| Networking        | Python `socket`        |
| Multithreading    | `threading.Thread`     |

---

## 🛠️ How to Run

### 1. **Requirements**
- **Python 3.11.8** (Recommended for compatibility)
- **TensorFlow 2.15**
- **Keras 2.15**
- **Pillow** (for image loading)
- add empty file called "temp" to the environment
- Other libraries: see below

### 2. **Install dependencies**
```bash
pip install tensorflow==2.15 keras==2.15 opencv-python sounddevice wavio librosa pycryptodome pillow
```
### 3. Train and export your models
- **Use Teachable Machine**
- **Export your trained models to .h5** (Keras format)
- **Place the files in:**
- **models/face_model.h5**
- **models/voice_model.h5**

### 4. Generate server RSA keys
- **On the server, run once:**
```bash
python generate_server_keys.py
```
- **Places server_private_key.pem and server_public_key.pem in encryptor_keys/**

- **Copy only server_public_key.pem to each client machine**

### 5. Run the server
```bash
python server.py
```

### 6. Run the client
```bash
python client.py
```

- **GUI will open in windowed fullscreen mode**
- **You can set the server IP and port** (default: 127.0.0.1:12345)
- **Capture image and record voice**
- **Authenticate** (encrypted communication)

---

### Notes
- Server listens on 0.0.0.0:12345 by default (changeable in code)
- Client and server must be on same local network (or test both on same PC with 127.0.0.1)
- Temp files are auto-cleaned after authentication attempt
- All authentication attempts/results are securely encrypted in both directions
- Advanced error/status display in GUI (colored, contextual)
- You can increase security/debug by managing keys, temp files, or adding logging as needed

---

###  👥 Author

Developed by Shalom Pinhas

Cyber Security Final Project (2025)
