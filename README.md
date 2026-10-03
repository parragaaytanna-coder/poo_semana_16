# 🍽️ Sistema de Gestión de Restaurante — Semana 16 (Food Droppy App)
## Nombre del estudiante: Aytanna Párraga
Proyecto final desarrollado en **Python** con **Tkinter** para la asignatura de **Programación Orientada a Objetos (POO)**. Esta aplicación permite la gestión integral de un restaurante mediante una interfaz gráfica modular, control de usuarios por roles, gestión de productos y registro de ventas con persistencia en **JSON**.

---

## 📈 Evolución del Proyecto

El desarrollo del proyecto se consolidó a lo largo del ciclo académico aplicando los principios de la Programación Orientada a Objetos:

* **Fase Inicial (Estructura y Modelos):** Definición de las clases principales (`Usuario`, `Producto`, `Venta`) aplicando **encapsulamiento** y abstracción de entidades del mundo real.
* **Fase Intermedia (Persistencia y Lógica):** Implementación del almacenamiento modularizado en archivos `.json` para mantener el estado de la aplicación sin depender de una base de datos externa.
* **Fase Final (Interfaz Gráfica y Eventos - Semana 16):** Diseño modular de la GUI mediante Tkinter, manejo de vistas (`login_view.py` y `main_view.py`), escalado dinámico de recursos multimedias (`Pillow`) y vinculación avanzada de eventos de usuario (*callbacks*, `command=` y `bind()`).

---

## 👥 Gestión de Usuarios y Roles

La aplicación implementa un sistema de control de acceso según el perfil del usuario autenticado:

* **Administrador General:** Tiene acceso completo a la gestión del sistema, incluyendo la administración de usuarios, mantenimiento del menú de productos y visualización del reporte general de ventas.
* **Empleado / Mesero:** Acceso limitado al módulo operativo para el registro de ventas y consulta del menú disponible.

---

## 🖱️ Eventos Implementados (`bind()`, `command=` y Callbacks)

Para garantizar una interfaz interactiva y receptiva, se utilizaron diferentes mecanismos de manejo de eventos en Tkinter:

* **Uso de `command=`:** Asignado directamente a los botones de la navegación lateral y formularios (`tk.Button`) para desencadenar la ejecución de métodos *callback* (ej. cambio de vistas, inicio de sesión, guardado de registros).
* **Uso de `bind()`:**
  * Vinculación del evento `<Return>` (tecla Enter) en el formulario de inicio de sesión para permitir el acceso rápido sin hacer clic en el botón.
  * Captura de eventos de selección `<ListboxSelect>` o `<<ComboboxSelected>>` para la actualización dinámica de datos en pantalla.
* **Manejo de Callbacks:** Métodos internos encargados de validar entradas, procesar lógica de negocio y actualizar la interfaz gráfica dinámicamente sin congelar la aplicación.

---

## 📂 Estructura del Proyecto

```text
restaurante_app/
│
├── assets/                  # Recursos gráficos
│   ├── icons/               # Íconos de botones y navegación (.png)
│   └── logo/                # Logotipo del restaurante (.png)
│
├── datos/                   # Archivos JSON de persistencia de datos
│   ├── usuarios.json        # Registro de usuarios y credenciales
│   ├── productos.json       # Catálogo y precios del menú
│   └── ventas.json          # Historial de ventas realizadas
│
├── modelos/                 # Clases del modelo de dominio (POO)
│   ├── __init__.py
│   ├── producto.py          # Clase Producto
│   ├── usuario.py           # Clase Usuario
│   └── venta.py             # Clase Venta
│
├── ui/                      # Vistas de la Interfaz Gráfica (Tkinter)
│   ├── __init__.py
│   ├── login_view.py        # Vista de inicio de sesión
│   └── main_view.py         # Panel principal y navegación
│
├── main.py                  # Punto de entrada principal
├── requirements.txt         # Dependencias del proyecto
└── README.md                # Documentación del proyecto (Semana 16)


Persistencia de Datos
La aplicación utiliza la librería nativa json para la carga y almacenamiento de datos locales:

Lectura Automática: Al iniciar la aplicación, los módulos leen los archivos .json ubicados en la carpeta datos/.

Escritura en Tiempo Real: Cada registro, edición o eliminación de usuarios, productos o ventas actualiza inmediatamente el archivo .json correspondiente, garantizando la durabilidad de la información.

Pasos para ejecutar main.py
Prerrequisitos: Tener instalado Python 3.10 o superior y Tkinter (incluido por defecto en instaladores estándar de Python para Windows).

Abrir el proyecto: Abrir la carpeta raíz del proyecto en Visual Studio Code.

Ejecutar la aplicación:

Abrir la terminal en la raíz del proyecto (Terminal > Nueva terminal).

Ejecutar el comando:

Bash
python main.py