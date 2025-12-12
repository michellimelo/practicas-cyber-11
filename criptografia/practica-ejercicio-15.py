import re

# 1 Bloque TR-31 y KBPK

tr31_block = "D0144D0AB00S000042766B9265B2DF93AE6E29B58135B77A2F616C8D515ACDBE6A5626F79FA7B4071E9EE1423C6D7970FA2B965D18B23922B5B2E5657495E03CD857FD37018E111B"

kbpk = bytes.fromhex("A1A10101010101010101010101010102")

tr31_hex = re.sub(r"\s+", "", tr31_block).upper()

#-----------------------------------------------------------------------------------------

# 2) Cabecera fija (16 caracteres)

header = tr31_hex[:16]

version = header[0:1]
length  = header[1:5]
usage   = header[5:7]
alg     = header[7:8]
mode    = header[8:9]
kver    = header[9:11]
export  = header[11:12]

print("VERSION:", version)
print("LENGTH :", length)
print("USAGE  :", usage)
print("ALG    :", alg)
print("MODE   :", mode)
print("KVER   :", kver)
print("EXPORT :", export)
print("--------------------------------------------------")
