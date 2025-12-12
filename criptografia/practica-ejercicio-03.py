from Crypto.Cipher import ChaCha20, ChaCha20_Poly1305
from base64 import b64decode, b64encode
from Crypto.Random import get_random_bytes

# ==================================================
# 3. CIFRADO DE FLUJO / CHACHA20 / ChaCha20-Poly1305
# ==================================================

texto_plano = bytes('KeepCoding te enseña a codificar y a cifrar', 'UTF-8')

clave = bytes.fromhex('AF9DF30474898787A45605CCB9B936D33B780D03CABC81719D52383480DC3120')

# Nonce en Base64 a bytes
nonce_b64 = "9Yccn/f5nJJhAt2S"
nonce_mensaje = b64decode(nonce_b64)

# Con la clave y con el nonce se cifra. El nonce debe ser único por mensaje
cipher = ChaCha20.new(key=clave, nonce=nonce_mensaje)
texto_cifrado = cipher.encrypt(texto_plano)

print('Mensaje cifrado en hex = ', texto_cifrado.hex())

#-----------------------------------------------------------------------------------------

# 3.1 Propuesta mejora ChaCha20-Poly1305

# Texto
texto_plano = bytes('KeepCoding te enseña a codificar y a cifrar', 'UTF-8')

# Clave del keystore
clave = bytes.fromhex("AF9DF30474898787A45605CCB9B936D33B780D03CABC81719D52383480DC3120")

# Nonce en Base64 a bytes
nonce = b64decode("9Yccn/f5nJJhAt2S")

# Cifrado autenticado
cipher = ChaCha20_Poly1305.new(key=clave, nonce=nonce)
ciphertext, tag = cipher.encrypt_and_digest(texto_plano)

print("Mensaje cifrado en hex:", ciphertext.hex())
print("Tag que añade integridad :", tag.hex())