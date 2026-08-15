edad = 25
nombre = "Juan" 
altura = 1.75
activo = True

# and or not operadores logicos 
# > < >= <= == != operadores de comparacion
def verificar_edad(edad, activo, nombre):
    if edad >= 18 and activo:
        print(f"{nombre} es mayor de edad y está activo.")
    else:
        print(f"{nombre} no cumple con los requisitos.")

def verificar_altura(altura):
    if altura >= 1.70:
        return "La altura es suficiente."
    elif altura >= 1.50:
        return "La altura es aceptable."
    else:
        return "eres bajo."


def main():
    nombre = input("Ingrese su nombre: ")
    edad = int(input("Ingrese su edad: "))
    activo = input("¿Está activo? (s/n): ").lower() == "s"
    altura = float(input("Ingrese su altura en metros: "))
    verificar_edad(edad, activo, nombre)
    resultado_altura = verificar_altura(altura)
    print(resultado_altura)

if __name__ == "__main__":
    main()          




    
        

