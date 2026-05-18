from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def encrypt_value(value, key):
    fernet = Fernet(key)
    encrypted_value = fernet.encrypt(value.encode())
    return encrypted_value

def decrypt_value(encrypted_value, key):
    fernet = Fernet(key)
    decrypted_value = fernet.decrypt(encrypted_value).decode()
    return decrypted_value