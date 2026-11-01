def calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4):
    if consumo_kwh < 0:
        raise ValueError("El consumo no puede ser negativo")
    return consumo_kwh * factor_emision


def obtener_metricas_consumo(registros):
    """registros: lista de dicts con 'planta' y 'consumo_kwh'."""
    total_emisiones = 0.0
    planta_mayor = None
    mayor_consumo = -1

    for reg in registros:
        total_emisiones += calcular_emisiones_carbono(reg["consumo_kwh"])
        if reg["consumo_kwh"] > mayor_consumo:
            mayor_consumo = reg["consumo_kwh"]
            planta_mayor = reg["planta"]

    return {
        "total_emisiones": round(total_emisiones, 2),
        "planta_mayor_consumo": planta_mayor,
        "consumo_maximo": mayor_consumo if planta_mayor else 0,
    }
