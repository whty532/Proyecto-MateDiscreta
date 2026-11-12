"""Interfaz gráfica para el proyecto educativo de criptografía RSA.

La lógica matemática debe estar implementada en ``rsa_logic.py`` mediante las
funciones ``encriptar`` y ``desencriptar`` acordadas por el equipo.
"""

from importlib import import_module
import tkinter as tk
from itertools import zip_longest
from tkinter import messagebox, ttk
from types import SimpleNamespace

try:
    rsa_logic = import_module("rsa_logic")
except ImportError:
    rsa_logic = SimpleNamespace(desencriptar=None, encriptar=None)


COLOR_FONDO = "#f4f7fb"
COLOR_PRIMARIO = "#173f73"
COLOR_SECUNDARIO = "#2563a6"
COLOR_TEXTO = "#172033"


def representar_caracter(caracter):
    """Muestra de forma visible espacios y otros caracteres especiales."""
    equivalencias = {
        " ": "␠ (espacio)",
        "\n": "\\n",
        "\t": "\\t",
    }
    return equivalencias.get(caracter, caracter)


def limpiar_tabla(tabla):
    for elemento in tabla.get_children():
        tabla.delete(elemento)


def escribir_texto(caja, contenido):
    caja.configure(state="normal")
    caja.delete("1.0", "end")
    caja.insert("1.0", str(contenido))
    caja.configure(state="disabled")


class AplicacionRSA(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora RSA - Matemática Discreta 1")
        self.geometry("1180x760")
        self.minsize(960, 650)
        self.configure(background=COLOR_FONDO)

        self.ultimo_cifrado = ""
        self.ultima_longitud = ""

        self._configurar_estilos()
        self._crear_encabezado()
        self._crear_pestanas()

    def _configurar_estilos(self):
        estilo = ttk.Style(self)
        if "clam" in estilo.theme_names():
            estilo.theme_use("clam")

        estilo.configure("TFrame", background=COLOR_FONDO)
        estilo.configure("TLabel", background=COLOR_FONDO, foreground=COLOR_TEXTO)
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 21, "bold"), foreground=COLOR_PRIMARIO)
        estilo.configure("Subtitulo.TLabel", font=("Segoe UI", 10), foreground="#526079")
        estilo.configure("Seccion.TLabelframe", background=COLOR_FONDO, padding=12)
        estilo.configure(
            "Seccion.TLabelframe.Label",
            background=COLOR_FONDO,
            foreground=COLOR_PRIMARIO,
            font=("Segoe UI", 11, "bold"),
        )
        estilo.configure("Accion.TButton", font=("Segoe UI", 10, "bold"), padding=(14, 9))
        estilo.configure("Treeview", rowheight=25, font=("Segoe UI", 9))
        estilo.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        estilo.configure("TNotebook", background=COLOR_FONDO, borderwidth=0)
        estilo.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=(18, 9))

    def _crear_encabezado(self):
        encabezado = ttk.Frame(self, padding=(22, 16, 22, 8))
        encabezado.pack(fill="x")
        ttk.Label(encabezado, text="Calculadora del sistema criptográfico RSA", style="Titulo.TLabel").pack(
            anchor="w"
        )
        ttk.Label(
            encabezado,
            text="Cifrado y descifrado educativo mediante aritmética modular",
            style="Subtitulo.TLabel",
        ).pack(anchor="w", pady=(3, 0))

    def _crear_pestanas(self):
        contenedor = ttk.Frame(self, padding=(20, 6, 20, 18))