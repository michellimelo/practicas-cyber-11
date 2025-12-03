# ============================================
# RETO 1 – XOR, BASE64 y HEX
# ============================================

from base64 import b64decode

# ============================================
# 1. CLAVE = XOR DE DOS COMPONENTES (HEX)
# ============================================

comp1_hex = "AFAA1232BCFF"
comp2_hex = "BCAA3332BCFA"

# Pasar de hex → enteros
comp1_int = int(comp1_hex, 16)
comp2_int = int(comp2_hex, 16)

# XOR bit a bit
comp3_int = comp1_int ^ comp2_int

# Resultado en hexadecimal (sin 0x, en mayúsculas)
comp3_hex = hex(comp3_int)[2:].upper()

print("=== XOR DE COMPONENTES ===")
print("Componente 1 (hex):", comp1_hex)
print("Componente 2 (hex):", comp2_hex)
print("Componente 3 = XOR (hex):", comp3_hex)
print()

# ============================================
# 2. DECODIFICAR BASE64 Y OBTENER HEX
# ============================================

cadena_b64 = "Vml2YSBLZWVwQ29kaW5n"

# Base64 → bytes
cadena_bytes = b64decode(cadena_b64)

# Mostrar texto en claro
cadena_texto = cadena_bytes.decode("utf-8")

# Mostrar también en hexadecimal
cadena_hex = cadena_bytes.hex().upper()

print("=== BASE64 → TEXTO + HEX ===")
print("Cadena Base64   :", cadena_b64)
print("Texto en claro  :", cadena_texto)
print("Texto en HEX    :", cadena_hex)
print()

# ============================================
# 3. CODIFICAR TEXTO A HEX
# ============================================

texto_original = "Viva KeepCoding"

# Texto → bytes (UTF-8)
texto_bytes = texto_original.encode("utf-8")

# Bytes → hex
texto_hex = texto_bytes.hex().upper()

print("=== TEXTO → HEX ===")
print("Texto original:", texto_original)
print("HEX obtenido  :", texto_hex)
