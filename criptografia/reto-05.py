from binascii import unhexlify, hexlify
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

# ============================================
# 1. DESCIFRADO RSA-OAEP (para descrifrado se usa solo clave privada)
# ============================================

import os
print("Carpeta actual:", os.getcwd())

# Cargar la clave privada desde el fichero
privKey = RSA.import_key(open("private-rsa.pem","rb").read())

# Crear el descifrador RSA-OAEP con SHA256
decryptor = PKCS1_OAEP.new(privKey, SHA256)

# Texto cifrado
cipher_hex = "5b3b37ab1221b43a985308fdb54d4d92f6dd7afa4096d7478e538d4f0624a5cc03d004bbd44d8d9856e26f1341301e79baf00c5e1b3b8016f47276b0e706396dca99ad4fe56023e3c8b8eae3118df225070ff6029531c53256bd5e3888f1143033fc8ab2999635d341075dd2613976d19591c808b1b4f00db6168e84c7bf136fcbf48534b0be045da166d19271c5721b8af5c61e2da738619d3f8b48b19441d33a9a751fee4eba0634547b05a8b79b266548b63ceea6464f71093b13ebbd5049763d561749360222d6ce4f278b486bf419e5cb8928d974edbc0c3c414b13341da799b1ad11800001c72f3ba5fefbd7097e1d5776451b6865a4165e99101c39064fe01e23e6fc10d080b813ea4f4d3ef44478e3a6c27bd6dc5c08948d0e4ae9d843ea5277f3f911706e2f75e466ef159050ba3076a6a81022772020be9487d2fc0a058f3ea12a0fc8158c75514ba7c711a5b7a2c1650c6790e01fa26aac3b1404039134a902f7ca737171fd0b965cc6683c85c48fb2d369dc5abbee0bbd3f3645"
cipher_bytes = bytes.fromhex(cipher_hex)

# Desciframos
plaintext = decryptor.decrypt(cipher_bytes)

print("Texto descifrado:", plaintext.decode())
