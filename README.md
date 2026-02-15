# 💊 Sistema de Gestión de Farmacia

Este proyecto es una aplicación de escritorio desarrollada en Python con interfaz gráfica usando `tkinter`, diseñada para la gestión básica de una farmacia. Permite registrar productos, controlar stock, realizar ventas, y visualizar información del inventario.

## 📌 Objetivo

Facilitar el manejo de productos farmacéuticos mediante un sistema intuitivo que permita registrar, modificar, buscar y eliminar productos, así como realizar ventas y mantener el control del inventario.

## 🖥️ Tecnologías utilizadas

- Python 3
- Tkinter (interfaz gráfica)
- SQLite (base de datos local)
- PIL (para manejo de imágenes)
- `datetime` (para control de fecha/hora)

## 🧩 Funcionalidades principales

- **Registro de productos:** Código, nombre, cantidad, precio, caducidad.
- **Búsqueda de productos** por código.
- **Actualización y eliminación** de registros.
- **Realización de ventas** con control de stock.
- **Alertas de productos caducos**.
- **Reloj en tiempo real** en la interfaz.
- **Diseño gráfico organizado** con botones e imágenes.

## ▶️ Cómo ejecutar

1. Clona el repositorio:
   ```bash
   git clone https://github.com/Rod45ri/Farmacia.git
   cd Farmacia
   ```

2. Asegúrate de tener Python 3 instalado.

3. Instala las dependencias necesarias:
   ```bash
   pip install pillow
   ```

4. Ejecuta el programa:
   ```bash
   python Proyecto_Fin.py
   ```

## 📷 Capturas (opcional)

_Puedes agregar capturas de pantalla del programa en ejecución aquí._

## 📂 Estructura del proyecto

```
Farmacia/
│
├── Proyecto_Fin.py        # Código principal del sistema
├── productos.db           # Base de datos SQLite (se genera en la primera ejecución)
└── img/                   # Carpeta con imágenes para la interfaz
```

## 👨‍💻 Autor

Rod45ri  
[https://github.com/Rod45ri](https://github.com/Rod45ri)

## 📝 Licencia

Este proyecto es de uso libre con fines educativos. Puedes modificarlo y reutilizarlo.