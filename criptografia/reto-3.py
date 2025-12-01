from Crypto.Cipher import ChaCha20
from base64 import b64decode

# Criptograma (en base64) del enunciado
cipher_b64 = "pl1yjRNniIvptiQIrX7HPeo4w19FLCnBd/WC1UZEHhOdZHe8KTvjuuoXUPlio5q631wLp7YcKT9jm5M9Aw=="
ciphertext = b64decode(cipher_b64)

# Clave (hex) del enunciado
clave_hex = "FF9DF30474898787A45605CCB9B936D33B780D03CABC81719D52383480DC3120"
clave = bytes.fromhex(key_hex)

# Nonce (en base64) del enunciado
nonce_b64 = "9Yccn/f5nJJhAt2S"
nonce = b64decode(nonce_b64)

# ChaCha20 "puro": no hay tag ni decrypt_and_verify
cipher = ChaCha20.new(clave=clave, nonce=nonce)
plaintext = cipher.decrypt(ciphertext)

print(plaintext.decode("utf-8"))




