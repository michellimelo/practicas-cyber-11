# ============================================
# 1. XOR PARA RECONSTRUIR CLAVES
# ============================================

# XOR de datos binarios
def xor_data(binary_data_1, binary_data_2):
    return bytes([b1 ^ b2 for b1, b2 in zip(binary_data_1, binary_data_2)])

# XOR de bytes
def xor_data(data1, data2):
    return bytes([b1 ^ b2 for b1, b2 in zip(data1, data2)])

#-----------------------------------------------------------------------------------------

# Escenario 1: desarrollo
clave_fija_codigo = bytes.fromhex("B1EF2ACFE2BAEEFF")
clave_final_memoria = bytes.fromhex("91BA13BA21AABB12")

parte_properties_desarrollo = xor_data(clave_fija_codigo, clave_final_memoria)

print("Parte dinámica (properties) en desarrollo:", parte_properties_desarrollo.hex())

#-----------------------------------------------------------------------------------------

# Escenario 2: producción
parte_properties_produccion = bytes.fromhex("B98A15BA31AEBB3F")
clave_final_produccion = xor_data(clave_fija_codigo, parte_properties_produccion)

print("Clave final obtenida en producción:", clave_final_produccion.hex())
