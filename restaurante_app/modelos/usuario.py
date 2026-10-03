class Usuario:
    ROLES_PERMITIDOS = ("Administrador", "Empleado", "Cliente")

    def __init__(self, identificador, nombre, usuario, contrasena, rol):
        self.identificador = identificador
        self.nombre = nombre
        self.usuario = usuario
        self.contrasena = contrasena
        self.rol = rol

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
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = self.validar_texto(valor, "nombre")

    @property
    def usuario(self):
        return self._usuario

    @usuario.setter
    def usuario(self, valor):
        self._usuario = self.validar_texto(valor, "usuario")

    @property
    def contrasena(self):
        return self._contrasena

    @contrasena.setter
    def contrasena(self, valor):
        self._contrasena = self.validar_texto(valor, "contraseña")

    @property
    def rol(self):
        return self._rol

    @rol.setter
    def rol(self, valor):
        rol_validado = self.validar_texto(valor, "rol")
        if rol_validado not in self.ROLES_PERMITIDOS:
            raise ValueError(f"El rol '{rol_validado}' no es válido. Debe ser uno de: {', '.join(self.ROLES_PERMITIDOS)}")
        self._rol = rol_validado

    def a_diccionario(self):
        """Convierte la instancia a diccionario para guardarla en usuarios.json."""
        return {
            "identificador": self.identificador,
            "nombre": self.nombre,
            "usuario": self.usuario,
            "contraseña": self.contrasena,
            "rol": self.rol
        }

    @classmethod
    def desde_diccionario(cls, datos):
        """Crea una instancia de Usuario a partir de un diccionario cargado del JSON."""
        return cls(
            identificador=datos.get("identificador"),
            nombre=datos.get("nombre"),
            usuario=datos.get("usuario"),
            contrasena=datos.get("contraseña") or datos.get("contrasena"),
            rol=datos.get("rol", "Cliente")
        )