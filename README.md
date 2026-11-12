# Proyecto de Mate Discreta - Sistema criptográfico RSA

Aplicación gráfica educativa que permite encriptar y desencriptar mensajes
utilizando el sistema criptográfico RSA. La aplicación muestra los valores y
bloques generados durante cada operación para facilitar la comprensión del
procedimiento matemático.

## Grupo 2

### Integrantes

- **Sebastián Garxía** - Lógica RSA
- **Gabriel Zambrano** - Interfaz y documentación

### Versión recomendada

- Python 3.10 o posterior.
- La interfaz utiliza Tkinter, incluido normalmente con Python.
- No es necesario instalar librerías externas.

### Archivos principales

```text
main.py        Interfaz gráfica y archivo principal de ejecución.
rsa_logic.py   Algoritmos matemáticos, validaciones y operaciones RSA.
pruebas.py     Comprobaciones de la implementación, si está incluido.
README.md      Información rápida del proyecto.
```

### Instrucciones de ejecución

1. Colocar `main.py` y `rsa_logic.py` en la misma carpeta.
2. Abrir una terminal en la carpeta del proyecto.
3. Ejecutar:

```bash
python main.py
```

En algunos sistemas se debe utilizar:

```bash
python3 main.py
```

### Uso básico

1. En la pestaña **Encriptar**, escribir el mensaje e ingresar los valores de
   `p`, `q` y `e`.
2. Presionar **Encriptar mensaje** para obtener el mensaje cifrado `C`, la
   longitud original `L` y los bloques utilizados.
3. Utilizar el botón **Copiar C y L a Desencriptar** para transferir los datos.
4. En la pestaña **Desencriptar**, presionar **Desencriptar mensaje** para
   recuperar el texto original.

Si algún dato no es válido, la aplicación muestra un mensaje de error sin
cerrarse. Los archivos `main.py` y `rsa_logic.py` deben permanecer en la misma
carpeta para que la interfaz pueda utilizar las funciones de encriptación y
descifrado.
