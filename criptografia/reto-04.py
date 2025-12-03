# ============================================
# 1. DATOS DEL EJERCICIO
# ============================================

texto1 = "KeepCoding Mola mucho"
texto2 = "KeepCoding Mola Mucho"   # cambia solo una letra

# Convertimos a bytes (UTF-8), requisito para cualquier hash
texto1_bytes = texto1.encode("utf-8")
texto2_bytes = texto2.encode("utf-8")

# ============================================
# 2. HASH SHA3-512
# ============================================

import hashlib

hash1 = hashlib.sha3_512(texto1_bytes).hexdigest()
hash2 = hashlib.sha3_512(texto2_bytes).hexdigest()

# ============================================
# 3. RESULTADOS
# ============================================

print("Texto 1:", texto1)
print("SHA3-512:", hash1)
print()

print("Texto 2:", texto2)
print("SHA3-512:", hash2)
print()

# ============================================
# 4. OBSERVACIÓN (propiedad de hash)
# ============================================

print("Propiedad destacada: Un pequeño cambio en la entrada genera un hash completamente distinto (efecto avalancha).")



# ============================================
# 5. HMAC-SHA256 DEL TEXTO
# ============================================

import hmac
import hashlib

# Texto del ejercicio
texto_hmac = "KeepCoding Mola mucho"
texto_hmac_bytes = texto_hmac.encode("utf-8")

# Clave proporcionada (hexadecimal)
clave_hex = "7212A51C997E14B4DF08D55967641B0677CA31E049E672A4B06861AA4D5826EB"
clave_bytes = bytes.fromhex(clave_hex)

# Cálculo del HMAC usando SHA-256
hmac_resultado = hmac.new(clave_bytes, texto_hmac_bytes, hashlib.sha256).hexdigest()

print("Texto:", texto_hmac)
print("Clave (hex):", clave_hex)
print("HMAC-SHA256:", hmac_resultado)
