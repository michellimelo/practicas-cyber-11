import sys
sys.stdout.reconfigure(encoding="utf-8")

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, ed25519

# ============================================================
# 13. FIRMA RSA PKCS#1 v1.5 Y FIRMA ED25519
# ============================================================

# Mensaje a firmar

mensaje = "El equipo está preparado para seguir con el proceso, necesitaremos más recursos."
mensaje_bytes = mensaje.encode("utf-8")

#-----------------------------------------------------------------------------------------

# Firma RSA PKCS#1 v1.5 (SHA-256)

f = open("clave-rsa-oaep-priv.pem", "rb")
rsa_private_key = serialization.load_pem_private_key(f.read(), password=None)
f.close()

firma_rsa = rsa_private_key.sign(
    mensaje_bytes,
    padding.PKCS1v15(),
    hashes.SHA256(),
)

print("Firma RSA PKCS#1 v1.5 (hex):")
print(firma_rsa.hex())
print("----------------------------------------")

#-----------------------------------------------------------------------------------------

# 2 Firma con curva elíptca ED25519

f = open("ed25519-priv", "rb")
key_bytes = f.read()
f.close()

seed = key_bytes[:32]  # SOLO 32 bytes
ed_private_key = ed25519.Ed25519PrivateKey.from_private_bytes(seed)

firma_ed25519 = ed_private_key.sign(mensaje_bytes)

print("Firma Ed25519 (hex):")
print(firma_ed25519.hex())
print("----------------------------------------")