import jwt

# ===============================
# 4. ANÁLISIS / VALIDACIÓN JWT HS256
# ===============================

clave = "Con KeepCoding aprendemos"

# JWT original del ejercicio (rol isNormal)
jwt_original = ("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c3VhcmlvIjoiRG9uIFBlcGl0byBkZSBsb3MgcGFsb3RlcyIsInJvbCI6ImlzTm9ybWFsIiwiaWF0IjoxNjY3OTMzNTMzfQ.gfhw0dDxp6oixMLXXRP97W4TDTrv0y7B5YjD0U8ixrE")

# JWT modificado por un atacante (rol isAdmin)
jwt_hacker = ("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c3VhcmlvIjoiRG9uIFBlcGl0byBkZSBsb3MgcGFsb3RlcyIsInJvbCI6ImlzQWRtaW4iLCJpYXQiOjE2Njc5MzM1MzN9.krgBkzCBQ5WZ8JnZHuRvmnAZdg4ZMeRNv2CIAODlHRI")

# ===================================================
# 4.1 DECODIFICAR SIN VALIDAR (solo para ver la info)
# ====================================================

print("Header original:", jwt.get_unverified_header(jwt_original))
print("Payload original (sin verificar):",
      jwt.decode(jwt_original, options={"verify_signature": False}))

print("Payload hacker (sin verificar):",
      jwt.decode(jwt_hacker, options={"verify_signature": False}))

# ===============================
# 4.2 VALIDAR FIRMA DEL JWT BUENO
# ===============================

try:
    valido = jwt.decode(jwt_original, clave, algorithms=["HS256"])
    print("JWT original válido:", valido)
except Exception as e:
    print("Error validando el JWT original:", e)

# ===============================
# 4.3 VALIDAR FIRMA DEL JWT HACKER
# ===============================

try:
    jwt.decode(jwt_hacker, clave, algorithms=["HS256"])
    print("JWT del hacker validado (NO debería pasar)")
except Exception as e:
    print("JWT del hacker rechazado:", e)
