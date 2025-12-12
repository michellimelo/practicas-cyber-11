import hashlib

# ===============================================
# 5. HASHING: SHA3 (Keccak) y SHA2
# ===============================================


# Hashes dados en el enunciado
hash_sha3_dado = "bced1be95fbd85d2ffcce9c85434d79aa26f24ce82fbd4439517ea3f072d56fe"
hash_sha2_dado = ("4cec5a9f85dcc5c4c6ccb603d124cf1cdc6dfe836459551a1044f4f2908aa5d63739506f6468833d77c07cfd69c488823b8d858283f1d05877120e8c5351c833")

# Comprobación de longitudes → tipo de SHA3 y SHA2 ----
bits_sha3 = len(hash_sha3_dado) * 4          # cada hex = 4 bits
bits_sha2 = len(hash_sha2_dado) * 4

print("Bits del SHA3 recibido:", bits_sha3)
print("Bits del SHA2 recibido:", bits_sha2)


# ---- 2) Generar el SHA3-256 del nuevo texto ----
texto = "En KeepCoding aprendemos cómo protegernos con criptografía."
hash_sha3_nuevo = hashlib.sha3_256(texto.encode("utf-8")).hexdigest()

print("Nuevo SHA3-256:", hash_sha3_nuevo)

