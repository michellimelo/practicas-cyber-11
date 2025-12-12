from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


# ============================================================
# 14 Derivación de clave con HKDF (SHA-512)
# ============================================================

# Datos del ejercicio

clave_maestra = bytes.fromhex("A2CFF885901A5449E9C448BA5B948A8C4EE377152B3F1ACFA0148FB3A426DB72")
device_id = bytes.fromhex("e43bb4067cbcfab3bec54437b84bef4623e345682d89de9948fbb0afedc461a3")

#-----------------------------------------------------------------------------------------

# 3 HKDF con SHA-512 / Salt: device_id / Info: vacío / Longitud: 32 bytes (AES-256)

hkdf = HKDF(
    algorithm=hashes.SHA512(),
    length=32,
    salt=device_id,
    info=b"",
    backend=default_backend()
)

#-----------------------------------------------------------------------------------------

# 4 Derivación de la clave

clave_derivada = hkdf.derive(clave_maestra)

print("Clave AES-256 derivada (HEX):", clave_derivada.hex().upper())
