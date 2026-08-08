# Código base — Semana 01
# Fuente: 01-Momento-1-Contrato-y-secuencia/01-Semana-01-Repaso-y-modelo-de-memoria/02-guia-de-laboratorio.html

from hola_estructuras import *


def test_contar():
    assert contar([]) == 0
    assert contar([1, 2, 3]) == 3


def test_suma():
    assert suma([]) == 0
    assert suma([1, 2, 3]) == 6
    assert suma([-1, 1]) == 0


def test_maximo():
    assert maximo([]) is None
    assert maximo([5]) == 5
    assert maximo([3, 9, 1]) == 9


def test_buscar():
    assert buscar([], 1) == -1
    assert buscar([1, 2, 3], 2) == 1
    assert buscar([1, 2, 3], 9) == -1


def test_invertida_no_muta():
    original = [1, 2, 3]
    resultado = invertida(original)
    assert resultado == [3, 2, 1]
    assert original == [1, 2, 3]      # la original NO cambió


def test_invertir_en_sitio_muta():
    lista = [1, 2, 3]
    identidad = id(lista)
    invertir_en_sitio(lista)
    assert lista == [3, 2, 1]
    assert id(lista) == identidad     # es el MISMO objeto
