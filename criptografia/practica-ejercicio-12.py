from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64


# Texto a cifrar
texto = "He descubierto el error y no volveré a hacerlo mal"
texto_bytes = texto.encode("utf-8")

# Clave del enunciado (AES-256 en hex)
key_bytes = bytes.fromhex("E2CFF885901B3449E9C448BA5B948A8C4EE322152B3F1ACFA0148FB3A426DB74")

# Nonce del enunciado (en base64 → 12 bytes)
nonce_bytes = base64.b64decode("9Yccn/f5nJJhAt2S")

# Cifrado AES-GCM con la clave y el nonce indicados
cipher = AES.new(key_bytes, AES.MODE_GCM, nonce=nonce_bytes)
ciphertext_bytes, tag_bytes = cipher.encrypt_and_digest(texto_bytes)

# Resultado que pide el ejercicio
print("Texto cifrado (hex):", ciphertext_bytes.hex())
print("Texto cifrado (base64):", base64.b64encode(ciphertext_bytes).decode("ascii"))

