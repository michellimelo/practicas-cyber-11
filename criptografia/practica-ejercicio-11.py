import sys
sys.stdout.reconfigure(encoding="utf-8")

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# ===================================================================
# 11. RSA-OAEP (SHA-256): RECUPERAR Y VOLVER A CIFRAR CLAVE SIMÉTRICA
# ===================================================================

# Texto cifrado 

ciphertext_hex = "b72e6fd48155f565dd2684df3ffa8746d649b11f0ed4637fc4c99d18283b32e1709b30c96b4a8a20d5dbc639e9d83a53681e6d96f76a0e4c279f0dffa76a329d04e3d3d4ad629793eb00cc76d10fc00475eb76bfbc1273303882609957c4c0ae2c4f5ba670a4126f2f14a9f4b6f41aa2edba01b4bd586624659fca82f5b4970186502de8624071be78ccef573d896b8eac86f5d43ca7b10b59be4acf8f8e0498a455da04f67d3f98b4cd907f27639f4b1df3c50e05d5bf63768088226e2a9177485c54f72407fdf358fe64479677d8296ad38c6f177ea7cb74927651cf24b01dee27895d4f05fb5c161957845cd1b5848ed64ed3b03722b21a526a6e447cb8ee"
ciphertext = bytes.fromhex(ciphertext_hex)


# Descifrar con RSA_OAEP + SHA256 (clave privada)

with open("clave-rsa-oaep-priv.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None,
    )

plaintext = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    ),
)

print("Clave simétrica recuperada (hex):")
print(plaintext.hex())
print("----------------------------------------")


# Volver a cifrar la misma clave (clave pública)

with open("clave-rsa-oaep-publ.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

new_ciphertext = public_key.encrypt(
    plaintext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    ),
)

print("Nuevo texto cifrado (hex):")
print(new_ciphertext.hex())
