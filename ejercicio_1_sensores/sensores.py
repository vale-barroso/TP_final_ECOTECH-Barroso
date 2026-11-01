UBICACION_POR_DEFECTO = "Área No Asignada"


def limpiar_registro_sensor(registro_raw):
    """Recibe un diccionario crudo y devuelve uno nuevo, estandarizado."""
    limpio = {}

    # 1. ID sin espacios sobrantes
    limpio["sensor_id"] = str(registro_raw.get("sensor_id", "")).strip()

    # 2. Temperatura como float
    temperatura = registro_raw.get("temperatura", 0.0)
    if isinstance(temperatura, (int, float)):
        limpio["temperatura"] = float(temperatura)
    else:
        texto = (
            str(temperatura)
            .upper()
            .replace("C", "")
            .replace("F", "")
            .replace("°", "")
            .replace(" ", "")
            .replace(",", ".")
        )
        try:
            limpio["temperatura"] = float(texto)
        except ValueError:
            limpio["temperatura"] = 0.0  # valor seguro si el texto esta corrupto

    # 3. Ubicacion con valor por defecto
    ubicacion = registro_raw.get("ubicacion")
    if isinstance(ubicacion, str) and ubicacion.strip():
        limpio["ubicacion"] = ubicacion.strip()
    else:
        limpio["ubicacion"] = UBICACION_POR_DEFECTO

    return limpio


def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):
    """Devuelve la tupla (lista_sensores_alerta, promedio_temperatura)."""
    # clausula de guarda: evita la division por cero
    if not lista_sensores_limpios:
        return [], 0.0

    suma = 0.0
    alertas = []

    for sensor in lista_sensores_limpios:
        suma += sensor["temperatura"]
        if sensor["temperatura"] > umbral_temperatura:
            alertas.append(sensor["sensor_id"])

    promedio = round(suma / len(lista_sensores_limpios), 2)
    return alertas, promedio


if __name__ == "__main__":
    crudos = [
        {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": "SENSOR-002", "temperatura": "35.0 C", "ubicacion": "Planta Sur"},
        {"sensor_id": "  SENSOR-003", "temperatura": "31.2°C"},
        {"sensor_id": "SENSOR-004 ", "temperatura": 28, "ubicacion": "   "},
        {"sensor_id": "SENSOR-005", "temperatura": "error", "ubicacion": ""},
    ]
    umbral = 30.0

    limpios = [limpiar_registro_sensor(r) for r in crudos]
    alertas, promedio = generar_resumen_sensores(limpios, umbral)

    print("=== REPORTE DE SENSORES - ECOTECH SOLUTIONS ===")
    for s in limpios:
        print(f"{s['sensor_id']:<12} {s['temperatura']:>5.1f} C   {s['ubicacion']}")
    print(f"\nUmbral de alerta: {umbral} C")
    print(f"Sensores en alerta: {alertas}")
    print(f"Promedio térmico global: {promedio} C")
