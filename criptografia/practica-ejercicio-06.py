import sys
sys.stdout.reconfigure(encoding="utf-8")

import os
import jks
import hmac
import hashlib

# ===============================================
# 6. HMAC-SHA256 VERIFICAR CLAVE REAL DEL KEYSTORE
# ===============================================

# Texto indicado
texto = "Siempre existe más de una forma de hacerlo, y más de una solución válida"

# Ruta del keystore (mismo directorio del script)
path = os.path.dirname(__file__)
keystore = os.path.join(path, "KeyStorePracticas")

# Cargar keystore
ks = jks.KeyStore.load(keystore, "123456")

# Obtener la clave exacta que Python está usando
key = None
for alias, sk in ks.secret_keys.items():
    if sk.alias == "hmac-sha256":   # alias tal cual aparece en el keystore
        key = sk.key
        break

if key is None:
    raise ValueError("No se encontró la clave 'hmac-sha256' en el keystore.")

# Mostrar la clave que realmente se está usando
print("Clave real usada en hex:", key.hex())

# Calcular HMAC-SHA256 del texto con la clave real
hmac_hex = hmac.new(key, texto.encode("utf-8"), hashlib.sha256).hexdigest()

print("HMAC-SHA256:", hmac_hex)

