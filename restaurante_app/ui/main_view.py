import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk


class MainView(tk.Frame):

  def __init__(self, master, usuario_actual, restaurante_servicio, al_cerrar_sesion):
        super().__init__(master, bg='#f7fafc')
        self.usuario_actual = usuario_actual
        self.restaurante_servicio = restaurante_servicio
        self.al_cerrar_sesion = al_cerrar_sesion
        self.contenido = None
        self.etiqueta_estado = None
        self.botones_menu = {}
        self.iconos = {}

    # Referencias a widgets de formularios
        self.producto_codigo_entry = None
        self.producto_nombre_entry = None
        self.producto_categoria_entry = None
        self.producto_precio_entry = None
        self.producto_stock_entry = None
        self.tabla_productos = None

        self.usuario_identificador_entry = None
        self.usuario_nombre_entry = None
        self.usuario_login_entry = None
        self.usuario_contrasena_entry = None
        self.usuario_rol_combo = None
        self.usuario_rol_estado = None
        self.usuario_identificador_seleccionado = None
        self.tabla_usuarios = None

        self.usuario_venta_combo = None
        self.producto_venta_combo = None
        self.tabla_ventas = None
        self.opciones_usuarios_venta = {}
        self.opciones_productos_venta = {}

        self.definir_estilos()
        self.construir_interfaz()

  def definir_estilos(self):
    """Configura la identidad visual y estilos de los componentes."""
    self.color_fondo = '#f7fafc'
    self.color_panel = '#ffffff'
    self.color_encabezado = '#1f2a44'  # Azul oscuro sidebar
    self.color_texto = '#243447'
    self.color_secundario = '#dbeafe'  # Azul muy claro (barra estado)
    self.color_resaltado = '#2563eb'  # Azul botón acción

    estilo = ttk.Style()
    estilo.theme_use('clam')

    # Estilos de botones del menú lateral
    estilo.configure(
        'MenuApp.TButton',
        background='#334155',  # Gris azulado oscuro
        foreground='#ffffff',
        font=('Arial', 10, 'bold'),
        padding=(12, 10),
        borderwidth=0,
        anchor='w',
    )
    estilo.map('MenuApp.TButton', background=[('active', '#475569')])

    estilo.configure(
        'MenuActivo.TButton',
        background=self.color_resaltado,
        foreground='#ffffff',
        font=('Arial', 10, 'bold'),
        padding=(12, 10),
        borderwidth=0,
        anchor='w',
    )
    estilo.map('MenuActivo.TButton', background=[('active', '#1d4ed8')])

    # Estilos de botones de acción en formularios
    estilo.configure(
        'Secundario.TButton',
        background='#1f2a44',
        foreground='#ffffff',
        font=('Arial', 10, 'bold'),
        padding=(10, 7),
        borderwidth=0,
    )
    estilo.map('Secundario.TButton', background=[('active', '#334155')])

    estilo.configure(
        'Accion.TButton',
        background=self.color_resaltado,
        foreground='#ffffff',
        font=('Arial', 10, 'bold'),
        padding=(10, 7),
        borderwidth=0,
    )
    estilo.map('Accion.TButton', background=[('active', '#1d4ed8')])

    estilo.configure(
        'Eliminar.TButton',
        background='#e11d48',  # Rojo
        foreground='#ffffff',
        font=('Arial', 10, 'bold'),
        padding=(10, 7),
        borderwidth=0,
    )
    estilo.map('Eliminar.TButton', background=[('active', '#be123c')])

    # Estilo de encabezados de tabla
    estilo.configure(
        'Treeview.Heading',
        background=self.color_secundario,
        foreground=self.color_encabezado,
        font=('Arial', 10, 'bold'),
    )

  def cargar_icono(self, nombre_archivo):
        """Carga un ícono en Tkinter nativo ajustando según su tamaño original."""
        ruta_base = Path(__file__).resolve().parent.parent
        ruta_icono = ruta_base / 'assets' / 'icons' / nombre_archivo

        if not ruta_icono.exists():
            print(f"⚠️ [ADVERTENCIA] No se encontró el ícono en: {ruta_icono}")
            return None

        try:
            icono_original = tk.PhotoImage(file=str(ruta_icono))
            
            # Obtener el ancho de la imagen cargada
            ancho = icono_original.width()

            # Si la imagen es grande (ej. mayor a 64px), la achicamos
            if ancho > 64:
                factor = int(ancho / 24)  # Calcula cuánto achicar para que quede cercano a 24px
                icono_final = icono_original.subsample(factor, factor)
            else:
                icono_final = icono_original  # Si ya es pequeña, la dejamos intacta

            if not hasattr(self, 'iconos'):
                self.iconos = {}

            self.iconos[nombre_archivo] = icono_final
            return icono_final
        except Exception as e:
            print(f"❌ Error al procesar {nombre_archivo}: {e}")
            return None

  def crear_boton(self, contenedor, texto, comando, estilo, icono=None):
    """Utility para crear botones con ícono opcional y estilo."""
    imagen = self.cargar_icono(icono) if icono else None
    if imagen is not None:
      boton = ttk.Button(
          contenedor,
          text=texto,
          command=comando,
          style=estilo,
          image=imagen,
          compound='left',
      )
    else:
      boton = ttk.Button(contenedor, text=texto, command=comando, style=estilo)
    return boton

  def construir_interfaz(self):
    """Construye la estructura principal de la interfaz (sidebar + contenido)."""
    # Sidebar lateral
    frame_sidebar = tk.Frame(
        self, bg=self.color_encabezado, width=190, padx=16, pady=18
    )
    frame_sidebar.pack(side='left', fill='y')
    frame_sidebar.pack_propagate(False)

    # Título de la App en el sidebar
    tk.Label(
        frame_sidebar,
        text='Food Droppy App',
        bg=self.color_encabezado,
        fg='#ffffff',
        font=('Arial', 13, 'bold'),
    ).pack(anchor='w', pady=(0, 8))

    # Nombre del usuario autenticado
    tk.Label(
        frame_sidebar,
        text=self.usuario_actual.nombre,
        bg=self.color_encabezado,
        fg='#dbeafe',
        font=('Arial', 10),
        wraplength=150,
        justify='left',
    ).pack(anchor='w', pady=(0, 24))

    # Botones de navegación principal
    self.crear_boton_menu(
        frame_sidebar, 'Inicio', self.mostrar_inicio, 'inicio.png'
    )

    # Restricción de rol (Semana 16): Solo admin gestiona usuarios
    if self.usuario_actual.rol == 'Administrador':
      self.crear_boton_menu(
          frame_sidebar, 'Usuarios', self.mostrar_usuarios, 'usuario.png'
      )

    self.crear_boton_menu(
        frame_sidebar, 'Productos', self.mostrar_productos, 'producto.png'
    )
    self.crear_boton_menu(
        frame_sidebar, 'Ventas', self.mostrar_ventas, 'venta.png'
    )

    # Espacio flexible y botón Cerrar sesión
    tk.Frame(frame_sidebar, bg=self.color_encabezado).pack(
        fill='both', expand=True
    )
    self.crear_boton(
        frame_sidebar,
        'Cerrar sesión',
        self.cerrar_sesion,
        'Eliminar.TButton',
        'salida.png',
    ).pack(fill='x', pady=(16, 0))

    # Área de contenido principal
    frame_principal = tk.Frame(self, bg=self.color_fondo)
    frame_principal.pack(side='left', fill='both', expand=True)

    self.contenido = tk.Frame(
        frame_principal, bg=self.color_fondo, padx=28, pady=24
    )
    self.contenido.pack(fill='both', expand=True)

    # Barra de estado inferior
    barra_estado = tk.Frame(
        frame_principal, bg=self.color_secundario, padx=18, pady=8
    )
    barra_estado.pack(fill='x', side='bottom')
    self.etiqueta_estado = tk.Label(
        barra_estado,
        bg=self.color_secundario,
        fg=self.color_texto,
        font=('Arial', 10),
    )
    self.etiqueta_estado.pack(side='left')

    # Carga la vista inicial
    self.mostrar_inicio()

  def crear_boton_menu(self, contenedor, texto, comando, icono):
    """Crea y empaca un botón del menú lateral."""
    boton = self.crear_boton(contenedor, texto, comando, 'MenuApp.TButton', icono)
    boton.pack(fill='x', pady=(0, 8))
    self.botones_menu[texto] = boton

  def marcar_seccion(self, seccion):
    """Cambia el estilo del botón del menú lateral seleccionado."""
    for texto, boton in self.botones_menu.items():
      estilo = 'MenuActivo.TButton' if texto == seccion else 'MenuApp.TButton'
      boton.configure(style=estilo)

  def limpiar_contenido(self):
    """Elimina todos los widgets del panel de contenido central."""
    assert self.contenido is not None
    for widget in self.contenido.winfo_children():
      widget.destroy()

  def actualizar_barra_estado(self):
    """Refresca las cantidades en la barra de estado inferior."""
    assert self.etiqueta_estado is not None
    self.etiqueta_estado.config(
        text=(
            f'Productos: {self.restaurante_servicio.cantidad_productos()} | '
            f'Usuarios: {self.restaurante_servicio.cantidad_usuarios()} | '
            f'Ventas: {self.restaurante_servicio.cantidad_ventas()} | '
            'Datos JSON locales'
        )
    )

  # -------------------------------------------------------------------------
  # Inicio: Panel de bienvenida y resumen.
  # -------------------------------------------------------------------------
  def mostrar_inicio(self):
    self.marcar_seccion('Inicio')
    self.limpiar_contenido()
    self.actualizar_barra_estado()
    assert self.contenido is not None

    tk.Label(
        self.contenido,
        text='Panel principal',
        bg=self.color_fondo,
        fg=self.color_encabezado,
        font=('Arial', 20, 'bold'),
    ).pack(anchor='w', pady=(0, 8))

    tk.Label(
        self.contenido,
        text='Bienvenido/a al sistema de gestión de su restaurante.',
        bg=self.color_fondo,
        fg=self.color_texto,
        font=('Arial', 12),
    ).pack(anchor='w', pady=(0, 22))

    resumen = tk.Frame(self.contenido, bg=self.color_fondo)
    resumen.pack(fill='x')

    self.crear_tarjeta_resumen(
        resumen, 'Usuarios', self.restaurante_servicio.cantidad_usuarios()
    )
    self.crear_tarjeta_resumen(
        resumen, 'Productos', self.restaurante_servicio.cantidad_productos()
    )
    self.crear_tarjeta_resumen(
        resumen, 'Ventas', self.restaurante_servicio.cantidad_ventas()
    )

  def crear_tarjeta_resumen(self, contenedor, titulo, valor):
    """Crea una tarjeta visual para el resumen del panel de inicio."""
    tarjeta = tk.Frame(contenedor, bg=self.color_panel, padx=18, pady=16)
    tarjeta.pack(side='left', fill='x', expand=True, padx=(0, 14))

    tk.Label(
        tarjeta,
        text=titulo,
        bg=self.color_panel,
        fg=self.color_texto,
        font=('Arial', 10, 'bold'),
    ).pack(anchor='w')

    tk.Label(
        tarjeta,
        text=str(valor),
        bg=self.color_panel,
        fg=self.color_resaltado,
        font=('Arial', 24, 'bold'),
    ).pack(anchor='w', pady=(8, 0))

  # -------------------------------------------------------------------------
  # Usuarios (Semana 16): CRUD y Eventos (Table & Form).
  # -------------------------------------------------------------------------
  def mostrar_usuarios(self):
    # Control de acceso (Semana 16)
    if self.usuario_actual.rol != 'Administrador':
      messagebox.showerror(
          'Usuarios', 'Solo el administrador puede acceder a esta sección.'
      )
      return

    self.marcar_seccion('Usuarios')
    self.limpiar_contenido()
    assert self.contenido is not None
    self.crear_titulo_seccion('Gestión de usuarios')

    cuerpo = tk.Frame(self.contenido, bg=self.color_fondo)
    cuerpo.pack(fill='both', expand=True)
    cuerpo.grid_columnconfigure(1, weight=1)
    cuerpo.grid_rowconfigure(0, weight=1)

    # Formulario de Usuario
    formulario = tk.LabelFrame(
        cuerpo,
        text='Datos del usuario',
        bg=self.color_panel,
        fg=self.color_encabezado,
        font=('Arial', 10, 'bold'),
        padx=14,
        pady=14,
    )
    formulario.grid(row=0, column=0, sticky='n', padx=(0, 18))

    self.usuario_identificador_entry = self.crear_campo(
        formulario, 'Identificador', 0
    )
    self.usuario_nombre_entry = self.crear_campo(formulario, 'Nombre', 1)
    self.usuario_login_entry = self.crear_campo(formulario, 'Usuario', 2)
    self.usuario_contrasena_entry = self.crear_campo(
        formulario, 'Contraseña', 3, show='*'
    )

    # Combobox de Rol
    tk.Label(
        formulario,
        text='Rol',
        bg=self.color_panel,
        fg=self.color_texto,
        font=('Arial', 10, 'bold'),
    ).grid(row=4, column=0, sticky='w', pady=(0, 8), padx=(0, 10))

    self.usuario_rol_combo = ttk.Combobox(
        formulario, values=('Empleado', 'Cliente'), state='readonly', width=25
    )
    self.usuario_rol_combo.grid(row=4, column=1, sticky='ew', pady=(0, 8))
    self.usuario_rol_combo.set('Cliente')

    # Etiqueta de estado del Rol (<<ComboboxSelected>>)
    self.usuario_rol_estado = tk.Label(
        formulario,
        text='Rol seleccionado: Cliente',
        bg=self.color_panel,
        fg=self.color_texto,
        font=('Arial', 9),
    )
    self.usuario_rol_estado.grid(
        row=5, column=0, columnspan=2, sticky='w', pady=(0, 8)
    )

    # Botones de Acción (Formulario Usuarios)
    acciones = tk.Frame(formulario, bg=self.color_panel)
    acciones.grid(row=6, column=0, columnspan=2, sticky='ew', pady=(12, 0))

    botones = (
        ('Registrar', self.registrar_usuario, 'Accion.TButton', 'registrar.png'),
        (
            'Actualizar',
            self.actualizar_usuario,
            'Accion.TButton',
            'actualizar.png',
        ),
        ('Eliminar', self.eliminar_usuario, 'Eliminar.TButton', 'eliminar.png'),
        ('Limpiar', self.limpiar_formulario_usuario, 'Secundario.TButton', 'limpiar.png'),
    )

    for texto, comando, estilo, icono in botones:
      self.crear_boton(acciones, texto, comando, estilo, icono).pack(
          fill='x', pady=(0, 7)
      )

    # Tabla de Usuarios
    listado = self.crear_listado(cuerpo, 'Usuarios registrados', usar_grid=True)
    self.tabla_usuarios = self.crear_tabla(
        listado,
        ('identificador', 'nombre', 'usuario', 'rol'),
        ('Identificador', 'Nombre', 'Usuario', 'Rol'),
    )

    # --- BINDING DE EVENTOS (Semana 16) ---

    # 1. Evento virtual: Selección en Treeview carga datos al formulario
    self.tabla_usuarios.bind('<<TreeviewSelect>>', self.al_seleccionar_usuario)

    # 2. Evento de teclado: Enter confirma el registro (atajo)
    self.usuario_rol_combo.bind('<Return>', self.al_presionar_enter)

    # 3. Evento de teclado: Escape limpia el formulario y cancela selección
    for widget in (
        self.usuario_identificador_entry,
        self.usuario_nombre_entry,
        self.usuario_login_entry,
        self.usuario_contrasena_entry,
        self.usuario_rol_combo,
        self.tabla_usuarios,
    ):
      widget.bind('<Escape>', self.al_presionar_escape)

    # 4. Evento virtual: Detecta el cambio de rol en el Combobox
    self.usuario_rol_combo.bind('<<ComboboxSelected>>', self.al_seleccionar_rol)

    self.refrescar_usuarios()

  # --- Callbacks y Métodos de Lógica para Usuarios ---

  def obtener_datos_usuario(self):
    """Obtiene y limpia los datos de los campos del formulario de usuario."""
    assert self.usuario_identificador_entry is not None
    assert self.usuario_nombre_entry is not None
    assert self.usuario_login_entry is not None
    assert self.usuario_contrasena_entry is not None
    assert self.usuario_rol_combo is not None
    return (
        self.usuario_identificador_entry.get().strip(),
        self.usuario_nombre_entry.get().strip(),
        self.usuario_login_entry.get().strip(),
        self.usuario_contrasena_entry.get().strip(),
        self.usuario_rol_combo.get().strip(),
    )

  def registrar_usuario(self):
    """Acción del botón 'Registrar' o atajo <Return>."""
    try:
      # Reutiliza la lógica de negocio del servicio
      self.restaurante_servicio.registrar_usuario(*self.obtener_datos_usuario())
      self.limpiar_formulario_usuario()
      self.refrescar_usuarios()
      messagebox.showinfo('Usuarios', 'Usuario registrado correctamente.')
    except ValueError as error:
      messagebox.showerror('Usuarios', str(error))

  def al_seleccionar_usuario(self, event):
    """Callback para <<TreeviewSelect>>: Carga el usuario seleccionado."""
    assert self.tabla_usuarios is not None
    seleccion = self.tabla_usuarios.selection()
    if not seleccion:
      return

    # Obtiene el identificador de la primera columna (oculta o visible)
    valores = self.tabla_usuarios.item(seleccion[0], 'values')
    if not valores:
      return

    identificador = valores[0]
    usuario = self.restaurante_servicio.buscar_usuario_por_identificador(
        identificador
    )
    if usuario is None:
      return

    self.cargar_usuario_en_formulario(usuario)

  def cargar_usuario_en_formulario(self, usuario):
    """Utility para poblar el formulario con datos de un objeto Usuario."""
    assert self.usuario_identificador_entry is not None
    assert self.usuario_nombre_entry is not None
    assert self.usuario_login_entry is not None
    assert self.usuario_contrasena_entry is not None
    assert self.usuario_rol_combo is not None

    self.limpiar_campos_usuario()
    self.usuario_identificador_seleccionado = usuario.identificador
    self.usuario_identificador_entry.insert(0, usuario.identificador)
    self.usuario_nombre_entry.insert(0, usuario.nombre)
    self.usuario_login_entry.insert(0, usuario.usuario)
    self.usuario_contrasena_entry.insert(0, usuario.contrasena)

    # Lógica de seguridad: Un admin no puede quitarse el rol a sí mismo
    if (
        usuario.identificador == self.usuario_actual.identificador
        and usuario.rol == 'Administrador'
    ):
      self.usuario_rol_combo.configure(
          values=('Administrador',), state='disabled'
      )
    else:
      self.usuario_rol_combo.configure(
          values=('Empleado', 'Cliente'), state='readonly'
      )

    self.usuario_rol_combo.set(usuario.rol)
    self.actualizar_texto_rol(usuario.rol)

  def actualizar_usuario(self):
    """Acción del botón 'Actualizar'."""
    if self.usuario_identificador_seleccionado is None:
      messagebox.showerror('Usuarios', 'Seleccione un usuario de la tabla.')
      return

    identificador, nombre, usuario, contrasena, rol = (
        self.obtener_datos_usuario()
    )

    if identificador != self.usuario_identificador_seleccionado:
      messagebox.showerror(
          'Usuarios', 'No cambie el identificador del usuario seleccionado.'
      )
      return

    try:
      self.restaurante_servicio.actualizar_usuario(
          identificador,
          nombre,
          usuario,
          contrasena,
          rol,
          self.usuario_actual.identificador,
      )
      self.refrescar_usuarios()
      messagebox.showinfo('Usuarios', 'Usuario actualizado correctamente.')
    except ValueError as error:
      messagebox.showerror('Usuarios', str(error))

  def eliminar_usuario(self):
    """Acción del botón 'Eliminar'."""
    if self.usuario_identificador_seleccionado is None:
      messagebox.showerror('Usuarios', 'Seleccione un usuario de la tabla.')
      return

    confirmar = messagebox.askyesno(
        'Usuarios', '¿Desea eliminar el usuario seleccionado?'
    )
    if not confirmar:
      return

    try:
      self.restaurante_servicio.eliminar_usuario(
          self.usuario_identificador_seleccionado, self.usuario_actual.identificador
      )
      self.limpiar_formulario_usuario()
      self.refrescar_usuarios()
      messagebox.showinfo('Usuarios', 'Usuario eliminado correctamente.')
    except ValueError as error:
      messagebox.showerror('Usuarios', str(error))

  def limpiar_campos_usuario(self):
    """Utility para vaciar las entradas de texto del formulario."""
    for entrada in (
        self.usuario_identificador_entry,
        self.usuario_nombre_entry,
        self.usuario_login_entry,
        self.usuario_contrasena_entry,
    ):
      assert entrada is not None
      entrada.delete(0, tk.END)

  def limpiar_formulario_usuario(self):
    """Utility/Callback para botón 'Limpiar' o <Escape>: Restablece el estado."""
    assert self.usuario_identificador_entry is not None
    assert self.usuario_rol_combo is not None

    self.limpiar_campos_usuario()
    self.usuario_identificador_seleccionado = None
    self.usuario_rol_combo.configure(
        values=('Empleado', 'Cliente'), state='readonly'
    )
    self.usuario_rol_combo.set('Cliente')
    self.actualizar_texto_rol('Cliente')

    # Cancela la selección visual en la tabla
    if self.tabla_usuarios is not None:
      for item in self.tabla_usuarios.selection():
        self.tabla_usuarios.selection_remove(item)

    self.usuario_identificador_entry.focus()

  def al_presionar_enter(self, event):
    """Callback para <Return> en Combobox (atajo de registro)."""
    # Semana 16: Evitamos duplicar lógica llamando al método existente
    self.registrar_usuario()

  def al_presionar_escape(self, event):
    """Callback para <Escape> en widgets de usuario (cancela/limpia)."""
    # Semana 16: Evitamos duplicar lógica llamando al método existente
    self.limpiar_formulario_usuario()

  def al_seleccionar_rol(self, event):
    """Callback para <<ComboboxSelected>>: Actualiza texto informativo."""
    assert self.usuario_rol_combo is not None
    self.actualizar_texto_rol(self.usuario_rol_combo.get())

  def actualizar_texto_rol(self, rol):
    """Utility para cambiar el texto de la etiqueta debajo del Combobox."""
    if self.usuario_rol_estado is not None:
      self.usuario_rol_estado.config(text=f'Rol seleccionado: {rol}')

  def refrescar_usuarios(self):
    """Vuelve a cargar la lista de usuarios del servicio en la tabla."""
    assert self.tabla_usuarios is not None
    self.limpiar_tabla(self.tabla_usuarios)
    for usuario in self.restaurante_servicio.listar_usuarios():
      # No mostramos la contraseña en la tabla por seguridad
      self.tabla_usuarios.insert(
          '',
          tk.END,
          values=(
              usuario.identificador,
              usuario.nombre,
              usuario.usuario,
              usuario.rol,
          ),
      )
    self.actualizar_barra_estado()

  # -------------------------------------------------------------------------
  # Productos: CRUD básico e Integración de stock (Semana 14/15/16).
  # -------------------------------------------------------------------------
  def mostrar_productos(self):
    self.marcar_seccion('Productos')
    self.limpiar_contenido()
    assert self.contenido is not None
    self.crear_titulo_seccion('Gestión de productos')

    cuerpo = tk.Frame(self.contenido, bg=self.color_fondo)
    cuerpo.pack(fill='both', expand=True)
    cuerpo.grid_columnconfigure(1, weight=1)
    cuerpo.grid_rowconfigure(0, weight=1)

    # Formulario de Producto
    formulario = tk.LabelFrame(
        cuerpo,
        text='Datos del producto',
        bg=self.color_panel,
        fg=self.color_encabezado,
        font=('Arial', 10, 'bold'),
        padx=14,
        pady=14,
    )
    formulario.grid(row=0, column=0, sticky='n', padx=(0, 18))

    self.producto_codigo_entry = self.crear_campo(formulario, 'Código', 0)
    self.producto_nombre_entry = self.crear_campo(formulario, 'Nombre', 1)
    self.producto_categoria_entry = self.crear_campo(formulario, 'Categoría', 2)
    self.producto_precio_entry = self.crear_campo(formulario, 'Precio', 3)
    # Campo stock integrado
    self.producto_stock_entry = self.crear_campo(formulario, 'Stock', 4)

    # Botones de Acción (Formulario Productos)
    acciones = tk.Frame(formulario, bg=self.color_panel)
    acciones.grid(row=5, column=0, columnspan=2, sticky='ew', pady=(12, 0))

    botones = (
        ('Registrar', self.registrar_producto, 'Accion.TButton', 'registrar.png'),
        (
            'Cargar por código',
            self.cargar_producto_en_formulario,
            'Secundario.TButton',
            'cargar.png',
        ),
        (
            'Actualizar',
            self.actualizar_producto,
            'Accion.TButton',
            'actualizar.png',
        ),
        ('Eliminar', self.eliminar_producto, 'Eliminar.TButton', 'eliminar.png'),
        ('Limpiar', self.limpiar_formulario_producto, 'Secundario.TButton', 'limpiar.png'),
    )

    for texto, comando, estilo, icono in botones:
      self.crear_boton(acciones, texto, comando, estilo, icono).pack(
          fill='x', pady=(0, 7)
      )

    # Tabla de Productos
    listado = self.crear_listado(cuerpo, 'Productos registrados', usar_grid=True)
    self.tabla_productos = self.crear_tabla(
        listado,
        ('codigo', 'nombre', 'categoria', 'precio', 'stock'),
        ('Código', 'Nombre', 'Categoría', 'Precio', 'Stock'),
    )

    self.refrescar_productos()

  # --- Métodos de Lógica para Productos ---

  def obtener_datos_producto(self):
    """Obtiene y limpia los datos de los campos del formulario de producto."""
    assert self.producto_codigo_entry is not None
    assert self.producto_nombre_entry is not None
    assert self.producto_categoria_entry is not None
    assert self.producto_precio_entry is not None
    assert self.producto_stock_entry is not None
    return (
        self.producto_codigo_entry.get().strip(),
        self.producto_nombre_entry.get().strip(),
        self.producto_categoria_entry.get().strip(),
        self.producto_precio_entry.get().strip(),
        self.producto_stock_entry.get().strip(),
    )

  def registrar_producto(self):
    """Acción del botón 'Registrar'."""
    try:
      self.restaurante_servicio.registrar_producto(*self.obtener_datos_producto())
      self.limpiar_formulario_producto()
      self.refrescar_productos()
      messagebox.showinfo('Productos', 'Producto registrado correctamente.')
    except ValueError as error:
      messagebox.showerror('Productos', str(error))

  def cargar_producto_en_formulario(self):
    """Acción del botón 'Cargar por código'."""
    assert self.producto_codigo_entry is not None
    assert self.producto_nombre_entry is not None
    assert self.producto_categoria_entry is not None
    assert self.producto_precio_entry is not None
    assert self.producto_stock_entry is not None

    producto = self.restaurante_servicio.buscar_producto_por_codigo(
        self.producto_codigo_entry.get()
    )
    if producto is None:
      messagebox.showerror('Productos', 'No existe un producto con ese código.')
      return

    self.limpiar_formulario_producto()
    self.producto_codigo_entry.insert(0, producto.codigo)
    self.producto_nombre_entry.insert(0, producto.nombre)
    self.producto_categoria_entry.insert(0, producto.categoria)
    self.producto_precio_entry.insert(0, f'{producto.precio:.2f}')
    self.producto_stock_entry.insert(0, str(producto.stock))

  def actualizar_producto(self):
    """Acción del botón 'Actualizar'."""
    try:
      self.restaurante_servicio.actualizar_producto(*self.obtener_datos_producto())
      self.refrescar_productos()
      messagebox.showinfo('Productos', 'Producto actualizado correctamente.')
    except ValueError as error:
      messagebox.showerror('Productos', str(error))

  def eliminar_producto(self):
    """Acción del botón 'Eliminar'."""
    assert self.producto_codigo_entry is not None
    try:
      self.restaurante_servicio.eliminar_producto(self.producto_codigo_entry.get())
      self.limpiar_formulario_producto()
      self.refrescar_productos()
      messagebox.showinfo('Productos', 'Producto eliminado correctamente.')
    except ValueError as error:
      messagebox.showerror('Productos', str(error))

  def limpiar_formulario_producto(self):
    """Acción del botón 'Limpiar'."""
    for entrada in (
        self.producto_codigo_entry,
        self.producto_nombre_entry,
        self.producto_categoria_entry,
        self.producto_precio_entry,
        self.producto_stock_entry,
    ):
      assert entrada is not None
      entrada.delete(0, tk.END)

  def refrescar_productos(self):
    """Vuelve a cargar la lista de productos del servicio en la tabla."""
    assert self.tabla_productos is not None
    self.limpiar_tabla(self.tabla_productos)
    for producto in self.restaurante_servicio.listar_productos():
      self.tabla_productos.insert(
          '',
          tk.END,
          values=(
              producto.codigo,
              producto.nombre,
              producto.categoria,
              f'${producto.precio:.2f}',
              producto.stock,
          ),
      )
    self.actualizar_barra_estado()

  # -------------------------------------------------------------------------
  # Ventas: Gestión de registro y visualización (Semana 15/16).
  # -------------------------------------------------------------------------
  def mostrar_ventas(self):
    self.marcar_seccion('Ventas')
    self.limpiar_contenido()
    assert self.contenido is not None
    self.crear_titulo_seccion('Ventas')

    cuerpo = tk.Frame(self.contenido, bg=self.color_fondo)
    cuerpo.pack(fill='both', expand=True)
    cuerpo.grid_columnconfigure(1, weight=1)
    cuerpo.grid_rowconfigure(0, weight=1)

    # Formulario para Registrar Venta
    formulario = tk.LabelFrame(
        cuerpo,
        text='Registrar venta',
        bg=self.color_panel,
        fg=self.color_encabezado,
        font=('Arial', 10, 'bold'),
        padx=14,
        pady=14,
    )
    formulario.grid(row=0, column=0, sticky='n', padx=(0, 18))

    self.usuario_venta_combo = self.crear_selector_venta(
        formulario, 'Usuario', 0, self.obtener_opciones_usuarios_venta()
    )
    self.producto_venta_combo = self.crear_selector_venta(
        formulario, 'Producto', 1, self.obtener_opciones_productos_venta()
    )

    # Botones de Acción (Formulario Ventas)
    acciones = tk.Frame(formulario, bg=self.color_panel)
    acciones.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(12, 0))

    # El botón usa command= para ejecutar este callback al hacer clic.
    self.crear_boton(
        acciones, 'Registrar venta', self.registrar_venta, 'Accion.TButton', 'registrar.png'
    ).pack(fill='x')

    # Tabla de Ventas
    listado = self.crear_listado(cuerpo, 'Ventas registradas', usar_grid=True)
    self.tabla_ventas = self.crear_tabla(
        listado,
        ('identificador', 'usuario', 'producto', 'fecha'),
        ('Venta', 'Usuario', 'Producto', 'Fecha'),
    )

    self.refrescar_ventas()

  # --- Métodos de Lógica para Ventas ---

  def crear_selector_venta(self, contenedor, etiqueta, fila, opciones):
    """Utility para crear Comboboxes de selección en ventas."""
    tk.Label(
        contenedor,
        text=etiqueta,
        bg=self.color_panel,
        fg=self.color_texto,
        font=('Arial', 10, 'bold'),
    ).grid(row=fila, column=0, sticky='w', pady=(0, 8), padx=(0, 10))

    selector = ttk.Combobox(
        contenedor, values=list(opciones.keys()), state='readonly', width=34
    )
    selector.grid(row=fila, column=1, sticky='ew', pady=(0, 8))
    return selector

  def obtener_opciones_usuarios_venta(self):
    """Utility: Genera el mapeo de Nombre -> ID para el combo de usuarios."""
    self.opciones_usuarios_venta = {
        f'{usuario.identificador} - {usuario.nombre}': usuario.identificador
        for usuario in self.restaurante_servicio.listar_usuarios()
    }
    return self.opciones_usuarios_venta

  def obtener_opciones_productos_venta(self):
    """Utility: Genera el mapeo de Nombre -> Código para el combo de productos."""
    self.opciones_productos_venta = {
        f'{producto.codigo} - {producto.nombre} (Stock: {producto.stock})': producto.codigo
        for producto in self.restaurante_servicio.listar_productos()
        if producto.stock > 0  # Solo productos con stock disponible
    }
    return self.opciones_productos_venta

  def registrar_venta(self):
    """Acción del botón 'Registrar venta'."""
    assert self.usuario_venta_combo is not None
    assert self.producto_venta_combo is not None

    usuario_id = self.opciones_usuarios_venta.get(
        self.usuario_venta_combo.get(), ''
    )
    producto_codigo = self.opciones_productos_venta.get(
        self.producto_venta_combo.get(), ''
    )

    try:
      # Relaciona el usuario y el producto seleccionados antes de registrar la venta.
      self.restaurante_servicio.registrar_venta(usuario_id, producto_codigo)
      self.limpiar_formulario_venta()
      self.refrescar_ventas()
      messagebox.showinfo('Ventas', 'Venta registrada correctamente.')
    except ValueError as error:
      messagebox.showerror('Ventas', str(error))

  def limpiar_formulario_venta(self):
    """Utility: Restablece los comboboxes de venta."""
    assert self.usuario_venta_combo is not None
    assert self.producto_venta_combo is not None
    self.usuario_venta_combo.set('')
    # Actualiza las opciones de producto (por si cambió el stock)
    self.producto_venta_combo.configure(
        values=list(self.obtener_opciones_productos_venta().keys())
    )
    self.producto_venta_combo.set('')

  def refrescar_ventas(self):
    """Vuelve a cargar la lista de ventas del servicio en la tabla."""
    assert self.tabla_ventas is not None
    self.limpiar_tabla(self.tabla_ventas)

    for venta in self.restaurante_servicio.listar_ventas():
      usuario = self.restaurante_servicio.buscar_usuario_por_identificador(
          venta.usuario_id
      )
      producto = self.restaurante_servicio.buscar_producto_por_codigo(
          venta.producto_codigo
      )

      texto_usuario = (
          venta.usuario_id
          if usuario is None
          else f'{usuario.identificador} - {usuario.nombre}'
      )
      texto_producto = (
          venta.producto_codigo
          if producto is None
          else f'{producto.codigo} - {producto.nombre}'
      )

      self.tabla_ventas.insert(
          '',
          tk.END,
          values=(
              venta.identificador,
              texto_usuario,
              texto_producto,
              venta.fecha,
          ),
      )
    # Refresca la tabla para mostrar la respuesta de la aplicación.
    self.actualizar_barra_estado()

  # -------------------------------------------------------------------------
  # Utilidades de interfaz compartidas por las vistas.
  # -------------------------------------------------------------------------
  def crear_titulo_seccion(self, texto):
    """Empaca un título principal para cada sección."""
    assert self.contenido is not None
    tk.Label(
        self.contenido,
        text=texto,
        bg=self.color_fondo,
        fg=self.color_encabezado,
        font=('Arial', 20, 'bold'),
    ).pack(anchor='w', pady=(0, 16))

  def crear_campo(self, contenedor, etiqueta, fila, show=None):
    """Utility para crear una etiqueta y campo de entrada en un grid."""
    tk.Label(
        contenedor,
        text=etiqueta,
        bg=self.color_panel,
        fg=self.color_texto,
        font=('Arial', 10, 'bold'),
    ).grid(row=fila, column=0, sticky='w', pady=(0, 8), padx=(0, 10))

    entrada = tk.Entry(contenedor, width=28, font=('Arial', 10), show=show)
    entrada.grid(row=fila, column=1, sticky='ew', pady=(0, 8))
    return entrada

  def crear_listado(self, contenedor, titulo, usar_grid=False):
    """Utility para crear un contenedor LabelFrame para tablas."""
    listado = tk.LabelFrame(
        contenedor,
        text=titulo,
        bg=self.color_panel,
        fg=self.color_encabezado,
        font=('Arial', 10, 'bold'),
        padx=12,
        pady=12,
    )
    if usar_grid:
      listado.grid(row=0, column=1, sticky='nsew')
    else:
      listado.pack(fill='both', expand=True)
    return listado

  def crear_tabla(self, contenedor, columnas, encabezados):
    """Utility para crear una tabla Treeview con scrollbar."""
    frame_tabla = tk.Frame(contenedor, bg=self.color_panel)
    frame_tabla.pack(fill='both', expand=True)

    tabla = ttk.Treeview(frame_tabla, columns=columnas, show='headings', height=12)
    barra = ttk.Scrollbar(frame_tabla, orient='vertical', command=tabla.yview)
    tabla.configure(yscrollcommand=barra.set)

    for columna, encabezado in zip(columnas, encabezados):
      tabla.heading(columna, text=encabezado)
      tabla.column(columna, width=150, anchor='w')

    tabla.pack(side='left', fill='both', expand=True)
    barra.pack(side='right', fill='y')
    return tabla

  def limpiar_tabla(self, tabla):
    """Utility para borrar todas las filas de una tabla."""
    for item in tabla.get_children():
      tabla.delete(item)

  def cerrar_sesion(self):
    """Acción del botón 'Cerrar sesión'."""
    self.al_cerrar_sesion()