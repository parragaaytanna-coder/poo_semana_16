from datetime import date
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta

class RestauranteServicio:
    def __init__(self, archivo_servicio):
        self.archivo_servicio = archivo_servicio
        self.usuarios = []
        self.productos = []
        self.ventas = []
        self.cargar_datos()

    def cargar_datos(self):
        """Carga los datos persistidos desde los archivos JSON y los convierte en objetos."""
        usuarios_json = self.archivo_servicio.leer_json("usuarios.json")
        productos_json = self.archivo_servicio.leer_json("productos.json")
        ventas_json = self.archivo_servicio.leer_json("ventas.json")

        self.usuarios = [Usuario.desde_diccionario(datos) for datos in usuarios_json]
        self.productos = [Producto.desde_diccionario(datos) for datos in productos_json]
        self.ventas = [Venta.desde_diccionario(datos) for datos in ventas_json]

    # --- Métodos de Persistencia ---

    def guardar_usuarios(self):
        datos = [usuario.a_diccionario() for usuario in self.usuarios]
        self.archivo_servicio.escribir_json("usuarios.json", datos)

    def guardar_productos(self):
        datos = [producto.a_diccionario() for producto in self.productos]
        self.archivo_servicio.escribir_json("productos.json", datos)

    def guardar_ventas(self):
        datos = [venta.a_diccionario() for venta in self.ventas]
        self.archivo_servicio.escribir_json("ventas.json", datos)

    # --- Autenticación y Consultas Básicas ---

    def validar_acceso(self, usuario, contrasena):
        """Verifica las credenciales en el inicio de sesión."""
        for u in self.usuarios:
            if u.usuario == usuario and u.contrasena == contrasena:
                return u
        return None

    def cantidad_usuarios(self):
        return len(self.usuarios)

    def cantidad_productos(self):
        return len(self.productos)

    def cantidad_ventas(self):
        return len(self.ventas)

    def listar_usuarios(self):
        return self.usuarios

    def listar_productos(self):
        return self.productos

    def listar_ventas(self):
        return self.ventas

    # --- Buscadores por Código e Identificador ---

    def buscar_producto_por_codigo(self, codigo):
        codigo = str(codigo).strip()
        for producto in self.productos:
            if producto.codigo == codigo:
                return producto
        return None

    def buscar_usuario_por_identificador(self, identificador):
        identificador = str(identificador).strip()
        for usuario in self.usuarios:
            if usuario.identificador == identificador:
                return usuario
        return None

    def buscar_usuario_por_nombre_usuario(self, nombre_usuario):
        nombre_usuario = str(nombre_usuario).strip()
        for usuario in self.usuarios:
            if usuario.usuario == nombre_usuario:
                return usuario
        return None

    # --- Gestión de Productos ---

    def registrar_producto(self, codigo, nombre, categoria, precio, stock):
        nuevo_producto = Producto(codigo, nombre, categoria, precio, stock)
        if self.buscar_producto_por_codigo(nuevo_producto.codigo) is not None:
            raise ValueError("Ya existe un producto con ese código.")
        self.productos.append(nuevo_producto)
        self.guardar_productos()
        return nuevo_producto

    def actualizar_producto(self, codigo, nombre, categoria, precio, stock):
        producto_actual = self.buscar_producto_por_codigo(codigo)
        if producto_actual is None:
            raise ValueError("No existe un producto con ese código.")
        datos_validados = Producto(codigo, nombre, categoria, precio, stock)
        producto_actual.nombre = datos_validados.nombre
        producto_actual.categoria = datos_validados.categoria
        producto_actual.precio = datos_validados.precio
        producto_actual.stock = datos_validados.stock
        self.guardar_productos()
        return producto_actual

    def eliminar_producto(self, codigo):
        producto_actual = self.buscar_producto_por_codigo(codigo)
        if producto_actual is None:
            raise ValueError("No existe un producto con ese código.")
        self.productos.remove(producto_actual)
        self.guardar_productos()
        return producto_actual

    # --- Gestión de Usuarios (Semana 16) ---

    def registrar_usuario(self, identificador, nombre, usuario, contrasena, rol):
        nuevo_usuario = Usuario(identificador, nombre, usuario, contrasena, rol)
        if self.buscar_usuario_por_identificador(nuevo_usuario.identificador) is not None:
            raise ValueError("Ya existe un usuario con ese identificador.")
        if self.buscar_usuario_por_nombre_usuario(nuevo_usuario.usuario) is not None:
            raise ValueError("Ya existe otro usuario con ese nombre de usuario.")
        self.usuarios.append(nuevo_usuario)
        self.guardar_usuarios()
        return nuevo_usuario

    def actualizar_usuario(self, identificador, nombre, usuario, contrasena, rol, identificador_usuario_actual=None):
        usuario_actual = self.buscar_usuario_por_identificador(identificador)
        if usuario_actual is None:
            raise ValueError("No existe un usuario con ese identificador.")
        
        datos_validados = Usuario(identificador, nombre, usuario, contrasena, rol)
        
        # Validar duplicados de nombre de usuario en otro registro
        usuario_con_mismo_login = self.buscar_usuario_por_nombre_usuario(datos_validados.usuario)
        if usuario_con_mismo_login is not None and usuario_con_mismo_login.identificador != usuario_actual.identificador:
            raise ValueError("Ya existe otro usuario con ese nombre de usuario.")

        # Regla de seguridad: Impedir que un admin se quite el rol a sí mismo
        if identificador_usuario_actual == usuario_actual.identificador and usuario_actual.rol == "Administrador" and datos_validados.rol != "Administrador":
            raise ValueError("No puede cambiar el rol del administrador actualmente autenticado.")

        usuario_actual.nombre = datos_validados.nombre
        usuario_actual.usuario = datos_validados.usuario
        usuario_actual.contrasena = datos_validados.contrasena
        usuario_actual.rol = datos_validados.rol
        self.guardar_usuarios()
        return usuario_actual

    def eliminar_usuario(self, identificador, identificador_usuario_actual=None):
        usuario_actual = self.buscar_usuario_por_identificador(identificador)
        if usuario_actual is None:
            raise ValueError("No existe un usuario con ese identificador.")
        if usuario_actual.identificador == identificador_usuario_actual:
            raise ValueError("No puede eliminar la cuenta del usuario actualmente autenticado.")
        
        self.usuarios.remove(usuario_actual)
        self.guardar_usuarios()
        return usuario_actual

    # --- Gestión de Ventas ---

    def generar_identificador_venta(self):
        siguiente = len(self.ventas) + 1
        return f"V{siguiente:03d}"

    def registrar_venta(self, usuario_id, producto_codigo):
        usuario_id = str(usuario_id).strip()
        producto_codigo = str(producto_codigo).strip()

        if not usuario_id:
            raise ValueError("Debe seleccionar un usuario.")
        if not producto_codigo:
            raise ValueError("Debe seleccionar un producto.")

        usuario = self.buscar_usuario_por_identificador(usuario_id)
        if usuario is None:
            raise ValueError("El usuario seleccionado no existe.")

        producto = self.buscar_producto_por_codigo(producto_codigo)
        if producto is None:
            raise ValueError("El producto seleccionado no existe.")

        if producto.stock <= 0:
            raise ValueError("No hay stock suficiente para realizar la venta de este producto.")

        # Descuenta stock y genera la venta
        producto.stock -= 1
        self.guardar_productos()

        nueva_venta = Venta(
            identificador=self.generar_identificador_venta(),
            usuario_id=usuario.identificador,
            producto_codigo=producto.codigo,
            fecha=date.today().strftime("%d/%m/%Y")
        )

        self.ventas.append(nueva_venta)
        self.guardar_ventas()
        return nueva_venta