class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

a = Nodo(5)
b = Nodo(10)

print("referencia del objeto a:", a)
print("referencia del objeto b:", b) 

a.siguiente = b

c = Nodo(15)
d = Nodo(20)
b.siguiente = c
c.siguiente = d 

print("dato del nodo a:", a.dato)
print("dato del nodo b:", b.dato)
print("dato del nodo c:", c.dato)
print("dato del nodo d:", d.dato)

#------------------------------------------
#Asignacion de nodo a otro nodo en medio.
#------------------------------------------

n1 = Nodo(1)
n2 = Nodo(2)
n3 = Nodo(3)

n1.siguiente = n3
# opcion 1: variable temporal 
temp = n1.siguiente
n1.siguiente = n2
n1.siguiente.siguiente = temp
#opcion 2: sin variable temporal
n1.siguiente = n2
n2.siguiente = n3






