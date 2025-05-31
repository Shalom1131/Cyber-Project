# protocol.py

# HEADER = 4 בתים לזיהוי
# LEN_FACE, LEN_VOICE = 4 בתים כל אחד
# [HEADER][LEN_FACE][LEN_VOICE][ENCRYPTED_FACE][ENCRYPTED_VOICE]

import struct

HEADER = b"AUTH"

def pack_message(face_bytes: bytes, voice_bytes: bytes) -> bytes:
    return HEADER + struct.pack(">II", len(face_bytes), len(voice_bytes)) + face_bytes + voice_bytes

def unpack_message(data: bytes):
    if data[:4] != HEADER:
        raise ValueError("Invalid header")
    face_len, voice_len = struct.unpack(">II", data[4:12])
    face_data = data[12:12+face_len]
    voice_data = data[12+face_len:12+face_len+voice_len]
    return face_data, voice_data
