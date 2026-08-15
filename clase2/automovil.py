class Automovil:
    marca: str
    color: str
    modelo: str
    anio: int

    def __init__(self, marca: str):
        self.marca = marca


    def set_color(self, color: str):
        self.color = color

    def set_modelo(self, modelo: str):
        self.modelo = modelo

    def set_anio(self, anio: int):
        self.anio = anio  

    def revisar_estado(self)-> bool:
        #codigo ...
        return True        

auto1 = Automovil('Mazda')
auto2 = Automovil('Toyoya')
auto3 = Automovil('Mazda')
auto4 = auto1 

auto4.marca = "Hiii"
numero1 = 5
numero2 = 5
"""
if numero1 == numero2:
    print("son iguales")
else:
    print("no son iguales")
"""

print("objeto1:", auto1)
print("objeto2:", auto2)
print("objeto3:", auto3)
print("objeto4:", auto4)
print()
print("marca de auto1" )
