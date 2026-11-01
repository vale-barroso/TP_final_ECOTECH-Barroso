import re

UBICACION_POR_DEFECTO = "Sin ubicacion"


def limpiar_registro_sensor(registro_raw):
    """Devuelve un diccionario normalizado a partir de un registro crudo."""
    sensor_id = str(registro_raw.get("sensor_id", "")).strip()

    # busco el numero dentro del texto (ej: "24.5C" -> 24.5)
    texto_temp = str(registro_raw.get("temperatura", "")).strip()
    coincidencia = re.search(r"-?\d+(?:[.,]\d+)?", texto_temp)
    temperatura = None
    if coincidencia:
        temperatura = float(coincidencia.group().replace(",", "."))

    # si la clave falta, es None o viene vacia, uso el valor por defecto
    ubicacion = str(registro_raw.get("ubicacion") or "").strip()
    if not ubicacion:
        ubicacion = UBICACION_POR_DEFECTO

    return {"sensor_id": sensor_id, "temperatura": temperatura, "ubicacion": ubicacion}


def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):
    """Devuelve (ids_en_alerta, promedio_de_temperatura)."""
    ids_alerta = []
    temperaturas = []

    for sensor in lista_sensores_limpios:
        temp = sensor["temperatura"]
        if temp is None:  # lectura que no se pudo interpretar
            continue
        temperaturas.append(temp)
        if temp > umbral_temperatura:
            ids_alerta.append(sensor["sensor_id"])

    promedio = sum(temperaturas) / len(temperaturas) if temperaturas else 0.0
    return ids_alerta, promedio


if __name__ == "__main__":
    crudos = [
        {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": "SENSOR-002", "temperatura": " 31,2 C ", "ubicacion": "Planta Sur"},
        {"sensor_id": "  SENSOR-003", "temperatura": "40C"},
        {"sensor_id": "SENSOR-004 ", "temperatura": "28.0C", "ubicacion": "   "},
        {"sensor_id": "SENSOR-005", "temperatura": "error", "ubicacion": "Planta Este"},
    ]
    umbral = 30.0

    limpios = [limpiar_registro_sensor(r) for r in crudos]
    alertas, promedio = generar_resumen_sensores(limpios, umbral)

    print("=== REPORTE DE SENSORES - ECOTECH SOLUTIONS ===")
    for s in limpios:
        temp = f"{s['temperatura']:.1f} C" if s["temperatura"] is not None else "sin dato"
        print(f"{s['sensor_id']:<12} {temp:<10} {s['ubicacion']}")
    print(f"\nUmbral: {umbral:.1f} C")
    print(f"Sensores en alerta: {', '.join(alertas) if alertas else 'ninguno'}")
    print(f"Promedio global: {promedio:.2f} C")
