#XOR de datos binarios
def xor_data(binary_data_1, binary_data_2):
    return bytes([b1 ^ b2 for b1, b2 in zip(binary_data_1, binary_data_2)])


# ============================================================
# Función auxiliar para aplicar XOR entre dos secuencias de bytes
# ============================================================
# XOR se aplica byte a byte. Es reversible:
#   A XOR B = C
#   C XOR A = B
#   C XOR B = A
# Esto permite separar una clave en dos mitades sin revelar
# directamente la clave final completa.
def xor_data(data1, data2):
    return bytes([b1 ^ b2 for b1, b2 in zip(data1, data2)])


# ============================================================
# ESCENARIO 1: ENTORNO DE DESARROLLO
# ============================================================
# Tenemos:
#   - clave_fija_codigo: valor incrustado en el código fuente
#   - clave_final_memoria: la clave real con la que opera el sistema
#
# Queremos averiguar:
#   - parte_properties: valor que el Key Manager debe colocar en el fichero
#
# Recordar:
#   clave_final = clave_fija_codigo XOR parte_properties
# Por tanto:
#   parte_properties = clave_fija_codigo XOR clave_final
# ============================================================

clave_fija_codigo = bytes.fromhex("B1EF2ACFE2BAEEFF")
clave_final_memoria = bytes.fromhex("91BA13BA21AABB12")

parte_properties_desarrollo = xor_data(clave_fija_codigo, clave_final_memoria)

print("Parte dinámica (properties) en desarrollo:", parte_properties_desarrollo.hex())


# ============================================================
# ESCENARIO 2: ENTORNO DE PRODUCCIÓN
# ============================================================
# Tenemos:
#   - clave_fija_codigo: misma clave que en desarrollo
#   - parte_properties_produccion: valor dinámico que está escrito en el properties
#
# Queremos averiguar:
#   - clave_final_produccion: la clave real que se obtiene en memoria
#
# Recordar:
#   clave_final = clave_fija_codigo XOR parte_properties
# ============================================================

parte_properties_produccion = bytes.fromhex("B98A15BA31AEBB3F")

clave_final_produccion = xor_data(clave_fija_codigo, parte_properties_produccion)

print("Clave final obtenida en producción:", clave_final_produccion.hex())
