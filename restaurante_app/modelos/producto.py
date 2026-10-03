class Producto:
    def __init__(self, codigo, nombre, categoria, precio, stock):
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock

    @staticmethod
    def validar_texto(valor, campo):
        """Valida que los campos de texto no estén vacíos."""
        if not valor or not str(valor).strip():
            raise ValueError(f"El campo {campo} no puede estar vacío.")
        return str(valor).strip()

    @staticmethod
    def validar_numero_positivo(valor, campo):
        """Valida que los valores numéricos sean válidos y mayores o iguales a cero."""
        try:
            val_num = float(valor)
            if val_num < 0:
                raise ValueError(f"El campo {campo} no puede ser negativo.")
            return val_num
        except (ValueError, TypeError):
            raise ValueError(f"El campo {campo} debe ser un número válido.")

    # --- Encapsulamiento con Getters y Setters ---

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        self._codigo = self.validar_texto(valor, "código")

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = self.validar_texto(valor, "nombre")

    @property
    def categoria(self):
        return self._categoria

    @categoria.setter
    def categoria(self, valor):
        self._categoria = self.validar_texto(valor, "categoría")

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        self._precio = self.validar_numero_positivo(valor, "precio")

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, valor):
        val_num = self.validar_numero_positivo(valor, "stock")
        self._stock = int(val_num)

    def a_diccionario(self):
        """Convierte el objeto a un diccionario para guardarlo en productos.json."""
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock
        }

    @classmethod
    def desde_diccionario(cls, datos):
        """Crea una instancia de Producto desde un diccionario cargado de JSON."""
        return cls(
            codigo=datos.get("codigo"),
            nombre=datos.get("nombre"),
            categoria=datos.get("categoria"),
            precio=datos.get("precio", 0.0),
            stock=datos.get("stock", 0)
        )