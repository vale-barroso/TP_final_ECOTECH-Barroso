from django.shortcuts import render

from emisiones import obtener_metricas_consumo

# datos de prueba inventados
HISTORIAL_CONSUMOS = [
    {"planta": "Planta Norte", "consumo_kwh": 1500},
    {"planta": "Planta Sur", "consumo_kwh": 2300.5},
    {"planta": "Planta Este", "consumo_kwh": 980},
    {"planta": "Planta Oeste", "consumo_kwh": 1750},
]


def vista_panel_sustentabilidad(request):
    metricas = obtener_metricas_consumo(HISTORIAL_CONSUMOS)
    contexto = {
        "registros": HISTORIAL_CONSUMOS,
        "total_emisiones": metricas["total_emisiones"],
        "planta_mayor_consumo": metricas["planta_mayor_consumo"],
        "consumo_maximo": metricas["consumo_maximo"],
    }
    return render(request, "sustentabilidad/panel.html", contexto)
