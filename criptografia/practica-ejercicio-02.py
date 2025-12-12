import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
import jks
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# ===============================
# 2. DESCIFRADO PKCS7 / X923
# ===============================

# Clave AES-256 en hexadecimal (32 bytes -> 64 caracteres hex)
clave_hex = "A2CFF885901A5449E9C448BA5B948A8C4EE377152B3F1ACFA0148FB3A426DB72"
clave_bytes = bytes.fromhex(clave_hex)

# IV de 16 bytes todos a 0x00 (AES usa bloque de 16 bytes)
iv_bytes = bytes.fromhex("00000000000000000000000000000000")

# Dato cifrado en base64
texto_b64 = "TQ9SOMKc6aFS9SlxhfK9wT18UXpPCd505Xf5J/5nLI7Of/o0QKIWXg3nu1RRz4QWElezdrLAD5LO4USt3aB/i50nvvJbBiG+le1ZhpR84oI="
texto_cifrado_bytes = b64decode(texto_b64)

#-----------------------------------------------------------------------------------------

# 2.1 Descifrado con PKCS7
cipher = AES.new(clave_bytes, AES.MODE_CBC, iv_bytes)
texto_con_padding = cipher.decrypt(texto_cifrado_bytes)
print(texto_con_padding) #lo hice por curiosidad jeje

texto_plano_bytes = unpad(texto_con_padding, AES.block_size, style="pkcs7")
print(texto_plano_bytes.decode("utf-8"))

#-----------------------------------------------------------------------------------------

# 2.2 Descifrado con X923
cipher = AES.new(clave_bytes, AES.MODE_CBC, iv_bytes)
texto_con_padding = cipher.decrypt(texto_cifrado_bytes)
print(texto_con_padding) #lo hice por curiosidad jeje

texto_plano_bytes = unpad(texto_con_padding, AES.block_size, style="x923")
print(texto_plano_bytes.decode("utf-8"))

#-----------------------------------------------------------------------------------------

# 2.4 Conexión keystore

# Obtener ruta del script y montar ruta del keystore
path = os.path.dirname(__file__)
keystore = os.path.join(path, "keyStorePracticas")

# Cargar el keystore usando la contraseña proporcionada
ks = jks.KeyStore.load(keystore, "123456")

# Buscar la clave por alias
key = None
for alias, sk in ks.secret_keys.items():
    if sk.alias == "cifrado-sim-aes-256":
        key = sk.key
        break

# Validación por si el alias no existe
if key is None:
    raise ValueError("No se encontró la clave 'cifrado-sim-aes-256' en el keystore.")

# Convertir clave a bytes para AES
clave_bytes = key
print("Clave obtenida desde el keystore:", clave_bytes.hex())