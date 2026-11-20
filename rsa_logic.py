"""Lógica del sistema criptográfico RSA - Proyecto 3, MM2015 Matemática Discreta 1 """

ASCII_MIN = 32          # espacio
ASCII_MAX = 126         # ~
N_MIN = 126126          # n debe ser mayor, el bloque más grande posible es 126126
N_MAX = 1000000         # n debe ser menor, así cada bloque cifrado cabe en 6 dígitos
DIGITOS_BLOQUE = 6
DIGITOS = "0123456789"


def es_primo(n):
    """Indica si n es primo usando división de prueba

    Si ningún número entre 2 y la raíz de n lo divide, n es primo
    """
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def mcd(a, b):
    """Máximo común divisor con el algoritmo de Euclides

    Se escribe a = q*b + r y se cambia (a, b) por (b, r) hasta que el
    residuo sea 0. El último divisor distinto de 0 es el MCD.
    """
    while b != 0:
        r = a % b
        a = b
        b = r
    return a


def multiplicar_matrices(A, B):
    """Producto de dos matrices de 2x2"""
    return [
        [A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]],
        [A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]],
    ]


def inverso_modular(a, m):
    """Inverso de a módulo m con Euclides y Bézout en forma matricial.

    1. Euclides: m = q0*a + r1, a = q1*r1 + r2, ... Se guarda el cociente de cada división cuyo residuo no es 0
    2. Con cada cociente se forma Q = [[q, 1], [1, 0]] y se calcula M = Q0 * Q1 * ... * Qk. Así queda [m, a] = M [r, MCD].
    3. La inversa de M es [[d, -b], [-c, a]] / det(M). Su segunda fila da la ecuación de Bézout: MCD = x*m + y*a. Si MCD = 1, y es el inverso de a.

    Devuelve el representante d que cumple 1 <= d < m
    """
    if m < 2 or a < 1:
        raise ValueError(f"No se puede calcular el inverso de {a} módulo {m}.")

    #  Euclides guardando los cocientes
    cocientes = []
    dividendo, divisor = m, a
    while dividendo % divisor != 0:
        cocientes.append(dividendo // divisor)
        dividendo, divisor = divisor, dividendo % divisor

    if divisor != 1:
        raise ValueError(f"{a} no tiene inverso módulo {m}, porque MCD({a}, {m}) = {divisor}.")

    # M = Q0 * Q1 * ... * Qk
    M = [[1, 0], [0, 1]]
    for q in cocientes:
        M = multiplicar_matrices(M, [[q, 1], [1, 0]])

    # segunda fila de la inversa de M. det(M) es 1 o -1, la división es exacta.
    det = M[0][0] * M[1][1] - M[0][1] * M[1][0]
    y = M[0][0] // det
    return y % m


def exp_modular(base, exponente, modulo):
    """Calcula base^exponente mod modulo con el algoritmo mpower2 

    - Si el exponente es 0, el resultado es 1.
    - Si es par:   (base^(exponente/2))^2 mod m
    - Si es impar: base * (base^((exponente-1)/2))^2 mod m

    Se reduce módulo m en cada paso; nunca se calcula la potencia completa.
    """
    if exponente == 0:
        return 1 % modulo
    mitad = exp_modular(base, exponente // 2, modulo)
    cuadrado = (mitad * mitad) % modulo
    if exponente % 2 == 0:
        return cuadrado
    return (base * cuadrado) % modulo



# Validaciones

def nombre_caracter(caracter):
    """Texto legible para un carácter"""
    especiales = {" ": "espacio", "\n": "salto de línea", "\t": "tabulación", "\r": "retorno de carro"}
    return especiales.get(caracter, caracter)


def convertir_entero(valor, nombre):
    """Convierte el texto de un campo a entero o lanza un error claro."""
    texto = str(valor).strip()
    if texto == "":
        raise ValueError(f"Falta el valor de {nombre}.")
    try:
        return int(texto)
    except ValueError:
        raise ValueError(f"{nombre} debe ser un número entero. Se recibió: {texto}") from None


def validar_parametros(p, q, e):
    """Revisa p, q y e. Devuelve (p, q, e, n, phi) ya como enteros"""
    p = convertir_entero(p, "p")
    q = convertir_entero(q, "q")
    e = convertir_entero(e, "e")

    if not es_primo(p):
        raise ValueError(f"p = {p} no es primo")
    if not es_primo(q):
        raise ValueError(f"q = {q} no es primo")
    if p == q:
        raise ValueError("p y q deben ser primos distintos")

    n = p * q
    if not N_MIN < n < N_MAX:
        raise ValueError(f"n = p * q = {n} está fuera del rango. Debe cumplir {N_MIN} < n < {N_MAX}.")

    phi = (p - 1) * (q - 1)
    if e <= 1:
        raise ValueError(f"e debe ser mayor que 1. Se recibió e = {e}.")
    divisor_comun = mcd(e, phi)
    if divisor_comun != 1:
        raise ValueError(
            f"MCD(e, φ) = MCD({e}, {phi}) = {divisor_comun}. "
            "e debe ser primo relativo con φ, es decir, el MCD debe ser 1."
        )
    return p, q, e, n, phi


def validar_mensaje(mensaje):
    """Cada carácter debe tener código ASCII entre 32 y 126"""
    if mensaje == "":
        raise ValueError("Escriba un mensaje para encriptar.")
    for posicion, caracter in enumerate(mensaje, start=1):
        codigo = ord(caracter)
        if codigo < ASCII_MIN or codigo > ASCII_MAX:
            raise ValueError(
                f"El carácter \"{nombre_caracter(caracter)}\" (posición {posicion}) no está permitido. "
                "Solo se aceptan caracteres ASCII del 32 al 126: sin tildes, ñ, "
                "tabulaciones ni saltos de línea."
            )


def leer_cifrado(cifrado, n):
    """Separa C en bloques de 6 dígitos y revisa que cada uno cumpla 0 <= c < n."""
    partes = str(cifrado).split()
    if not partes:
        raise ValueError("Escriba el mensaje cifrado C.")

    bloques = []
    for numero, parte in enumerate(partes, start=1):
        solo_digitos = all(caracter in DIGITOS for caracter in parte)
        if len(parte) != DIGITOS_BLOQUE or not solo_digitos:
            raise ValueError(
                f"El bloque {numero} de C (\"{parte}\") no es válido. Cada bloque debe tener "
                "6 dígitos del 0 al 9 y los bloques se separan con espacios."
            )
        c = int(parte)
        if c >= n:
            raise ValueError(
                f"El bloque {numero} de C vale {c} y no es menor que n = {n}. "
                "Cada bloque debe cumplir 0 ≤ c < n."
            )
        bloques.append(c)
    return bloques


# Conversión entre texto y bloques

def pareja_a_bloque(pareja):
    """'AB' -> '065' + '066' -> 65066."""
    return int(f"{ord(pareja[0]):03d}{ord(pareja[1]):03d}")


def bloque_a_pareja(m, numero_bloque):
    """65066 -> '065066' -> 065 y 066 -> 'AB'. Revisa que ambos códigos sean válidos."""
    digitos = f"{m:06d}"
    codigos = [int(digitos[:3]), int(digitos[3:])]
    for codigo in codigos:
        if codigo < ASCII_MIN or codigo > ASCII_MAX:
            raise ValueError(
                f"El bloque {numero_bloque} da {digitos} y el código {codigo:03d} no es un "
                "carácter permitido. Revise que C, L, p, q y e sean los mismos que se usaron al encriptar."
            )
    return chr(codigos[0]) + chr(codigos[1])



# Encriptar y desencriptar

def encriptar(mensaje, p, q, e):
    """Encripta el mensaje M con la llave pública (e, n).

    Devuelve un diccionario con todo lo que la interfaz necesita mostrar.
    """
    validar_mensaje(mensaje)
    p, q, e, n, phi = validar_parametros(p, q, e)

    L = len(mensaje)
    relleno = L % 2 == 1
    texto = mensaje + " " if relleno else mensaje

    caracteres = [(caracter, ord(caracter)) for caracter in texto]

    bloques = []
    for i in range(0, len(texto), 2):
        pareja = texto[i:i + 2]
        m = pareja_a_bloque(pareja)
        c = exp_modular(m, e, n)
        bloques.append({"pareja": pareja, "m": m, "c": c})

    C = " ".join(f"{bloque['c']:06d}" for bloque in bloques)

    return {
        "p": p, "q": q, "e": e, "n": n, "phi": phi, "mcd": 1,
        "L": L, "relleno": relleno,
        "texto_con_relleno": texto,
        "caracteres": caracteres,
        "bloques": bloques,
        "C": C,
    }


def desencriptar(cifrado, longitud, p, q, e):
    """Recupera el mensaje M a partir de C, L, p, q y e."""
    p, q, e, n, phi = validar_parametros(p, q, e)
    bloques_c = leer_cifrado(cifrado, n)

    k = len(bloques_c)
    L = convertir_entero(longitud, "L")
    if L != 2 * k and L != 2 * k - 1:
        raise ValueError(
            f"L = {L} no coincide con C. C tiene {k} bloque(s), "
            f"así que L debe ser {2 * k} o {2 * k - 1}."
        )

    d = inverso_modular(e, phi)

    bloques = []
    texto = ""
    for numero, c in enumerate(bloques_c, start=1):
        m = exp_modular(c, d, n)
        pareja = bloque_a_pareja(m, numero)
        bloques.append({"c": c, "m": m, "pareja": pareja})
        texto += pareja

    relleno = L % 2 == 1
    if relleno:
        if texto[-1] != " ":
            raise ValueError(
                "L es impar, pero el último carácter recuperado no es un espacio. Revise C y L."
            )
        mensaje = texto[:-1]    # se quita solo el espacio de relleno
    else:
        mensaje = texto

    return {
        "p": p, "q": q, "e": e, "n": n, "phi": phi, "d": d,
        "L": L, "k": k, "relleno": relleno,
        "texto_con_relleno": texto,
        "caracteres": [(caracter, ord(caracter)) for caracter in texto],
        "bloques": bloques,
        "mensaje": mensaje,
    }
