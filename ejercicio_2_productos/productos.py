import json


class StockInvalidoError(Exception):
    def __init__(self, mensaje="El stock no puede ser un valor negativo."):
        super().__init__(mensaje)


class DispositivoEcologico:
    def __init__(self, id_producto, nombre, precio, stock):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = precio
        self._stock = 0
        self.stock = stock  # usa el setter, asi se valida desde la creacion

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, valor):
        if valor < 0:
            raise StockInvalidoError(
                f"Stock inválido para '{self.nombre}': se intentó asignar {valor}"
            )
        self._stock = valor

    def generar_ficha_tecnica(self):
        return {
            "ID": self.id_producto,
            "Nombre": self.nombre,
            "Precio": f"${self.precio:.2f}",
            "Stock": self.stock,
        }

    def a_diccionario(self):
        """Version con valores numericos, pensada para guardar en JSON."""
        return {
            "tipo": type(self).__name__,
            "id_producto": self.id_producto,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
        }


class PanelSolar(DispositivoEcologico):
    def __init__(self, id_producto, nombre, precio, stock, eficiencia, potencia_w):
        super().__init__(id_producto, nombre, precio, stock)
        self.eficiencia = eficiencia
        self.potencia_w = potencia_w

    def generar_ficha_tecnica(self):
        ficha = super().generar_ficha_tecnica()
        ficha.update({
            "Tipo": "Panel Solar",
            "Potencia": f"{self.potencia_w} W",
            "Eficiencia": f"{self.eficiencia}%",
        })
        return ficha

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["eficiencia"] = self.eficiencia
        datos["potencia_w"] = self.potencia_w
        return datos


class GestorInventario:
    def guardar_catalogo_json(self, lista_dispositivos, ruta_archivo):
        datos = [d.a_diccionario() for d in lista_dispositivos]
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    catalogo = []

    panel = PanelSolar("PS-001", "Panel Monocristalino 450W", 320.0, 12, 21.3, 450)
    print("Ficha técnica del panel:")
    print(panel.generar_ficha_tecnica())
    catalogo.append(panel)

    # intento intencional de asignar stock negativo a un objeto existente
    try:
        panel.stock = -5
    except StockInvalidoError as error:
        print("\nAdvertencia controlada:", error)

    # intento de crear un producto directamente con stock invalido
    try:
        defectuoso = PanelSolar("PS-999", "Panel Defectuoso", 150.0, -3, 18.0, 300)
        catalogo.append(defectuoso)
    except StockInvalidoError as error:
        print("Advertencia controlada:", error)

    catalogo.append(PanelSolar("PS-002", "Panel Policristalino 280W", 180.5, 30, 16.8, 280))
    catalogo.append(DispositivoEcologico("CS-001", "Cargador Solar Portatil", 45.9, 50))

    print(f"\nStock del panel sigue en: {panel.stock}")

    GestorInventario().guardar_catalogo_json(catalogo, "catalogo_ecotech.json")
    print(f"Se exportaron {len(catalogo)} productos válidos a catalogo_ecotech.json")
