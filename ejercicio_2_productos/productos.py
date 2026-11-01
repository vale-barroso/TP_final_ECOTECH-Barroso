import json


class StockInvalidoError(Exception):
    """Se lanza cuando se intenta asignar un stock negativo."""


class DispositivoEcologico:
    def __init__(self, nombre, precio, stock):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock  # pasa por el setter, asi tambien se valida al crear

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, valor):
        if valor < 0:
            raise StockInvalidoError(
                f"El stock de '{self.nombre}' no puede ser negativo (recibido: {valor})"
            )
        self._stock = valor

    def ficha_tecnica(self):
        return f"{self.nombre} | Precio: ${self.precio:.2f} | Stock: {self.stock} u."

    def a_diccionario(self):
        return {
            "tipo": type(self).__name__,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
        }


class PanelSolar(DispositivoEcologico):
    def __init__(self, nombre, precio, stock, potencia_w, eficiencia):
        super().__init__(nombre, precio, stock)
        self.potencia_w = potencia_w
        self.eficiencia = eficiencia  # porcentaje

    def ficha_tecnica(self):
        base = super().ficha_tecnica()
        return f"[PANEL SOLAR] {base} | {self.potencia_w} W | Eficiencia: {self.eficiencia}%"

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["potencia_w"] = self.potencia_w
        datos["eficiencia"] = self.eficiencia
        return datos


class GestorInventario:
    def guardar_catalogo_json(self, lista_dispositivos, ruta_archivo):
        datos = [d.a_diccionario() for d in lista_dispositivos]
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    catalogo = []

    # intento de crear un producto con stock erroneo
    try:
        malo = PanelSolar("Panel Defectuoso", 150.0, -5, 300, 18.5)
        catalogo.append(malo)
    except StockInvalidoError as error:
        print("Error capturado:", error)

    # tambien al modificar el stock de uno ya creado
    panel = PanelSolar("Panel Monocristalino 450W", 320.0, 12, 450, 21.3)
    try:
        panel.stock = -1
    except StockInvalidoError as error:
        print("Error capturado:", error)

    catalogo.append(panel)
    catalogo.append(PanelSolar("Panel Policristalino 280W", 180.5, 30, 280, 16.8))
    catalogo.append(DispositivoEcologico("Cargador Solar Portatil", 45.9, 50))

    for d in catalogo:
        print(d.ficha_tecnica())

    GestorInventario().guardar_catalogo_json(catalogo, "catalogo_ecotech.json")
    print(f"\nSe exportaron {len(catalogo)} productos a catalogo_ecotech.json")
