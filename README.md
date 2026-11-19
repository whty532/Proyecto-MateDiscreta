# Cifrado RSA

Programa con interfaz gráfica para encriptar y desencriptar mensajes con RSA.
Proyecto 3 de MM2015 Matemática Discreta 1, Universidad del Valle de Guatemala.

## Integrantes - Grupo 2

- Estuardo Sebastián García de León
- Gabriel Zambrano

## Versión de Python y dependencias

- Python 3.10 o posterior.
- Solo se usa la biblioteca estándar (Tkinter ya viene con Python). No hay que instalar
  nada; por eso `requirements.txt` no tiene librerías.
- En Linux, si falta Tkinter: `sudo apt install python3-tk`.

## Cómo ejecutar

En una terminal, dentro de la carpeta del proyecto:

```bash
python main.py      # abre el programa
python pruebas.py   # corre las comprobaciones
```

Si `python` no funciona, usar `python3` o `py`.

## Archivos

- `main.py`: interfaz gráfica (archivo principal).
- `rsa_logic.py`: algoritmos, validaciones, encriptación y desencriptación.
- `pruebas.py`: comprobaciones automáticas.

## Uso

**Encriptar**

1. En la pestaña **Encriptar**, escribir el mensaje M, p, q y e. El botón
   **Ejemplo RSA** llena el ejemplo del enunciado.
2. Presionar **Encriptar**.
3. **C** aparece en el recuadro *Resultado*, en el campo *Cifrado C*, y **L** justo debajo,
   en *Longitud L*. En *Valores calculados* están n, φ, MCD(e, φ), la llave pública (e, n)
   y si hubo relleno. En *Proceso* se ven los códigos ASCII y los bloques antes y después.

**Desencriptar**

1. Ingresar C y L con el botón **Pasar a Desencriptar**, o a mano: usar **Copiar C**,
   pegar C en *Cifrado C* y escribir L en *Longitud L*. C son bloques de 6 dígitos
   separados por espacios, por ejemplo `026054 123875`.
2. Escribir los mismos p, q y e, y presionar **Desencriptar**.
3. El mensaje aparece en *Resultado* entre comillas, para que se vean los espacios del
   inicio y del final. En *Valores calculados* se muestran n, φ y d.

Si un dato no es válido, aparece un mensaje de error con la causa y el programa sigue abierto.

## Relleno

Cada bloque lleva dos caracteres. Si L es impar, se agrega un espacio (032) al final
antes de encriptar. Al desencriptar, si L es impar se quita solo ese último espacio;
si L es par no se quita nada. Así se conservan los espacios originales del mensaje.

## Ejemplo completo

| Dato | Valor |
|---|---|
| Mensaje, p, q, e | "RSA", 367, 373, 17 |
| n, φ, MCD(e, φ) | 136891, 136152, 1 |
| L y relleno | 3, se usa "RSA " |
| Bloques m | 082083 065032 |
| Cifrado C | 026054 123875 |
| d | 8009 |
| Mensaje recuperado | "RSA" |

## Algoritmos

Están en `rsa_logic.py` y siguen los métodos vistos en clase. No se usa `math.gcd`,
`pow` ni librerías de criptografía.

| Algoritmo | Función | Método |
|---|---|---|
| Primalidad | `es_primo` | División de prueba hasta la raíz de n. |
| MCD | `mcd` | Algoritmo de Euclides. |
| Inverso modular | `inverso_modular` | Euclides y lema de Bézout con matrices; da d con 1 ≤ d < φ. |
| Exponenciación modular | `exp_modular` | Algoritmo recursivo que reduce módulo n en cada paso. |

## Comprobaciones

`pruebas.py` tiene 32 comprobaciones y todas pasan. Revisan:

- Los algoritmos con ejemplos de los apuntes y el ejemplo del enunciado.
- La recuperación de mensajes de longitud par e impar, con mayúsculas, minúsculas,
  números, signos, espacios seguidos, espacios al inicio y al final, y bloques cifrados
  con ceros iniciales.
- El rechazo de p o q no primos, p = q, n fuera de 126126 < n < 1000000, e inválido,
  caracteres no permitidos (ñ, tildes, saltos de línea), bloques mal formados, c ≥ n
  y L incoherente.

## Video

PEGAR_AQUI_EL_ENLACE
