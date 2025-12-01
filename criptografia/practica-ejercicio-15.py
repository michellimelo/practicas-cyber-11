from psec import tr31

#Documentado en este fichero
#https://github.com/knovichikhin/psec/blob/master/psec/tr31.py

header, key = tr31.unwrap( kbpk=bytes.fromhex("A1A10101010101010101010101010102"), key_block="D0144D0AB00S000042766B9265B2DF93AE6E29B58135B77A2F616C8D515ACDBE6A5626F79FA7B4071E9EE1423C6D7970FA2B965D18B23922B5B2E5657495E03CD857FD37018E111B")
print(key.hex())

print("Key Version ID: " + header.version_id )
print("Algoritmo: " + header.algorithm)
print("Modo de uso: " + header.mode_of_use)
print("Uso de la clave: " + header.key_usage)
print("Exportabilidad: " + header.exportability)


# ============================================================
# RESPUESTAS DEL EJERCICIO TR-31
# ============================================================
# 1. Algoritmo que protege el bloque:
#    El bloque TR-31 versión D está protegido mediante AES
#    según el esquema de protección definido en TR-31/ISO 20038.
#
# 2. Algoritmo para el que se ha definido la clave:
#    Campo 'A' → clave definida para AES.
#
# 3. Modo de uso:
#    Campo 'B' → Both (la clave puede cifrar y descifrar).
#
# 4. Exportabilidad de la clave:
#    Campo 'S' → clave sensible, exportable bajo cualquier KEK.
#
# 5. Uso de la clave:
#    Campo 'D0' → clave simétrica para cifrado de datos.
#
# 6. Valor de la clave obtenida:
#    key = c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1
# ============================================================
