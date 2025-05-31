# file_crypto.py
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes

def pad(data):
    # PKCS7 padding
    pad_len = 16 - (len(data) % 16)
    return data + bytes([pad_len]) * pad_len

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

def encrypt_file_hybrid(data: bytes, encryptor):
    # 1. צור מפתח AES רנדומלי
    aes_key = get_random_bytes(32)  # AES-256
    cipher_aes = AES.new(aes_key, AES.MODE_CBC)
    iv = cipher_aes.iv
    encrypted_data = cipher_aes.encrypt(pad(data))

    # 2. הצפן את המפתח AES עם RSA
    encrypted_aes_key = encryptor.encrypt(aes_key + iv)  # מצפין מפתח ואיווי יחד

    # 3. שלח קודם את אורך המפתח המוצפן (2 בתים), אח"כ את המפתח המוצפן, ואז את הדאטה המוצפן
    return len(encrypted_aes_key).to_bytes(2, "big") + encrypted_aes_key + encrypted_data

def decrypt_file_hybrid(data: bytes, encryptor):
    # 1. קבל אורך מפתח ה־AES המוצפן
    enc_key_len = int.from_bytes(data[:2], "big")
    encrypted_aes_key = data[2:2+enc_key_len]
    encrypted_data = data[2+enc_key_len:]

    # 2. פענח את מפתח ה־AES + iv עם RSA
    aes_and_iv = encryptor.decrypt(encrypted_aes_key)
    aes_key = aes_and_iv[:32]
    iv = aes_and_iv[32:48]
    cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
    decrypted_data = cipher_aes.decrypt(encrypted_data)
    return unpad(decrypted_data)
