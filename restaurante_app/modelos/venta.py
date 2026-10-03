class Venta:
    def __init__(self, identificador, usuario_id, producto_codigo, fecha):
        self.identificador = identificador
        self.usuario_id = usuario_id
        self.producto_codigo = producto_codigo
        self.fecha = fecha

    @staticmethod
    def validar_texto(valor, campo):
        """Valida que los campos de texto no estén vacíos."""
        if not valor or not str(valor).strip():
            raise ValueError(f"El campo {campo} no puede estar vacío.")
        return str(valor).strip()

    # --- Encapsulamiento con Getters y Setters ---

    @property
    def identificador(self):
        return self._identificador

    @identificador.setter
    def identificador(self, valor):
        self._identificador = self.validar_texto(valor, "identificador")

    @property
    def usuario_id(self):
        return self._usuario_id

    @usuario_id.setter
    def usuario_id(self, valor):
        self._usuario_id = self.validar_texto(valor, "usuario_id")

    @property
    def producto_codigo(self):
        return self._producto_codigo

    @producto_codigo.setter
    def producto_codigo(self, valor):
        self._producto_codigo = self.validar_texto(valor, "producto_codigo")

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, valor):
        self._fecha = self.validar_texto(valor, "fecha")

    def a_diccionario(self):
        """Convierte la instancia a diccionario para guardarla en ventas.json."""
        return {
            "identificador": self.identificador,
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "fecha": self.fecha
        }

    @classmethod
    def desde_diccionario(cls, datos):
        """Crea una instancia de Venta a partir de un diccionario cargado del JSON."""
        return cls(
            identificador=datos.get("identificador"),
            usuario_id=datos.get("usuario_id"),
            producto_codigo=datos.get("producto_codigo") or datos.get("libro_codigo"),
            fecha=datos.get("fecha")
        )