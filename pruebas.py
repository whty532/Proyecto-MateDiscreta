"""Comprobaciones del proyecto RSA"""

import unittest

from rsa_logic import (
    desencriptar,
    encriptar,
    es_primo,
    exp_modular,
    inverso_modular,
    mcd,
)

# Parámetros del ejemplo de referencia del enunciado
P, Q, E = 367, 373, 17


def ida_y_vuelta(mensaje, p=P, q=Q, e=E):
    """Encripta y desencripta; devuelve (resultado_encriptar, mensaje_recuperado)."""
    cifrado = encriptar(mensaje, p, q, e)
    recuperado = desencriptar(cifrado["C"], cifrado["L"], p, q, e)
    return cifrado, recuperado["mensaje"]


def exp_lenta(base, exponente, modulo):
    """Referencia lenta: multiplica una vez por paso y reduce en cada paso."""
    resultado = 1 % modulo
    for _ in range(exponente):
        resultado = (resultado * base) % modulo
    return resultado


class Algoritmos(unittest.TestCase):

    def test_primalidad_apuntes(self):
        """Primalidad: 101 es primo y 91 = 7 * 13 no lo es (apuntes, pág. 3)"""
        self.assertTrue(es_primo(101))
        self.assertFalse(es_primo(91))
        self.assertTrue(es_primo(2))
        self.assertFalse(es_primo(1))
        self.assertFalse(es_primo(0))
        self.assertTrue(es_primo(367) and es_primo(373))

    def test_mcd_apuntes(self):
        """MCD: mcd(108, 8) = 4, mcd(662, 441) = 1, mcd(92, 48) = 4 (apuntes)"""
        self.assertEqual(mcd(108, 8), 4)
        self.assertEqual(mcd(662, 441), 1)
        self.assertEqual(mcd(92, 48), 4)
        self.assertEqual(mcd(8, 4), 4)          # caso en que b divide a a
        self.assertEqual(mcd(17, 136152), 1)

    def test_inverso_apuntes(self):
        """Inverso: 7 en Z11 es 8 y 39 en Z58 es 3 (apuntes, págs. 16-18)"""
        self.assertEqual(inverso_modular(7, 11), 8)
        self.assertEqual(inverso_modular(39, 58), 3)

    def test_inverso_cumple_definicion(self):
        """Inverso: e * d ≡ 1 (mod φ) y 1 <= d < φ para varios valores"""
        phi = 136152
        for e in [5, 17, 19, 23, 65537, 136153]:
            d = inverso_modular(e, phi)
            self.assertTrue(1 <= d < phi)
            self.assertEqual((e * d) % phi, 1)

    def test_inverso_sin_mcd_1(self):
        """Inverso: rechaza calcularlo si MCD(a, m) no es 1"""
        with self.assertRaises(ValueError):
            inverso_modular(6, 9)

    def test_exp_modular(self):
        """Exponenciación modular: coincide con la multiplicación paso a paso"""
        casos = [(9, 13, 22), (2, 10, 1000), (3, 0, 7), (82083, 17, 136891), (123875, 8009, 136891)]
        for base, exponente, modulo in casos:
            self.assertEqual(exp_modular(base, exponente, modulo), exp_lenta(base, exponente, modulo))


class EjemploReferencia(unittest.TestCase):

    def test_ejemplo_rsa(self):
        """Ejemplo del enunciado: "RSA" con p = 367, q = 373, e = 17"""
        cifrado = encriptar("RSA", P, Q, E)
        self.assertEqual(cifrado["n"], 136891)
        self.assertEqual(cifrado["phi"], 136152)
        self.assertEqual(cifrado["L"], 3)
        self.assertTrue(cifrado["relleno"])
        self.assertEqual(cifrado["texto_con_relleno"], "RSA ")
        self.assertEqual([f"{b['m']:06d}" for b in cifrado["bloques"]], ["082083", "065032"])
        self.assertEqual(cifrado["C"], "026054 123875")

        descifrado = desencriptar("026054 123875", 3, P, Q, E)
        self.assertEqual(descifrado["d"], 8009)
        self.assertEqual(descifrado["mensaje"], "RSA")


class Recuperacion(unittest.TestCase):

    def test_longitud_par(self):
        """Recupera un mensaje de longitud par sin relleno"""
        cifrado, recuperado = ida_y_vuelta("Hola")
        self.assertFalse(cifrado["relleno"])
        self.assertEqual(recuperado, "Hola")

    def test_longitud_impar(self):
        """Recupera un mensaje de longitud impar y retira solo el relleno"""
        cifrado, recuperado = ida_y_vuelta("Hola!")
        self.assertTrue(cifrado["relleno"])
        self.assertEqual(recuperado, "Hola!")

    def test_mayusculas_minusculas(self):
        """Conserva mayúsculas y minúsculas"""
        self.assertEqual(ida_y_vuelta("MaTeMaTiCa DiScReTa")[1], "MaTeMaTiCa DiScReTa")

    def test_numeros_y_signos(self):
        """Conserva números y signos"""
        mensaje = "Discreta 1: 100% (2+2=4)? #UVG @2026 {ok} [x] ~_~"
        self.assertEqual(ida_y_vuelta(mensaje)[1], mensaje)

    def test_espacios_seguidos(self):
        """Conserva espacios seguidos"""
        self.assertEqual(ida_y_vuelta("a    b  c")[1], "a    b  c")

    def test_espacios_inicio_y_final(self):
        """Conserva los espacios del inicio y del final"""
        for mensaje in ["  Hola, Mundo! 2026  ", "   RSA", "RSA   ", " ", "  "]:
            self.assertEqual(ida_y_vuelta(mensaje)[1], mensaje)

    def test_mensaje_que_termina_en_espacio(self):
        """L par: un espacio original al final no se toma como relleno"""
        cifrado, recuperado = ida_y_vuelta("ab ")      # L = 3, impar
        self.assertEqual(recuperado, "ab ")
        cifrado, recuperado = ida_y_vuelta("abc ")     # L = 4, par
        self.assertFalse(cifrado["relleno"])
        self.assertEqual(recuperado, "abc ")

    def test_todos_los_caracteres_permitidos(self):
        """Recupera los 95 caracteres ASCII del 32 al 126"""
        mensaje = "".join(chr(codigo) for codigo in range(32, 127))
        self.assertEqual(ida_y_vuelta(mensaje)[1], mensaje)

    def test_ceros_iniciales(self):
        """Bloques cifrados con ceros iniciales se escriben con 6 dígitos y se recuperan"""
        cifrado, recuperado = ida_y_vuelta("  Hola, Mundo! 2026  ", 401, 409, 65537)
        self.assertTrue(cifrado["C"].startswith("004965"))
        self.assertEqual(recuperado, "  Hola, Mundo! 2026  ")

        cifrado, recuperado = ida_y_vuelta("Discreta 1: 100%")
        self.assertIn("002039", cifrado["C"].split())
        self.assertEqual(recuperado, "Discreta 1: 100%")

    def test_otros_parametros(self):
        """Funciona con otros p, q y e válidos, incluso con e mayor que φ"""
        for p, q, e in [(503, 509, 7), (401, 409, 65537), (2, 63073, 5), (367, 373, 136153)]:
            self.assertEqual(ida_y_vuelta("Prueba RSA 123", p, q, e)[1], "Prueba RSA 123")

    def test_formato_de_c(self):
        """Cada bloque de C tiene 6 dígitos y van separados por un espacio"""
        cifrado = encriptar("Proyecto 3", P, Q, E)
        for bloque in cifrado["C"].split(" "):
            self.assertEqual(len(bloque), 6)
            self.assertTrue(bloque.isdigit())


class Rechazos(unittest.TestCase):

    def assertRechaza(self, funcion, *argumentos):
        with self.assertRaises(ValueError):
            funcion(*argumentos)

    # p, q y e
    def test_p_no_primo(self):
        """Rechaza p o q que no son primos"""
        self.assertRechaza(encriptar, "RSA", 365, Q, E)
        self.assertRechaza(encriptar, "RSA", P, 371, E)
        self.assertRechaza(encriptar, "RSA", 1, Q, E)
        self.assertRechaza(encriptar, "RSA", -367, Q, E)

    def test_p_igual_q(self):
        """Rechaza p = q"""
        self.assertRechaza(encriptar, "RSA", 409, 409, E)

    def test_n_fuera_de_rango(self):
        """Rechaza n <= 126126 y n >= 1000000"""
        self.assertRechaza(encriptar, "RSA", 101, 103, E)      # n = 10403
        self.assertRechaza(encriptar, "RSA", 347, 359, E)      # n = 124573
        self.assertRechaza(encriptar, "RSA", 1009, 1013, E)    # n = 1022117

    def test_e_invalido(self):
        """Rechaza e <= 1 y e con MCD(e, φ) distinto de 1"""
        self.assertRechaza(encriptar, "RSA", P, Q, 1)
        self.assertRechaza(encriptar, "RSA", P, Q, 0)
        self.assertRechaza(encriptar, "RSA", P, Q, -17)
        self.assertRechaza(encriptar, "RSA", P, Q, 2)          # φ es par
        self.assertRechaza(encriptar, "RSA", P, Q, 31)         # 31 divide a φ = 136152

    def test_datos_no_enteros(self):
        """Rechaza p, q, e o L que no son enteros"""
        self.assertRechaza(encriptar, "RSA", "abc", Q, E)
        self.assertRechaza(encriptar, "RSA", "367.0", Q, E)
        self.assertRechaza(encriptar, "RSA", P, "", E)
        self.assertRechaza(desencriptar, "026054 123875", "tres", P, Q, E)

    # Mensaje
    def test_caracteres_no_permitidos(self):
        """Rechaza ñ, tildes, tabulaciones, saltos de línea y emojis sin cambiarlos"""
        for mensaje in ["Año", "canción", "a\tb", "a\nb", "hola 😀", "¿Qué?"]:
            self.assertRechaza(encriptar, mensaje, P, Q, E)

    def test_mensaje_vacio(self):
        """Rechaza un mensaje vacío"""
        self.assertRechaza(encriptar, "", P, Q, E)

    # Cifrado C
    def test_bloques_mal_formados(self):
        """Rechaza bloques de 5 o 7 dígitos, con letras o mal separados"""
        for cifrado in ["26054 123875", "0260540 123875", "02605A 123875", "026054,123875", "-26054 123875"]:
            self.assertRechaza(desencriptar, cifrado, 3, P, Q, E)

    def test_c_vacio(self):
        """Rechaza un cifrado vacío"""
        self.assertRechaza(desencriptar, "   ", 1, P, Q, E)

    def test_c_mayor_o_igual_que_n(self):
        """Rechaza bloques con c >= n"""
        self.assertRechaza(desencriptar, "136891 123875", 3, P, Q, E)
        self.assertRechaza(desencriptar, "999999 123875", 3, P, Q, E)

    # Longitud L
    def test_l_incoherente(self):
        """Rechaza L distinto de 2k y de 2k - 1"""
        for L in [1, 2, 5, 6, 0, -3]:
            self.assertRechaza(desencriptar, "026054 123875", L, P, Q, E)

    def test_l_impar_sin_espacio_final(self):
        """Rechaza L impar si el último carácter recuperado no es un espacio"""
        cifrado = encriptar("Hola", P, Q, E)       # L = 4, sin relleno
        self.assertRechaza(desencriptar, cifrado["C"], 3, P, Q, E)

    # Texto recuperado
    def test_bloque_que_no_da_ascii_valido(self):
        """Rechaza bloques que no producen dos códigos ASCII válidos"""
        self.assertRechaza(desencriptar, "000000", 2, P, Q, E)
        self.assertRechaza(desencriptar, "000001", 2, P, Q, E)

    def test_llave_equivocada(self):
        """Con otro e no se presenta un mensaje como si fuera correcto"""
        cifrado = encriptar("RSA", P, Q, E)
        with self.assertRaises(ValueError):
            desencriptar(cifrado["C"], cifrado["L"], P, Q, 19)


if __name__ == "__main__":
    unittest.main(verbosity=2)
