# TP Final - EcoTech Solutions

Autora: Valentina Barroso

## Ejercicios

- `ejercicio_1_sensores/`: limpieza y resumen de lecturas de sensores.
  Ejecutar: `python sensores.py`
- `ejercicio_2_productos/`: catálogo de productos con excepción personalizada y persistencia en JSON.
  Ejecutar: `python productos.py` (genera `catalogo_ecotech.json`)
- `ejercicio_3_auditoria_web/`: tests unitarios del cálculo de emisiones y panel web en Django.
  Ejecutar los tests: `python -m unittest -v`

## Ver el panel web (ejercicio 3)

Requiere Django: `pip install django`

Desde la carpeta `ejercicio_3_auditoria_web/`:

    python ver_panel.py

Luego abrir en el navegador: http://127.0.0.1:8000/

Para detener el servidor: Ctrl + C.