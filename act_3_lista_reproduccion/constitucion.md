# Constitución del proyecto — Lista de reproducción

Principios que gobiernan cualquier decisión de este trabajo. Si una decisión de
`plan.md` o una tarea de `task.md` los contradice, la que está mal es la
decisión.

## 1. El contrato manda, no la estructura

`spec.md` describe **comportamiento observable**. Las dos implementaciones
(`ListaArreglo`, `ListaEnlazada`) se someten al mismo contrato y a la misma
batería de pruebas. Si para hacer pasar una implementación hay que tocar
`test_contrato.py`, el contrato estaba mal escrito y se corrige **en `spec.md`**,
no en la prueba a conveniencia.

## 2. El archivo de pruebas de la actividad 2 no se toca

`test_contrato.py` es el mismo archivo para las dos estructuras. La única forma
de extenderlo a otra implementación es registrarla en `conftest.py`. Si la
enlazada falla, el error está en la implementación o en el contrato, y hay que
decir cuál de los dos.

## 3. Sin atajos que anulen el aprendizaje

- **Nada de `list` de Python dentro de `ListaEnlazada`.** Los datos viven en
  nodos. Guardarlos en una lista y envolverla no es construir una lista enlazada.
- **`ListaArreglo` no usa `list.insert`/`list.pop`** para desplazar: desplaza
  con bucles explícitos, para que el costo medido sea el del algoritmo y no el de
  una rutina en C. (El bloque de almacenamiento sí es una `list` de tamaño fijo,
  equivalente a un arreglo.)

## 4. Los casos límite se prueban por separado

Lista vacía, un elemento, borrar el primero y borrar el último tienen pruebas
propias. Cada una comprueba además que la lista **siga funcionando después**
del caso límite, porque un puntero mal actualizado casi nunca falla en el
momento, falla en la operación siguiente.

## 5. Las decisiones salen de los datos

La recomendación de estructura sale de las frecuencias dadas y de costos
**medidos**, no de la intuición de que «las enlazadas son mejores para
insertar». Toda conclusión declara sus límites y qué tendría que cambiar para
invertirse.

## 6. Un enlace se sobrescribe solo cuando ya está guardado

Al manipular nodos: primero se conecta lo nuevo con lo existente; después se
desconecta lo viejo (ver `nodos_a_mano.md`).

## 7. Especificar antes de programar

Orden de trabajo: constitución → spec → plan → tareas → código. Si el código y
la spec no coinciden, el que está mal es el código.

## 8. Reproducible en una máquina limpia

`python -m pytest` pasa sin configuración extra; la única dependencia es
`pytest`. El benchmark es determinista salvo el ruido del reloj (semilla fija).
