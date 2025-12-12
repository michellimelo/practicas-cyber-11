import hashlib
from Crypto.Cipher import AES

# ===============================================
# 9. KCV(SHA-256) Y KCV(AES) DE UNA CLAVE AES-256
# ===============================================

# Clave AES del enunciado (toda en una sola línea)
key_hex = "A2CFF885901A5449E9C448BA5B948A8C4EE377152B3F1ACFA0148FB3A426DB72"
key = bytes.fromhex(key_hex)

# ----------------------------------------
# 9.1 SHA-256 COMPLETO Y KCV(SHA-256)
# ----------------------------------------

sha256_value = hashlib.sha256(key).digest().hex()

print("SHA-256 COMPLETO:")
print(sha256_value)
print()

kcv_sha256 = sha256_value[0:6]
print("KCV(SHA-256) (primeros 3 bytes):", kcv_sha256)
print("----------------------------------------")

# ----------------------------------------
# 9.2 BLOQUE AES COMPLETO Y KCV(AES)
# ----------------------------------------

# Texto plano (bloque AES de 16 bytes = 128 bits)
plaintext = bytes.fromhex("00000000000000000000000000000000")

# IV de 16 bytes a cero
iv = bytes.fromhex("00000000000000000000000000000000")

cipher = AES.new(key, AES.MODE_CBC, iv)
ciphertext = cipher.encrypt(plaintext)

print("AES-CBC(0x00...) BLOQUE CIFRADO COMPLETO:")
print(ciphertext.hex())
print()

kcv_aes = ciphertext.hex()[0:6]
print("KCV(AES) (primeros 3 bytes):", kcv_aes)
print("----------------------------------------")
