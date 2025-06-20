import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from datetime import datetime
import mysql.connector
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import platform
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

# Configuración de conexión a la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'farmacia_db'
}

class SistemaLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio de Sesión")
        self.root.geometry("800x500")
        frame = tk.Frame(root, bg="white")
        frame.place(x=400, y=0, width=400, height=500)
     

        try:
            image = Image.open("inicio.png").resize((400, 500))
            self.bg_image = ImageTk.PhotoImage(image)
            tk.Label(root, image=self.bg_image).place(x=0, y=0, width=400, height=500)
        except Exception as e:
            tk.Label(root, bg="lightblue").place(x=0, y=0, width=400, height=500)

        

        tk.Label(frame, text="¡Bienvenido de nuevo!", font=("Arial", 16, "bold"), fg="green", bg="white").pack(pady=20)

        self.entry_correo = self.crear_entry(frame, "Correo electrónico")
        self.entry_contraseña = self.crear_entry(frame, "Contraseña", es_password=True)

        tk.Button(frame, text="Iniciar sesión", command=self.iniciar_sesion).pack(pady=20)
        tk.Button(frame, text="¿No tienes cuenta? Regístrate", command=self.registrarse).pack(pady=5)

    def crear_entry(self, frame, texto, es_password=False):
        tk.Label(frame, text=texto, bg="white").pack(pady=5)
        entry = tk.Entry(frame, show="*" if es_password else "")
        entry.pack(pady=5, padx=20, fill="x")
        return entry



    def iniciar_sesion(self):
        correo = self.entry_correo.get()
        contraseña = self.entry_contraseña.get()
        conexion = mysql.connector.connect(**DB_CONFIG)
        cursor = conexion.cursor()
        cursor.execute("SELECT id_usuario, nombre_completo FROM usuarios WHERE correo=%s AND contraseña=%s", (correo, contraseña))
        resultado = cursor.fetchone()
        conexion.close()

        if resultado:
            self.root.destroy()
            root_app = tk.Tk()
            SistemaFarmacia(root_app, usuario_id=resultado[0], usuario_nombre=resultado[1])
            root_app.mainloop()
        else:
            messagebox.showerror("Error", "Correo o contraseña incorrectos")

    def registrarse(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Registro")
        ventana.geometry("400x300")

        tk.Label(ventana, text="Correo electrónico").pack(pady=5)
        entry_correo = tk.Entry(ventana)
        entry_correo.pack(pady=5)

        tk.Label(ventana, text="Contraseña").pack(pady=5)
        entry_contraseña = tk.Entry(ventana, show="*")
        entry_contraseña.pack(pady=5)

        tk.Label(ventana, text="Nombre completo").pack(pady=5)
        entry_nombre = tk.Entry(ventana)
        entry_nombre.pack(pady=5)

        def guardar():
            correo = entry_correo.get()
            contraseña = entry_contraseña.get()
            nombre = entry_nombre.get()

            if correo and contraseña and nombre:
                conexion = mysql.connector.connect(**DB_CONFIG)
                cursor = conexion.cursor()
                cursor.execute("INSERT INTO usuarios (correo, contraseña, nombre_completo) VALUES (%s, %s, %s)",
                               (correo, contraseña, nombre))
                conexion.commit()
                conexion.close()
                messagebox.showinfo("Éxito", "Usuario registrado")
                ventana.destroy()
            else:
                messagebox.showerror("Error", "Todos los campos son obligatorios")

        tk.Button(ventana, text="Registrar", command=guardar).pack(pady=10)

class SistemaFarmacia:
    def __init__(self, master, usuario_id, usuario_nombre):
        # Fondo de imagen
        self.master = master
        self.usuario_id = usuario_id
        self.usuario_nombre = usuario_nombre
        fondo_img = Image.open("logo.png").resize((900, 700))
        self.fondo_tk = ImageTk.PhotoImage(fondo_img)

        self.label_fondo = tk.Label(master, image=self.fondo_tk)
        self.label_fondo.grid(row=0, column=0, rowspan=999, columnspan=999, sticky="nsew")

        self.master.title(f"Sistema de Farmacia - Bienvenido {self.usuario_nombre}")
        self.label_reloj = tk.Label(master, font=("Arial", 10, "bold"), fg="black", anchor="e")
        self.master.geometry("900x700")
         # Estilos
        style = ttk.Style()
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)

        self.conn = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor(dictionary=True)
         # Layout con grid principal
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # 🔷 Encabezado
        frame_encabezado = tk.Frame(master, bg="#f9f9f9", relief=tk.GROOVE, bd=1)
        frame_encabezado.grid(row=0, column=0, sticky="ew")
        frame_encabezado.columnconfigure(1, weight=1)

        if os.path.exists("logo3.png"):
            logo = Image.open("logo3.png").resize((80, 40))
            self.logo_img = ImageTk.PhotoImage(logo)
            tk.Label(frame_encabezado, image=self.logo_img, bg="#f9f9f9").grid(row=0, column=0, padx=10)

        # Título
        tk.Label(frame_encabezado, text="Sistema de Farmacia - Bienvenido",
                 font=("Segoe UI", 14, "bold"), bg="#f9f9f9").grid(row=0, column=1, sticky="w")
 
        # Fecha y hora
        self.label_reloj = tk.Label(frame_encabezado, font=("Segoe UI", 10), bg="#f9f9f9")
        self.label_reloj.grid(row=0, column=2, sticky="e", padx=10)
        self.iniciar_reloj()

         # Usuario (línea debajo del reloj)
        self.label_usuario = tk.Label(frame_encabezado, text=f"Usuario: {self.usuario_nombre}",
                                      font=("Segoe UI", 9), bg="#f9f9f9")
        self.label_usuario.grid(row=1, column=2, sticky="e", padx=10)

        style = ttk.Style()
        style.theme_use("default")

# 🔷 Estilo para agrandar las pestañas
        style.configure("TNotebook.Tab", padding=[20, 10], font=("Segoe UI", 11, "bold"))


        # 📁 Pestañas
        self.tab_control = ttk.Notebook(master)
        self.tab_control.grid(row=1, column=0, sticky="nsew")
        self.tab_stock = ttk.Frame(self.tab_control)
        self.tab_ventas = ttk.Frame(self.tab_control)
        self.tab_reportes = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab_stock, text="Stock")
        self.tab_control.add(self.tab_ventas, text="Ventas")
        

        self.contador_ventas = 0
        self.ventas = []

        self.configurar_stock()
        self.configurar_ventas()
        self.configurar_reportes()  
        # puedes habilitar es to si tienes reportes
    def iniciar_reloj(self):
        ahora = datetime.now()
        texto = ahora.strftime("%d/%m/%Y %H:%M:%S")
        self.label_reloj.config(text=texto)
        self.master.after(1000, self.iniciar_reloj)  # Actualiza cada segundo

#STOCK  
    def configurar_stock(self):

        frame_buscar = ttk.Frame(self.tab_stock, padding="10")
        frame_buscar.pack(pady=10, fill=tk.X)
        ttk.Label(frame_buscar, text="Buscar Producto:").pack(side=tk.LEFT, padx=5)
        self.entry_buscar = ttk.Entry(frame_buscar, width=30)
        self.entry_buscar.pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buscar, text="Buscar", command=self.buscar_producto).pack(side=tk.LEFT, padx=5)

    
        self.tree_stock = ttk.Treeview(self.tab_stock, columns=("ID", "Nombre", "Stock","precio", "Tipo", "Receta"), show="headings")
        self.label_imagen = tk.Label(self.tab_stock)
        self.label_imagen.pack(pady=5)
        
        self.tree_stock.bind("<<TreeviewSelect>>", self.mostrar_imagen_stock)
        self.tree_stock.heading("ID", text="ID")
        self.tree_stock.heading("Nombre", text="Nombre")
        self.tree_stock.heading("Stock", text="Stock")
        self.tree_stock.heading("precio", text="Precio Unitario")
        self.tree_stock.heading("Tipo", text="Tipo")
        self.tree_stock.heading("Receta", text="Receta")
        self.tree_stock.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # 🔘 Botones
        frame_botones = ttk.Frame(self.tab_stock, padding="10")
        frame_botones.pack(pady=10, fill=tk.X)

        ttk.Button(frame_botones, text="🟰 Agregar Producto", command=self.abrir_ventana_agregar).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="⚠️ Verificar Alertas", command=self.verificar_alertas).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="📄 Exportar Stock a PDF", command=self.exportar_stock_pdf).pack(side=tk.LEFT, padx=5)
    

    # 🗑 Eliminar producto
        frame_eliminar = ttk.LabelFrame(self.tab_stock, text="Eliminar Producto", padding="10")
        frame_eliminar.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(frame_eliminar, text="ID del Producto:").pack(side=tk.LEFT, padx=5)
        self.entry_id_producto = ttk.Entry(frame_eliminar, width=15)
        self.entry_id_producto.pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_eliminar, text="🗑 Eliminar", command=self.eliminar_producto).pack(side=tk.LEFT, padx=5)

    # Cargar tabla
        self.actualizar_tabla_stock()


    def actualizar_tabla_stock(self):
        for row in self.tree_stock.get_children():
            self.tree_stock.delete(row)
        self.cursor.execute("SELECT id_producto, nombre, stock, precio_unitario, tipo, requiere_receta FROM productos")
        for producto in self.cursor.fetchall():
            self.tree_stock.insert("", "end", values=(producto["id_producto"], producto["nombre"], producto["stock"],f"${producto['precio_unitario']:.2f}",producto["tipo"],producto["requiere_receta"]))

    def mostrar_imagen_stock(self, event):
        seleccion = self.tree_stock.selection()
        if seleccion:
            item = self.tree_stock.item(seleccion[0])
            nombre_producto = item["values"][0]  # o [0] si usas ID

            ruta_imagen = os.path.join("imagenes_productos", f"{nombre_producto}.png")

            if os.path.exists(ruta_imagen):
                imagen = Image.open(ruta_imagen).resize((120, 100))
                self.img_producto = ImageTk.PhotoImage(imagen)
                self.label_imagen.config(image=self.img_producto, text="")
            else:
                self.label_imagen.config(image="", text="Sin imagen")


    def eliminar_producto(self):
        id_producto = self.entry_id_producto.get().strip()
        if not id_producto.isdigit():
            messagebox.showwarning("Error", "Ingrese un ID de producto válido.")
            return
        confirmacion = messagebox.askyesno("Eliminar Producto", f"¿Estás seguro de que deseas eliminar el producto ID {id_producto}?")
        if not confirmacion:
            return

        try:
            self.cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
            self.conn.commit()
            self.actualizar_tabla_stock()
            messagebox.showinfo("Eliminado", f"Producto ID {id_producto} eliminado correctamente.")
        except mysql.connector.errors.IntegrityError:
            messagebox.showerror("Error", "Este producto ya fue registrado en una venta y no puede eliminarse.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el producto: {str(e)}")


    def obtener_productos(self):
        self.cursor.execute("SELECT nombre, stock, DATE_FORMAT(vencimiento, '%d/%m/%Y') AS vencimiento, precio_unitario FROM productos")
        return self.cursor.fetchall()
    

    def exportar_stock_pdf(self):
        try:
            productos = self.obtener_productos()

            archivo = "stock_productos.pdf"
            c = canvas.Canvas(archivo, pagesize=letter)
            c.setFont("Helvetica-Bold", 14)
            c.drawString(200, 750, "Reporte de Stock de Productos")

            # Encabezados
            c.setFont("Helvetica-Bold", 10)
            columnas = ["Nombre", "Stock", "Vencimiento", "Precio Unitario"]
            x_inicial = 50
            y = 720
            for i, columna in enumerate(columnas):
                c.drawString(x_inicial + i * 120, y, columna)

            # Filas de productos
            c.setFont("Helvetica", 10)
            y -= 20
            for producto in productos:
                if y < 50:
                    c.showPage()
                    y = 750
                c.drawString(x_inicial + 0, y, str(producto["nombre"]))
                c.drawString(x_inicial + 120, y, str(producto["stock"]))
                c.drawString(x_inicial + 240, y, str(producto["vencimiento"]))
                c.drawString(x_inicial + 360, y, f"${producto['precio_unitario']:.2f}")
                y -= 20

            c.save()
            # Abrir el PDF
            if platform.system() == "Windows":
                os.startfile(archivo)
        
            messagebox.showinfo("PDF generado", f"Se ha creado el archivo '{archivo}' con éxito.")
        except Exception as e:
            messagebox.showerror("Error al generar PDF", str(e))


    def buscar_producto(self):
        query = self.entry_buscar.get().lower()
        self.cursor.execute(
            "SELECT nombre, stock, DATE_FORMAT(vencimiento, '%d/%m/%Y') AS vencimiento, precio_unitario FROM productos WHERE LOWER(nombre) LIKE %s",
            (f"%{query}%",)
        )
        resultados = self.cursor.fetchall()

        for item in self.tree_stock.get_children():
            self.tree_stock.delete(item)
        for producto in resultados:
            self.tree_stock.insert("", "end", values=(
                producto["nombre"],
                producto["stock"],
                producto["vencimiento"],
                f"${producto['precio_unitario']:.2f}"
            ))

    def abrir_ventana_agregar(self):
        ventana = tk.Toplevel(self.master)
        ventana.title("Agregar Producto")
        ventana.geometry("300x300")

        ttk.Label(ventana, text="Nombre:").pack(pady=5)
        entry_nombre = ttk.Entry(ventana, width=30)
        entry_nombre.pack(pady=5)

        ttk.Label(ventana, text="Stock:").pack(pady=5)
        entry_stock = ttk.Entry(ventana, width=30)
        entry_stock.pack(pady=5)

        ttk.Label(ventana, text="Precio Unitario:").pack(pady=5)
        entry_precio = ttk.Entry(ventana, width=30)
        entry_precio.pack(pady=5)
        

        ttk.Label(ventana, text="Vencimiento (dd/mm/yyyy):").pack(pady=5)
        entry_vencimiento = ttk.Entry(ventana, width=30)
        entry_vencimiento.pack(pady=5)

        # Tipo de producto
        ttk.Label(ventana, text="Tipo de Producto:").pack(pady=5)
        tipo_var = tk.StringVar()
        combo_tipo = ttk.Combobox(ventana, textvariable=tipo_var, values=["Jarabe", "Tableta", "Cápsula", "Inyectable", "Otro"])
        combo_tipo.pack(pady=5)
        combo_tipo.current(0)

        # ¿Requiere receta?
        ttk.Label(ventana, text="¿Requiere receta médica?").pack(pady=5)
        requiere_var = tk.StringVar(value="No")
        frame_requiere = ttk.Frame(ventana)
        frame_requiere.pack()
        ttk.Radiobutton(frame_requiere, text="Sí", variable=requiere_var, value="Sí").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(frame_requiere, text="No", variable=requiere_var, value="No").pack(side=tk.LEFT, padx=5)

        def agregar_producto():
            nombre = entry_nombre.get().strip()
            stock = entry_stock.get().strip()
            precio = entry_precio.get().strip()
            vencimiento = entry_vencimiento.get().strip()
            tipo = tipo_var.get()
            requiere = requiere_var.get()


            if nombre and stock.isdigit() and precio.replace('.', '', 1).isdigit() and vencimiento:
                try:
                    fecha_obj = datetime.strptime(vencimiento, "%d/%m/%Y")
                    fecha_mysql = fecha_obj.strftime("%Y-%m-%d")
                    try:
                        while self.cursor.nextset():
                            pass
                    except:
                        pass
                    self.cursor.execute(
                        "INSERT INTO productos (nombre, stock, vencimiento, precio_unitario, tipo, requiere_receta) VALUES (%s, %s, %s, %s, %s, %s)",
                        (nombre, int(stock), fecha_mysql, float(precio), tipo, requiere)
                    )
                    self.conn.commit()
                    self.actualizar_tabla_stock()
                    messagebox.showinfo("Éxito", "Producto agregado correctamente")
                    ventana.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Formato de fecha inválido. Use dd/mm/yyyy")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo agregar el producto: {str(e)}")
            else:
                messagebox.showwarning("Error", "Datos inválidos. Verifica los campos.")

        ttk.Button(ventana, text="Agregar", command=agregar_producto).pack(pady=10)


    
    def verificar_alertas(self):
        try:
            self.cursor.execute("SELECT nombre, vencimiento FROM productos")
            hoy = datetime.today().date()
            alerta = ""
            for producto in self.cursor.fetchall():
                fecha_venc = producto["vencimiento"]
                dias_restantes = (fecha_venc - hoy).days
                if dias_restantes < 0:
                    alerta += f"{producto['nombre']} está vencido!\n"
                elif dias_restantes <= 30:
                    alerta += f"{producto['nombre']} está por vencer pronto (en {dias_restantes} días)!\n"

            if alerta:
                messagebox.showwarning("Alertas de Vencimiento", alerta)
            else:
                messagebox.showinfo("Sin Alertas", "No hay productos próximos a vencer.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al verificar alertas: {str(e)}")

    def configurar_ventas(self):
        
        self.frame_entrada = ttk.Frame(self.tab_ventas, padding="10")
        
        self.frame_entrada.pack(fill=tk.X, padx=20, pady=10)
        ttk.Label(self.frame_entrada, text="Cliente:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_cliente = ttk.Entry(self.frame_entrada, width=30)
        self.entry_cliente.grid(row=0, column=1, padx=5, pady=5)


        ttk.Label(self.frame_entrada, text="Medicamento:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_medicamento = ttk.Entry(self.frame_entrada, width=30)
        self.entry_medicamento.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.frame_entrada, text="Cantidad:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_cantidad = ttk.Entry(self.frame_entrada, width=30)
        self.entry_cantidad.grid(row=2, column=1, padx=5, pady=5)

        self.btn_agregar = ttk.Button(self.frame_entrada, text="Agregar Venta", command=self.agregar_venta)
        self.btn_agregar.grid(row=3, column=0, columnspan=2, pady=10)

        self.frame_tabla = ttk.Frame(self.tab_ventas, padding="10")
        self.frame_tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columnas = ("medicamento", "cantidad", "precio", "total")
        self.tabla_ventas = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings", height=10)
        for col in columnas:
            self.tabla_ventas.heading(col, text=col.capitalize())
            self.tabla_ventas.column(col, width=100)
        self.tabla_ventas.pack(fill=tk.BOTH, expand=True)

        self.frame_finalizar = ttk.Frame(self.tab_ventas, padding="10")
        self.frame_finalizar.pack(fill=tk.X, padx=20, pady=10)
        self.btn_finalizar = ttk.Button(self.frame_finalizar, text="Finalizar Venta", command=self.finalizar_venta)
        self.btn_finalizar.pack(side=tk.RIGHT)

    def agregar_venta(self):
        if not hasattr(self, "ventas"):
            self.ventas = []

        medicamento = self.entry_medicamento.get().strip()
        cantidad = self.entry_cantidad.get().strip()

        if not medicamento or not cantidad:
            messagebox.showerror("Error", "Completa todos los campos.")
            return

        try:
            cantidad_val = int(cantidad)
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un entero.")
            return

        self.cursor.execute("SELECT id_producto, stock, precio_unitario FROM productos WHERE nombre = %s", (medicamento,))
        producto = self.cursor.fetchone()
        if not producto:
            messagebox.showerror("Error", "Producto no encontrado.")
            return

        if producto['stock'] < cantidad_val:
            messagebox.showerror("Error", f"Stock insuficiente. Disponible: {producto['stock']}")
            return

        total = cantidad_val * float(producto['precio_unitario'])
        self.ventas.append({"id": producto['id_producto'], "nombre": medicamento, "cantidad": cantidad_val, "precio": float(producto['precio_unitario']), "total": total})

        tag = 'even' if self.contador_ventas % 2 == 0 else 'odd'
        self.tabla_ventas.insert("", "end", values=(medicamento, cantidad_val, f"${producto['precio_unitario']:.2f}", f"${total:.2f}"), tags=(tag,))
        self.contador_ventas += 1

        self.entry_medicamento.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)
        for venta in self.ventas:
            if not isinstance(venta, dict):
                messagebox.showerror("Error interno", "Se detectó una venta corrupta.")
                return

    def finalizar_venta(self):
        cliente = self.entry_cliente.get().strip()
        if not cliente:
            messagebox.showerror("Error", "Debes ingresar el nombre del cliente.")
            return

        if not self.ventas:
            messagebox.showinfo("Info", "No hay ventas a registrar.")
            return
        while self.cursor.nextset():
            pass

        fecha_actual = datetime.today().strftime('%Y-%m-%d')
        self.cursor.execute(
            "INSERT INTO ventas (fecha, id_usuario, cliente) VALUES (%s, %s, %s)",
            (fecha_actual, self.usuario_id, cliente)
        )
        self.conn.commit()
        id_venta = self.cursor.lastrowid
        for venta in self.ventas:
            if not isinstance(venta, dict) or 'id' not in venta or 'cantidad' not in venta:
                messagebox.showerror("Error", f"Venta inválida detectada: {venta}")
                return


        for venta in self.ventas:
            self.cursor.execute(
                "INSERT INTO detalle_ventas (id_venta, id_producto, cantidad) VALUES (%s, %s, %s)",
                (id_venta, venta["id"], venta["cantidad"])
            )
            self.cursor.execute(
                "UPDATE productos SET stock = stock - %s WHERE id_producto = %s",
                (venta["cantidad"], venta["id"])
            )

        self.conn.commit()
        total = sum(v["total"] for v in self.ventas)
        messagebox.showinfo("Venta Registrada", f"Venta registrada con éxito. Total: ${total:.2f}")

        self.ventas.clear()
        for item in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(item)
        self.actualizar_tabla_stock()

    
    #############################################
    # FUNCIONALIDAD: HISTORIAL Y REPORTES
    #######################################
    def configurar_reportes(self):
        self.tab_reportes = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_reportes, text="Reportes")

        self.frame_filtros = ttk.Frame(self.tab_reportes, padding="10")
        self.frame_filtros.pack(fill=tk.X, padx=20, pady=10)

        ttk.Label(self.frame_filtros, text="Desde (dd/mm/yyyy):").grid(row=0, column=0, padx=5, pady=5)
        self.entry_desde = ttk.Entry(self.frame_filtros, width=15)
        self.entry_desde.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.frame_filtros, text="Hasta (dd/mm/yyyy):").grid(row=0, column=2, padx=5, pady=5)
        self.entry_hasta = ttk.Entry(self.frame_filtros, width=15)
        self.entry_hasta.grid(row=0, column=3, padx=5, pady=5)

        self.btn_filtrar = ttk.Button(self.frame_filtros, text="🔍 Filtrar", command=self.filtrar_ventas)
        self.btn_filtrar.grid(row=0, column=4, padx=5, pady=5)

        columnas = ("fecha", "producto", "cantidad", "precio", "total")
        self.tabla_reportes = ttk.Treeview(self.tab_reportes, columns=columnas, show="headings")
        for col in columnas:
            self.tabla_reportes.heading(col, text=col.capitalize())
            self.tabla_reportes.column(col, width=100)
            
        self.tabla_reportes.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.frame_botones_reportes = ttk.Frame(self.tab_reportes, padding="10")
        self.frame_botones_reportes.pack(pady=10, fill=tk.X)

        self.btn_actualizar = ttk.Button(self.frame_botones_reportes, text="🔄 Actualizar Reportes", command=self.actualizar_reportes)
        self.btn_actualizar.pack(side=tk.LEFT, padx=5)


        self.btn_reporte_resumido = ttk.Button(self.frame_botones_reportes, text="📊 Reporte Resumido", command=self.reporte_resumido)
        self.btn_reporte_resumido.pack(side=tk.LEFT, padx=5)

        self.cargar_historial_ventas()
        self.actualizar_tabla_reportes()

    def actualizar_reportes(self):
        self.cargar_historial_ventas()
        self.actualizar_tabla_reportes()
        messagebox.showinfo("Actualizado", "Los reportes se han actualizado con éxito.")


    def cargar_historial_ventas(self):
        self.cursor.execute("""
            SELECT v.fecha, p.nombre AS producto, dv.cantidad, p.precio_unitario,
                   (dv.cantidad * p.precio_unitario) AS total
            FROM detalle_ventas dv
            JOIN ventas v ON dv.id_venta = v.id_venta
            JOIN productos p ON dv.id_producto = p.id_producto
         
            ORDER BY v.fecha DESC
        """)
        self.historial_ventasventas = [
            {
                "fecha": venta["fecha"].strftime("%d/%m/%Y"),
                "nombre": venta["producto"],
                "cantidad": venta["cantidad"],
                "precio": float(venta["precio_unitario"]),
                "total": float(venta["total"])
            } for venta in self.cursor.fetchall()
        ]

    def actualizar_tabla_reportes(self):
        for item in self.tabla_reportes.get_children():
            self.tabla_reportes.delete(item)
        for venta in self.historial_ventasventas:
            self.tabla_reportes.insert("", "end", values=(
                venta["fecha"], venta["nombre"], venta["cantidad"],
                f"${venta['precio']:.2f}", f"${venta['total']:.2f}"
            ))

    def filtrar_ventas(self):
        desde = self.entry_desde.get().strip()
        hasta = self.entry_hasta.get().strip()

        try:
            fecha_desde = datetime.strptime(desde, "%d/%m/%Y").date() if desde else datetime.min.date()
            fecha_hasta = datetime.strptime(hasta, "%d/%m/%Y").date() if hasta else datetime.max.date()

            self.tabla_reportes.delete(*self.tabla_reportes.get_children())

            for venta in self.historial_ventasventas:
                fecha_venta = datetime.strptime(venta["fecha"], "%d/%m/%Y").date()
                if fecha_desde <= fecha_venta <= fecha_hasta:
                    self.tabla_reportes.insert("", "end", values=(
                    venta["fecha"], venta["nombre"], venta["cantidad"],
                    f"${venta['precio']:.2f}", f"${venta['total']:.2f}"
                ))
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Use dd/mm/yyyy")


    def reporte_resumido(self):
        if not self.tabla_reportes.get_children():
            messagebox.showwarning("Sin datos", "No hay ventas para resumir. Usa el botón 'Filtrar' o 'Actualizar' primero.")
            return

        total_ventas = 0
        total_productos = 0
        total_ingresos = 0.0

        for item in self.tabla_reportes.get_children():
            valores = self.tabla_reportes.item(item)["values"]
            if len(valores) >= 5:
                print("Valores:", valores)
                try:
                    cantidad = int(valores[2])
                    ingreso = float(valores[4].replace("$", "").replace(",", ""))
                    total_ventas += 1
                    total_productos += cantidad
                    total_ingresos += ingreso
                except (ValueError, IndexError) as e:
                    print("Error al procesar fila:", valores, "->", e)

        resumen = (
        f"Total de Ventas: {total_ventas}\n"
        f"Total de Productos Vendidos: {total_productos}\n"
        f"Total de Ingresos: ${total_ingresos:.2f}"
        )

        messagebox.showinfo("Reporte Resumido", resumen)

    # 📝 Crear PDF del resumen
        fecha_actual = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        nombre_archivo = f"reporte_resumido_{fecha_actual}.pdf"
        c = canvas.Canvas(nombre_archivo, pagesize=A4)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(2 * cm, 27 * cm, "Reporte Resumido de Ventas")

        c.setFont("Helvetica", 12)
        c.drawString(2 * cm, 25.5 * cm, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        c.drawString(2 * cm, 24.7 * cm, f"Usuario: {self.usuario_nombre}")

        c.drawString(2 * cm, 24 * cm, f"Total de Ventas: {total_ventas}")
        c.drawString(2 * cm, 23 * cm, f"Total de Productos Vendidos: {total_productos}")
        c.drawString(2 * cm, 22 * cm, f"Total de Ingresos: ${total_ingresos:.2f}")

        c.save()
        messagebox.showinfo("PDF generado", f"Reporte resumido guardado como:\n{nombre_archivo}")
        # Abrir el PDF automáticamente
        try:
            if platform.system() == "Windows":
                os.startfile(nombre_archivo)
      
        except Exception as e:
            messagebox.showerror("Error al abrir el PDF", str(e))
   

    
if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaLogin(root)
    root.mainloop()
