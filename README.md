# 🔐 Cyber Security Final Project – Face & Voice Authentication System

## 📌 Description
This project implements a secure **authentication system using face and voice recognition** via **Google Teachable Machine** models.  
It includes a **TCP-based client-server system**, **RSA encryption**, and a **simple GUI interface**.  
Designed as part of a final cybersecurity assignment.

---

## ✅ Features

- 📸 Face and 🎤 Voice recognition using custom-trained Teachable Machine models  
- 🖥️ Client-server architecture with **TCP socket communication**
- 🔒 **RSA encryption used only for protecting the final authentication result**  
- 🧵 Multithreaded server to support multiple clients simultaneously  
- 👨‍💻 Built using **object-oriented design** (`Classifier`, `Encryptor` classes)  
- 🖼️ Simple **Tkinter GUI** for user interaction  
- 📁 Works with webcam and microphone (OpenCV, sounddevice)

---

## 🗂️ File Structure

- project/
- │
- ├── client.py  Client application with GUI
- ├── server.py  Multithreaded server
- ├── classifier.py  Loads face/voice models and performs prediction
- ├── encryptor.py  Handles RSA key generation, encryption, decryption
- ├── protocol.py  Optional: handles message structure (currently unused)
- │
- ├── models/
- │ ├── face_model.h5  Trained face recognition model
- │ └── voice_model.h5  Trained voice recognition model
- │
- ├── received_face.jpg  Temp file for server-side face input
- ├── received_voice.wav  Temp file for server-side voice input


---

## 🔐 Encryption Strategy

- ✅ **RSA is used to encrypt only the final authentication result**  
  (e.g. `"Authentication successful: Face=Shalom, Voice=Shalom"`)  
- ❌ **Face and voice files are transmitted unencrypted**  
  This approach avoids issues with large RSA payloads while meeting the project’s security requirements.

---

## 💻 Technologies Used

| Purpose           | Technology             |
|------------------|------------------------|
| GUI              | Tkinter                |
| Face capture     | OpenCV (`cv2`)         |
| Audio recording  | sounddevice + wavio    |
| ML Inference     | TensorFlow/Keras       |
| Audio processing | Librosa                |
| Encryption       | PyCryptodome (RSA)     |
| Networking       | Python `socket` module |
| Multithreading   | `threading.Thread`     |

---

## 🛠️ How to Run

1. Train your models using [Teachable Machine](https://teachablemachine.withgoogle.com/)  
   - Export models as `.h5` for face and voice
   - Save them to `models/face_model.h5` and `models/voice_model.h5`

2. Install dependencies:
"pip install tensorflow opencv-python sounddevice wavio librosa pycryptodome"
3. Run the server: python server.py
4. Run the client (on same or other machine): python client.py


---

📄 Notes:
- The server automatically starts listening on 0.0.0.0:12345
- Make sure the client and server are on the same local network
- If you're running both locally, keep SERVER_IP = "127.0.0.1" in client.py
- The GUI will guide you through image and voice capture, then display authentication result


---

👥 Author
- Developed by Shalom Pinhas as part of the Cybersecurity final project (2025).