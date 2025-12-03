# ============================================
# RETO 2 – 11: OTP, modos de bloque, AES y 3DES
# ============================================

from Crypto.Cipher import AES, DES3
from Crypto.Util.Padding import pad, unpad
import base64

# ============================================
# 1. PREGUNTAS TEÓRICAS (para la memoria / formulario)
# ============================================
#
# ¿Cuál es el problema del OTP?
#   → Respuesta correcta:
#     "La longitud necesaria de la clave debe coincidir con el mensaje enviado
#      y la clave debe ser compartida entre emisor y receptor."
#
# Si tuvieras que elegir, de forma general, un modo de operación de cifrado en bloque, ¿Cuál sería?
#   → Respuesta correcta:
#     "GCM"
#
# (No afecta al código, pero lo dejamos documentado aquí.)

# ============================================
# 2. CIFRADO AES/CBC/PKCS7 → SALIDA EN BASE64
# ============================================

texto_aes = "KeepCoding es una pasada"
texto_aes_bytes = texto_aes.encode("utf-8")

clave_aes_hex = "E2CFF885901A5449E9C448BA5B948A8C4EE377152B3F1ACFA0148FB3A426DB72"
clave_aes_bytes = bytes.fromhex(clave_aes_hex)

iv_aes_hex = "00000000000000000000000000000000"
iv_aes_bytes = bytes.fromhex(iv_aes_hex)

cipher_aes = AES.new(clave_aes_bytes, AES.MODE_CBC, iv_aes_bytes)

texto_aes_padded = pad(texto_aes_bytes, AES.block_size, style="pkcs7")
cifrado_aes_bytes = cipher_aes.encrypt(texto_aes_padded)

cifrado_aes_b64 = base64.b64encode(cifrado_aes_bytes).decode("utf-8")

print("=== CIFRADO AES/CBC/PKCS7 ===")
print("Texto claro      :", texto_aes)
print("Clave (hex)      :", clave_aes_hex)
print("IV (hex)         :", iv_aes_hex)
print("Cifrado (Base64) :", cifrado_aes_b64)
print()

# ============================================
# 3. DESCIFRADO 3DES/CBC/PKCS7
# ============================================

cifrado_3des_hex = "2b6911293fc8a5733170c5e1b3f43c6ee51285f679b1f3112f1a628382a5794a"
cifrado_3des_bytes = bytes.fromhex(cifrado_3des_hex)

clave_3des_hex = "2b7e151628aed2a6abf715891defefef123456781232aaff"
clave_3des_bytes = bytes.fromhex(clave_3des_hex)

iv_3des_hex = "1010011111111111"
iv_3des_bytes = bytes.fromhex(iv_3des_hex)

cipher_3des = DES3.new(clave_3des_bytes, DES3.MODE_CBC, iv_3des_bytes)

texto_3des_padded = cipher_3des.decrypt(cifrado_3des_bytes)
texto_3des_bytes = unpad(texto_3des_padded, DES3.block_size, style="pkcs7")
texto_3des = texto_3des_bytes.decode("utf-8")

print("=== DESCIFRADO 3DES/CBC/PKCS7 ===")
print("Cifrado (hex) :", cifrado_3des_hex)
print("Clave (hex)   :", clave_3des_hex)
print("IV (hex)      :", iv_3des_hex)
print("Texto claro   :", texto_3des)
