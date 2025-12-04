from binascii import unhexlify, hexlify
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import sys
sys.stdout.reconfigure(encoding='utf-8')

# ============================================
# 1. DESCIFRADO RSA-OAEP (para descifrado clave privada)
# ============================================

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


# ============================================
# 2. CIFRADO RSA-OAEP (para crifrado clave pública)
# ============================================

# Cargar la clave pública desde el fichero
pubKey = RSA.import_key(open("public-rsa.pem","rb").read())

texto = bytes('Estamos probando a ver qué tal va la clase','utf-8')

# Ciframos
encryptor = PKCS1_OAEP.new(pubKey, SHA256)
encrypted = encryptor.encrypt(texto)

#print("Cifrado:", binascii.hexlify(encrypted))
print("Cifrado:", encrypted.hex())

# ============================================
# 4. VERIFICACIÓN DE FIRMA (firmar privada verificar pública / falta el mensaje)
# ============================================

# Cargar la clave pública
with open("public-rsa.pem", "r") as f:
    keypub = RSA.import_key(f.read())

# 2) Mensaje que se firmó (tienes que poner aquí el texto EXACTO del enunciado)
mensaje = "Podemos firmar cualquier longitud de datos porque previamente lo hasheamos"
mensaje_bytes = mensaje.encode("utf-8")

# 3) Calcular el hash SHA-256 del mensaje
h = SHA256.new(mensaje_bytes)

# 4) Firma en HEX dada en el ejercicio
firma_hex = ("4c3319d61533768385245abe64faa6556468745033081a2a452d70e24e7a43b5b53ef2c143fa497b6ae0253c89f7c5f58b65e0a9eed8d35975aa81de69f3f38bddd03db3d0fd41158071abf596324f071a297b6384e2f8c827c932fe4c67aa6945b1c4a05cdf5a63e7d1416f83405af77d74a1ce506739e4d16eb43ca44f012092af615c1ba26eb3356dcee2b9e55a04fac35c6a49bd8b3a88c28095c98f9fd1792ed98aabd752ff9c2723133548c68fa69ab13622fe1819e29c25e0694e9eb45bd148858905e883dd3fdc78142f4de5f411ee70407bb563a990c8ed63183eca87195a6946bcbaef968ac917a1198ee717d1f9dc84c6fdc624e876a67bffc82aa6ef850d8965b558821e631739a8a618a4674e3b45aa8b0c8c884c6354fd884dbc31d158e17c88da4e50e8323784ed44f1478c485c33610d458a1ef3008912346d7ddc8a3b946dc6a475ef10a1be31867575d8ea16e7ffbdbedeb3c518afb83ace6365845819e5f6ff2884515f0c6636f50cc667f30cc23f54289e04b9d77271")

firma = bytes.fromhex(firma_hex)

# 5) Verificar firma RSA-PKCS1 v1.5
try:
    pkcs1_15.new(keypub).verify(h, firma)
    print("Firma VÁLIDA")
except (ValueError, TypeError):
    print("Firma NO válida")
