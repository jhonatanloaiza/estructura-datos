"""Parte A: la cadena a mano, sin ninguna abstracción de lista.

Solo hay una clase mínima `Nodo` (dato + siguiente) y variables sueltas. Se
recorre con un bucle `while`. La segunda mitad muestra qué pasa si se reasigna
el enlace del primer nodo *antes* de guardar el segundo.

Ejecutar:  python nodos_a_mano.py
"""


class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


def recorrer(cabeza):
    salida = []
    actual = cabeza
    while actual is not None:
        salida.append(actual.dato)
        actual = actual.siguiente
    return salida


print("=== 1. Construir tres nodos y enlazarlos a mano ===")
n1 = Nodo("Canción A")
n2 = Nodo("Canción B")
n3 = Nodo("Canción C")
n1.siguiente = n2
n2.siguiente = n3
print("cadena:", recorrer(n1))

print()
print("=== 2. Insertar 'Última hora' al principio, en el orden correcto ===")
nuevo = Nodo("Última hora")
nuevo.siguiente = n1        # primero: el nuevo apunta a la cabeza vieja
cabeza = nuevo              # después: la cabeza pasa a ser el nuevo
print("cadena:", recorrer(cabeza))

print()
print("=== 3. El error: reasignar el enlace antes de guardar el segundo ===")
a = Nodo("A")
b = Nodo("B")
c = Nodo("C")
a.siguiente = b
b.siguiente = c
print("antes:  ", recorrer(a))

# Se quiere borrar B. Error: se reasigna a.siguiente sin haber guardado b.
a.siguiente = c             # <- b ya no es alcanzable desde ninguna variable
# (aquí 'b' sigue existiendo solo porque la variable local `b` lo referencia;
#  en una lista real esa variable no existe y el nodo se pierde)
print("después:", recorrer(a))

print()
print("=== 4. El mismo error en una inserción, sin variable de respaldo ===")
import weakref

x = Nodo("X")
y = Nodo("Y")
z = Nodo("Z")
x.siguiente = y
y.siguiente = z
ref_y = weakref.ref(y)      # observador: no mantiene vivo a Y
ref_z = weakref.ref(z)
cabeza = x
del y, z                    # como en una lista real: solo se conoce la cabeza
print("antes:  ", recorrer(cabeza))

nuevo_medio = Nodo("Nuevo")
cabeza.siguiente = nuevo_medio      # error: se pisa el único enlace a Y
nuevo_medio.siguiente = None        # (ya no hay de dónde recuperar a Y)
print("después:", recorrer(cabeza))
print("¿Y sigue existiendo?", ref_y() is not None)
print("¿Z sigue existiendo?", ref_z() is not None)

print()
print("=== 5. El orden correcto: guardar antes de reasignar ===")
x = Nodo("X")
y = Nodo("Y")
z = Nodo("Z")
x.siguiente = y
y.siguiente = z
cabeza = x
del y, z

nuevo_medio = Nodo("Nuevo")
nuevo_medio.siguiente = cabeza.siguiente   # 1) guardar el resto en el nuevo
cabeza.siguiente = nuevo_medio             # 2) recién ahora se pisa el enlace
print("cadena:", recorrer(cabeza))
