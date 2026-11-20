"""Cifrado RSA - interfaz gráfica del Proyecto 3 de MM2015 Matemática Discreta 1"""

import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, ttk

import rsa_logic

TITULO = "Cifrado RSA - MM2015 Matemática Discreta 1"
EJEMPLO = {"mensaje": "RSA", "p": "367", "q": "373", "e": "17"}

# Grises neutros
BLANCO = "#FFFFFF"
BORDE = "#ABADB3"
FILA_ALTERNA = "#F4F4F4"
FILA_RELLENO = "#E0E0E0"
TEXTO = "#1A1A1A"
TEXTO_SUAVE = "#5F5F5F"
TEXTO_ERROR = "#A31515"

NOTA_COMILLAS = "Las comillas solo marcan dónde empieza y termina el mensaje."

AYUDA = (
    "Encriptar\n"
    "1. Escriba el mensaje M y los valores de p, q y e.\n"
    "2. Presione Encriptar. El cifrado C y la longitud L aparecen en Resultado.\n"
    "3. Use Pasar a Desencriptar para llevar C, L, p, q y e a la otra pestaña.\n\n"
    "Desencriptar\n"
    "1. Escriba C (bloques de 6 dígitos separados por espacios), L, p, q y e.\n"
    "2. Presione Desencriptar. El mensaje recuperado aparece en Resultado.\n\n"
    "Si L es impar, al encriptar se agrega un espacio de relleno al final y al "
    "desencriptar se quita solo ese espacio."
)

ACERCA_DE = (
    "Cifrado RSA\n"
    "Proyecto 3 - MM2015 Matemática Discreta 1\n"
    "Universidad del Valle de Guatemala\n\n"
    "Grupo 2:\n"
    "Estuardo Sebastián García de León\n"
    "Gabriel Zambrano\n\n"
    "Hecho en Python con Tkinter."
)


def elegir_fuente(opciones, respaldo):
    """Usa la primera fuente instalada de la lista; si no hay ninguna, el respaldo."""
    instaladas = set(tkfont.families())
    for nombre in opciones:
        if nombre in instaladas:
            return nombre
    return respaldo


def mostrar_caracter(caracter):
    """Hace visibles los espacios en las tablas."""
    nombre = rsa_logic.nombre_caracter(caracter)
    return f"({nombre})" if nombre != caracter else caracter


def limpiar_tabla(tabla):
    for fila in tabla.get_children():
        tabla.delete(fila)


def etiqueta_fila(numero, es_relleno=False):
    if es_relleno:
        return ("relleno",)
    return ("alterna",) if numero % 2 == 1 else ()



# Piezas reutilizables de la interfaz

class PanelValores(ttk.Frame):
    """Lista de valores calculados: nombre a la izquierda y valor a la derecha"""

    def __init__(self, padre, filas):
        super().__init__(padre)
        self.valores = {}
        for numero, (clave, etiqueta) in enumerate(filas):
            ttk.Label(self, text=etiqueta).grid(row=numero, column=0, sticky="w", pady=1)
            variable = tk.StringVar(value="-")
            ttk.Label(self, textvariable=variable, style="Valor.TLabel").grid(
                row=numero, column=1, sticky="w", padx=(12, 0), pady=1
            )
            self.valores[clave] = variable

    def mostrar(self, datos):
        for clave, valor in datos.items():
            self.valores[clave].set(valor)

    def limpiar(self):
        for variable in self.valores.values():
            variable.set("-")


def crear_caja_texto(padre, app, alto, solo_lectura):
    """Caja de texto de varias líneas con el aspecto de un campo normal."""
    caja = tk.Text(
        padre, height=alto, width=10, wrap="word", font=(app.fuente_numeros, 12),
        background=BLANCO, foreground=TEXTO, relief="flat", borderwidth=0,
        highlightthickness=1, highlightbackground=BORDE, highlightcolor=BORDE,
        insertbackground=TEXTO, padx=6, pady=4,
    )
    if solo_lectura:
        caja.configure(state="disabled", cursor="arrow")
    return caja


def escribir_texto(caja, contenido):
    caja.configure(state="normal")
    caja.delete("1.0", "end")
    caja.insert("1.0", contenido)
    caja.configure(state="disabled")


def crear_tabla(padre, titulo, columnas):
    """Crea una tabla con título y barra de desplazamiento.

    columnas: lista de (clave, encabezado, ancho).
    """
    marco = ttk.Frame(padre)
    ttk.Label(marco, text=titulo).pack(anchor="w", pady=(0, 4))
    contenedor = ttk.Frame(marco)
    contenedor.pack(fill="both", expand=True)

    tabla = ttk.Treeview(contenedor, columns=[c[0] for c in columnas], show="headings", selectmode="none", height=6)
    for clave, encabezado, ancho in columnas:
        tabla.heading(clave, text=encabezado)
        tabla.column(clave, width=ancho, minwidth=40, anchor="center", stretch=True)
    tabla.tag_configure("alterna", background=FILA_ALTERNA)
    tabla.tag_configure("relleno", background=FILA_RELLENO)

    barra = ttk.Scrollbar(contenedor, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=barra.set)
    tabla.pack(side="left", fill="both", expand=True)
    barra.pack(side="right", fill="y")
    return marco, tabla


def crear_campo(padre, fila, texto, variable, accion):
    """Etiqueta y campo en una fila del formulario. Enter ejecuta la acción."""
    ttk.Label(padre, text=texto).grid(row=fila, column=0, sticky="w", pady=2, padx=(0, 8))
    entrada = ttk.Entry(padre, textvariable=variable, width=12)
    entrada.grid(row=fila, column=1, sticky="ew", pady=2)
    entrada.bind("<Return>", lambda _: accion())
    return entrada


def armar_pestana(pestana):
    """Distribución común: Datos y Valores a la izquierda, Resultado y Proceso a la derecha."""
    pestana.columnconfigure(0, minsize=400)
    pestana.columnconfigure(1, weight=1)
    pestana.rowconfigure(0, weight=1)

    izquierda = ttk.Frame(pestana)
    izquierda.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
    derecha = ttk.Frame(pestana)
    derecha.grid(row=0, column=1, sticky="nsew")

    datos = ttk.LabelFrame(izquierda, text="Datos", padding=(10, 8))
    datos.pack(fill="x")
    datos.columnconfigure(1, weight=1)

    valores = ttk.LabelFrame(izquierda, text="Valores calculados", padding=(10, 8))
    valores.pack(fill="x", pady=(10, 0))

    resultado = ttk.LabelFrame(derecha, text="Resultado", padding=10)
    resultado.pack(fill="x")
    resultado.columnconfigure(1, weight=1)

    proceso = ttk.LabelFrame(derecha, text="Proceso", padding=10)
    proceso.pack(fill="both", expand=True, pady=(10, 0))
    proceso.columnconfigure((0, 1), weight=1)
    proceso.rowconfigure(0, weight=1)
    return datos, valores, resultado, proceso


# Pestaña Encriptar

class PestanaEncriptar(ttk.Frame):

    def __init__(self, padre, app):
        super().__init__(padre, padding=10)
        self.app = app
        self.mensaje = tk.StringVar()
        self.p = tk.StringVar()
        self.q = tk.StringVar()
        self.e = tk.StringVar()
        self.longitud = tk.StringVar()
        self.ultimo = None

        datos, valores, resultado, proceso = armar_pestana(self)
        self._crear_datos(datos)
        self.panel = PanelValores(valores, [
            ("n", "n = p · q:"),
            ("phi", "φ = (p − 1)(q − 1):"),
            ("mcd", "MCD(e, φ):"),
            ("llave", "Llave pública (e, n):"),
            ("L", "Longitud L:"),
            ("relleno", "Relleno:"),
        ])
        self.panel.pack(anchor="w", fill="x")
        self._crear_resultado(resultado)
        self._crear_proceso(proceso)

        self.mensaje.trace_add("write", self._contar_caracteres)
        self._contar_caracteres()

    def _crear_datos(self, datos):
        entrada = crear_campo(datos, 0, "Mensaje M:", self.mensaje, self.encriptar)
        entrada.configure(font=(self.app.fuente_numeros, 11))
        self.contador = ttk.Label(datos, style="Pista.TLabel")
        self.contador.grid(row=1, column=1, sticky="w", pady=(0, 4))
        crear_campo(datos, 2, "Primo p:", self.p, self.encriptar)
        crear_campo(datos, 3, "Primo q:", self.q, self.encriptar)
        crear_campo(datos, 4, "Exponente e:", self.e, self.encriptar)

        botones = ttk.Frame(datos)
        botones.grid(row=5, column=0, columnspan=2, sticky="e", pady=(10, 0))
        ttk.Button(botones, text="Encriptar", default="active", command=self.encriptar).pack(side="left")
        ttk.Button(botones, text="Ejemplo RSA", command=self.cargar_ejemplo).pack(side="left", padx=6)
        ttk.Button(botones, text="Limpiar", command=self.limpiar).pack(side="left")

    def _crear_resultado(self, resultado):
        ttk.Label(resultado, text="Cifrado C:").grid(row=0, column=0, sticky="nw", pady=3, padx=(0, 10))
        self.caja_c = crear_caja_texto(resultado, self.app, 3, solo_lectura=True)
        self.caja_c.grid(row=0, column=1, columnspan=3, sticky="ew", pady=3)

        ttk.Label(resultado, text="Longitud L:").grid(row=1, column=0, sticky="w", pady=3, padx=(0, 10))
        ttk.Entry(resultado, textvariable=self.longitud, width=8, state="readonly", font=(self.app.fuente_numeros, 11)).grid(row=1, column=1, sticky="w", pady=3)
        ttk.Button(resultado, text="Copiar C", command=self.copiar_c).grid(row=1, column=2, sticky="e", padx=6)
        ttk.Button(resultado, text="Pasar a Desencriptar", command=self.pasar_a_desencriptar).grid(row=1, column=3, sticky="e")

    def _crear_proceso(self, proceso):
        marco, self.tabla_ascii = crear_tabla(proceso, "Caracteres y código ASCII", [
            ("pos", "Posición", 70), ("car", "Carácter", 100), ("ascii", "ASCII", 60),
        ])
        marco.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        marco, self.tabla_bloques = crear_tabla(proceso, "Bloques antes y después", [
            ("num", "Bloque", 60), ("pareja", "Pareja", 70), ("m", "m (antes)", 90), ("c", "c (después)", 90),
        ])
        marco.grid(row=0, column=1, sticky="nsew")


    # acciones 

    def _contar_caracteres(self, *_):
        L = len(self.mensaje.get())
        if L == 0:
            texto = "L = 0"
        elif L % 2 == 1:
            texto = f"L = {L}, impar: lleva relleno"
        else:
            texto = f"L = {L}, par: sin relleno"
        self.contador.configure(text=texto)

    def encriptar(self):
        try:
            r = rsa_logic.encriptar(self.mensaje.get(), self.p.get(), self.q.get(), self.e.get())
        except ValueError as error:
            self.limpiar_resultados()
            self.app.mostrar_error(str(error))
            return

        self.ultimo = r
        escribir_texto(self.caja_c, r["C"])
        self.longitud.set(str(r["L"]))
        self.panel.mostrar({
            "n": r["n"],
            "phi": r["phi"],
            "mcd": r["mcd"],
            "llave": f"({r['e']}, {r['n']})",
            "L": r["L"],
            "relleno": "Sí, un espacio" if r["relleno"] else "No, L es par",
        })

        limpiar_tabla(self.tabla_ascii)
        ultimo = len(r["caracteres"]) - 1
        for i, (caracter, codigo) in enumerate(r["caracteres"]):
            es_relleno = r["relleno"] and i == ultimo
            nombre = "(relleno)" if es_relleno else mostrar_caracter(caracter)
            self.tabla_ascii.insert("", "end", values=(i + 1, nombre, f"{codigo:03d}"),
                                    tags=etiqueta_fila(i, es_relleno))

        limpiar_tabla(self.tabla_bloques)
        for i, bloque in enumerate(r["bloques"]):
            self.tabla_bloques.insert("", "end", tags=etiqueta_fila(i), values=(
                i + 1, f"\"{bloque['pareja']}\"", f"{bloque['m']:06d}", f"{bloque['c']:06d}",
            ))

        self.app.mostrar_estado(f"Mensaje encriptado en {len(r['bloques'])} bloque(s). L = {r['L']}.")

    def copiar_c(self):
        if not self.ultimo:
            self.app.mostrar_error("Primero encripte un mensaje.")
            return
        self.app.clipboard_clear()
        self.app.clipboard_append(self.ultimo["C"])
        self.app.mostrar_estado("C copiado al portapapeles.")

    def pasar_a_desencriptar(self):
        if not self.ultimo:
            self.app.mostrar_error("Primero encripte un mensaje.")
            return
        self.app.pestana_desencriptar.recibir(self.ultimo)

    def cargar_ejemplo(self):
        self.mensaje.set(EJEMPLO["mensaje"])
        self.p.set(EJEMPLO["p"])
        self.q.set(EJEMPLO["q"])
        self.e.set(EJEMPLO["e"])
        self.app.pestanas.select(self)
        self.app.mostrar_estado("Ejemplo del enunciado cargado: \"RSA\" con p = 367, q = 373 y e = 17.")

    def limpiar_resultados(self):
        self.ultimo = None
        escribir_texto(self.caja_c, "")
        self.longitud.set("")
        self.panel.limpiar()
        limpiar_tabla(self.tabla_ascii)
        limpiar_tabla(self.tabla_bloques)

    def limpiar(self):
        for variable in (self.mensaje, self.p, self.q, self.e):
            variable.set("")
        self.limpiar_resultados()
        self.app.mostrar_estado("Datos de Encriptar borrados.")


# Pestaña Desencriptar

class PestanaDesencriptar(ttk.Frame):

    def __init__(self, padre, app):
        super().__init__(padre, padding=10)
        self.app = app
        self.L = tk.StringVar()
        self.p = tk.StringVar()
        self.q = tk.StringVar()
        self.e = tk.StringVar()

        datos, valores, resultado, proceso = armar_pestana(self)
        self._crear_datos(datos)
        self.panel = PanelValores(valores, [
            ("n", "n = p · q:"),
            ("phi", "φ = (p − 1)(q − 1):"),
            ("d", "Exponente privado d:"),
            ("prueba", "Comprobación e · d mod φ:"),
            ("llave", "Llave privada (d, n):"),
            ("relleno", "Relleno:"),
        ])
        self.panel.pack(anchor="w", fill="x")
        self._crear_resultado(resultado)
        self._crear_proceso(proceso)

    def _crear_datos(self, datos):
        ttk.Label(datos, text="Cifrado C:").grid(row=0, column=0, sticky="nw", pady=3, padx=(0, 8))
        self.entrada_c = crear_caja_texto(datos, self.app, 3, solo_lectura=False)
        self.entrada_c.configure(font=(self.app.fuente_numeros, 11))
        self.entrada_c.grid(row=0, column=1, sticky="ew", pady=3)
        ttk.Label(datos, text="Bloques de 6 dígitos", style="Pista.TLabel").grid(row=1, column=1, sticky="w", pady=(0, 4))
        crear_campo(datos, 2, "Longitud L:", self.L, self.desencriptar)
        crear_campo(datos, 3, "Primo p:", self.p, self.desencriptar)
        crear_campo(datos, 4, "Primo q:", self.q, self.desencriptar)
        crear_campo(datos, 5, "Exponente e:", self.e, self.desencriptar)

        botones = ttk.Frame(datos)
        botones.grid(row=6, column=0, columnspan=2, sticky="e", pady=(10, 0))
        ttk.Button(botones, text="Desencriptar", default="active", command=self.desencriptar).pack(side="left")
        ttk.Button(botones, text="Limpiar", command=self.limpiar).pack(side="left", padx=(6, 0))

    def _crear_resultado(self, resultado):
        ttk.Label(resultado, text="Mensaje M:").grid(row=0, column=0, sticky="nw", pady=3, padx=(0, 10))
        self.caja_m = crear_caja_texto(resultado, self.app, 2, solo_lectura=True)
        self.caja_m.grid(row=0, column=1, sticky="ew", pady=3)
        self.detalle = ttk.Label(resultado, style="Pista.TLabel", text=NOTA_COMILLAS)
        self.detalle.grid(row=1, column=1, sticky="w", pady=(2, 0))

    def _crear_proceso(self, proceso):
        marco, self.tabla_bloques = crear_tabla(proceso, "Bloques antes y después", [
            ("num", "Bloque", 60), ("c", "c (antes)", 90), ("m", "m (después)", 90), ("pareja", "Pareja", 70),
        ])
        marco.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        marco, self.tabla_ascii = crear_tabla(proceso, "Código ASCII y caracteres", [
            ("pos", "Posición", 70), ("ascii", "ASCII", 60), ("car", "Carácter", 100),
        ])
        marco.grid(row=0, column=1, sticky="nsew")

    # --- acciones -----------------------------------------------------------

    def recibir(self, resultado):
        """Recibe C, L, p, q y e desde la pestaña Encriptar."""
        self.entrada_c.delete("1.0", "end")
        self.entrada_c.insert("1.0", resultado["C"])
        self.L.set(str(resultado["L"]))
        self.p.set(str(resultado["p"]))
        self.q.set(str(resultado["q"]))
        self.e.set(str(resultado["e"]))
        self.limpiar_resultados()
        self.app.pestanas.select(self)
        self.app.mostrar_estado("C, L, p, q y e pasaron a Desencriptar. Presione Desencriptar.")

    def desencriptar(self):
        cifrado = self.entrada_c.get("1.0", "end-1c")
        try:
            r = rsa_logic.desencriptar(cifrado, self.L.get(), self.p.get(), self.q.get(), self.e.get())
        except ValueError as error:
            self.limpiar_resultados()
            self.app.mostrar_error(str(error))
            return

        escribir_texto(self.caja_m, f"\"{r['mensaje']}\"")
        quitado = "Se quitó el espacio de relleno." if r["relleno"] else "No había relleno."
        self.detalle.configure(
            text=f"{len(r['mensaje'])} caracteres, igual a L = {r['L']}. {quitado}\n{NOTA_COMILLAS}"
        )
        self.panel.mostrar({
            "n": r["n"],
            "phi": r["phi"],
            "d": r["d"],
            "prueba": (r["e"] * r["d"]) % r["phi"],
            "llave": f"({r['d']}, {r['n']})",
            "relleno": f"Sí, L = {r['L']} impar" if r["relleno"] else f"No, L = {r['L']} par",
        })

        limpiar_tabla(self.tabla_bloques)
        for i, bloque in enumerate(r["bloques"]):
            self.tabla_bloques.insert("", "end", tags=etiqueta_fila(i), values=(
                i + 1, f"{bloque['c']:06d}", f"{bloque['m']:06d}", f"\"{bloque['pareja']}\"",
            ))

        limpiar_tabla(self.tabla_ascii)
        ultimo = len(r["caracteres"]) - 1
        for i, (caracter, codigo) in enumerate(r["caracteres"]):
            es_relleno = r["relleno"] and i == ultimo
            nombre = "(relleno)" if es_relleno else mostrar_caracter(caracter)
            self.tabla_ascii.insert("", "end", values=(i + 1, f"{codigo:03d}", nombre),
                                    tags=etiqueta_fila(i, es_relleno))

        self.app.mostrar_estado(
            f"Mensaje recuperado: {r['k']} bloque(s) con d = {r['d']}, {len(r['mensaje'])} caracteres."
        )

    def limpiar_resultados(self):
        escribir_texto(self.caja_m, "")
        self.detalle.configure(text=NOTA_COMILLAS)
        self.panel.limpiar()
        limpiar_tabla(self.tabla_bloques)
        limpiar_tabla(self.tabla_ascii)

    def limpiar(self):
        self.entrada_c.delete("1.0", "end")
        for variable in (self.L, self.p, self.q, self.e):
            variable.set("")
        self.limpiar_resultados()
        self.app.mostrar_estado("Datos de Desencriptar borrados.")


# ---------------------------------------------------------------------------
# Ventana principal
# ---------------------------------------------------------------------------

class AplicacionRSA(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title(TITULO)
        ancho = min(1180, self.winfo_screenwidth() - 60)
        alto = min(740, self.winfo_screenheight() - 130)
        self.geometry(f"{ancho}x{alto}+30+20")
        self.minsize(1040, 600)

        self.fuente_numeros = elegir_fuente(["Consolas", "Menlo", "DejaVu Sans Mono"], "Courier")
        self._configurar_estilos()
        self._crear_menu()
        self._crear_barra_estado()
        self._crear_pestanas()

    def _configurar_estilos(self):
        """Usa el tema nativo del sistema (Windows o macOS) y lo deja en grises en Linux."""
        estilo = ttk.Style(self)
        for tema in ("vista", "aqua", "clam"):
            if tema in estilo.theme_names():
                estilo.theme_use(tema)
                break
        if estilo.theme_use() == "clam":
            estilo.configure(".", background="#F0F0F0")
            estilo.configure("Treeview.Heading", background="#E5E5E5")

        # En Windows la letra del sistema es de 9 puntos; 10 se lee mejor en el video
        for nombre in ("TkDefaultFont", "TkTextFont", "TkHeadingFont", "TkMenuFont"):
            fuente = tkfont.nametofont(nombre)
            if 0 < fuente.cget("size") < 10:
                fuente.configure(size=10)

        estilo.configure("Treeview", rowheight=24, font=(self.fuente_numeros, 10))
        estilo.configure("Valor.TLabel", font=(self.fuente_numeros, 10, "bold"))
        estilo.configure("Pista.TLabel", foreground=TEXTO_SUAVE)
        estilo.configure("Estado.TLabel", relief="sunken", padding=(6, 3))
        estilo.configure("Error.TLabel", relief="sunken", padding=(6, 3), foreground=TEXTO_ERROR)
        self.configure(background=estilo.lookup("TFrame", "background"))

    def _crear_menu(self):
        barra = tk.Menu(self)
        ayuda = tk.Menu(barra, tearoff=False)
        ayuda.add_command(label="Cómo usar", command=lambda: messagebox.showinfo("Cómo usar", AYUDA, parent=self))
        ayuda.add_command(label="Acerca de", command=lambda: messagebox.showinfo("Acerca de", ACERCA_DE, parent=self))
        barra.add_cascade(label="Ayuda", menu=ayuda)
        self.configure(menu=barra)

    def _crear_pestanas(self):
        self.pestanas = ttk.Notebook(self)
        self.pestanas.pack(fill="both", expand=True, padx=8, pady=(8, 4))
        self.pestana_encriptar = PestanaEncriptar(self.pestanas, self)
        self.pestana_desencriptar = PestanaDesencriptar(self.pestanas, self)
        self.pestanas.add(self.pestana_encriptar, text="Encriptar")
        self.pestanas.add(self.pestana_desencriptar, text="Desencriptar")

    def _crear_barra_estado(self):
        """Barra inferior con el último aviso. Se crea antes que las pestañas para que quede abajo."""
        self.estado = ttk.Label(self, style="Estado.TLabel",
                                text="Listo. El botón Ejemplo RSA llena los datos del ejemplo del enunciado.")
        self.estado.pack(side="bottom", fill="x")
        self.estado.bind("<Configure>", lambda evento: self.estado.configure(wraplength=evento.width - 20))

    def mostrar_estado(self, texto):
        self.estado.configure(text=texto, style="Estado.TLabel")

    def mostrar_error(self, texto):
        """Muestra el error en la barra y en un cuadro de diálogo, sin cerrar el programa."""
        self.estado.configure(text=f"Error: {texto}", style="Error.TLabel")
        messagebox.showerror("Dato inválido", texto, parent=self)


if __name__ == "__main__":
    AplicacionRSA().mainloop()
