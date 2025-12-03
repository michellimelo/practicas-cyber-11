# ============================================
# RETO 5 – RSA-OAEP y RSA-PKCS1v1_5
# ============================================

from binascii import unhexlify, hexlify
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

# ============================================
# 1. CARGA DE CLAVES RSA
# ============================================

with open("private-rsa.pem", "rb") as f:
    private_key = RSA.import_key(f.read())

with open("public-rsa.pem", "rb") as f:
    public_key = RSA.import_key(f.read())

# ============================================
# 2. DESCIFRADO RSA-OAEP
# ============================================

# Ciphertext dado en el enunciado (hex)
cifra_hex = (
    "5b3b37ab1221b43a985308fdb54d4d92f6dd7afa4096d7478e538d4f0624a5cc03d004bbd44d8d98"
    "56e26f1341301e79baf00c5e1b3b8016f47276b0e706396dca99ad4fe56023e3c8b8eae3118df225"
    "070ff6029531c53256bd5e3888f1143033fc8ab2999635d341075dd2613976d19591c808b1b4f00d"
    "b6168e84c7bf136fcbf48534b0be045da166d19271c5721b8af5c61e2da738619d3f8b48b19441d3"
    "3a9a751fee4eba0634547b05a8b79b266548b63ceea6464f71093b13ebbd5049763d561749360222"
    "d6ce4f278b486bf419e5cb8928d974edbc0c3c414b13341da799b1ad11800001c72f3ba5fefbd709"
    "7e1d5776451b6865a4165e99101c39064fe01e23e6fc10d080b813ea4f4d3ef44478e3a6c27bd6dc"
    "5c08948d0e4ae9d843ea5277f3f911706e2f75e466ef159050ba3076a6a81022772020be9487d2fc"
    "0a058f3ea12a0fc8158c75514ba7c711a5b7a2c1650c6790e01fa26aac3b1404039134a902f7ca73"
    "7171fd0b965cc6683c85c48fb2d369dc5abbee0bbd3f3645"
)

cifra_bytes = bytes.fromhex(cifra_hex)

cipher_rsa_oaep_dec = PKCS1_OAEP.new(private_key)
texto_plano_bytes = cipher_rsa_oaep_dec.decrypt(cifra_bytes)

print("=== DESCIFRADO RSA-OAEP ===")
print("Texto en claro:", texto_plano_bytes.decode("utf-8"))
print()

# ============================================
# 3. CIFRADO RSA-OAEP
# ============================================

mensaje_claro = "Estamos probando a ver qué tal va la clase"
mensaje_claro_bytes = mensaje_claro.encode("utf-8")

cipher_rsa_oaep_enc = PKCS1_OAEP.new(public_key)
cifrado_nuevo_bytes = cipher_rsa_oaep_enc.encrypt(mensaje_claro_bytes)

cifrado_nuevo_hex = cifrado_nuevo_bytes.hex()

print("=== CIFRADO RSA-OAEP ===")
print("Mensaje claro:", mensaje_claro)
print("Cifrado (hex):", cifrado_nuevo_hex)
print()

# ============================================
# 4. COMENTARIO TEÓRICO – RSA-PKCS1v1_5
# ============================================
# Pregunta del enunciado:
# ¿Es buena idea usar RSA-PKCS1v1_5 hoy en día?
#
# Respuesta correcta (para poner en la memoria):
# "En firma, no es mala opción, en cifrado intentamos evitarla."

# ============================================
# 5. VERIFICACIÓN FIRMA RSA-PKCS1v1_5
# ============================================

# Firma dada en el enunciado (hex)
firma_hex = (
    "4c3319d61533768385245abe64faa6556468745033081a2a452d70e24e7a43b5b53ef2c143fa497b"
    "6ae0253c89f7c5f58b65e0a9eed8d35975aa81de69f3f38bddd03db3d0fd41158071abf596324f07"
    "1a297b6384e2f8c827c932fe4c67aa6945b1c4a05cdf5a63e7d1416f83405af77d74a1ce506739e4"
    "d16eb43ca44f012092af615c1ba26eb3356dcee2b9e55a04fac35c6a49bd8b3a88c28095c98f9fd1"
    "792ed98aabd752ff9c2723133548c68fa69ab13622fe1819e29c25e0694e9eb45bd148858905e883"
    "dd3fdc78142f4de5f411ee70407bb563a990c8ed63183eca87195a6946bcbaef968ac917a1198ee7"
    "17d1f9dc84c6fdc624e876a67bffc82aa6ef850d8965b558821e631739a8a618a4674e3b45aa8b0c"
    "8c884c6354fd884dbc31d158e17c88da4e50e8323784ed44f1478c485c33610d458a1ef300891234"
    "6d7ddc8a3b946dc6a475ef10a1be31867575d8ea16e7ffbdbedeb3c518afb83ace6365845819e5f6"
    "ff2884515f0c6636f50cc667f30cc23f54289e04b9d77271"
)
firma_bytes = bytes.fromhex(firma_hex)

# IMPORTANTE: aquí debes poner el TEXTO que se supone que está firmado.
# El enunciado no lo especifica; el profesor suele indicarlo aparte.
# De momento dejamos un placeholder:
mensaje_firmado = "TEXTO_QUE_EL_PROFESOR_HAYA INDICADO"
mensaje_firmado_bytes = mensaje_firmado.encode("utf-8")

hash_mensaje = SHA256.new(mensaje_firmado_bytes)

print("=== VERIFICACIÓN FIRMA RSA-PKCS1v1_5 ===")
try:
    pkcs1_15.new(public_key).verify(hash_mensaje, firma_bytes)
    print("La firma ES válida.")
except (ValueError, TypeError):
    print("La firma NO es válida.")
