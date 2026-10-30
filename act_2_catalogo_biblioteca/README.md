# El catálogo de la biblioteca: ¿ordenar o no ordenar?

Se implementa `ListaArreglo` desde cero, se predice la complejidad de sus
operaciones, se mide con `timeit` y se decide con esos números si a la biblioteca
le conviene mantener ordenado su catálogo de 80.000 registros (200.000 el año
que viene).

**Respuesta:** sí, en las tres épocas del año. Con 50 búsquedas por inserción, el
catálogo ordenado cuesta 18,3 veces menos con 80.000 registros y 13,4 veces menos
con 200.000. El punto de equilibrio está en 2,67 y 3,69 búsquedas por inserción,
por debajo incluso de las 5 de vacaciones. El cálculo está en
[`decision.md`](decision.md).

## Instalar

```bash
pip install -r requirements.txt
```

## Correr las pruebas

Desde esta carpeta:

```bash
python -m pytest -v
```

88 pruebas: el contrato y los casos extremos de `ListaArreglo`, el conteo real de
operaciones que respalda la predicción, la preparación de las mediciones y las
cuentas de la decisión. Solo necesitan `pytest`.

## Reproducir las mediciones

```bash
python medicion.py
```

Tarda unos 5 minutos y sobrescribe `resultados.csv`. Conviene correrlo con el
computador conectado y sin otras tareas. Los tiempos cambiarán según la máquina.

Para regenerar los informes y las gráficas desde `resultados.csv`, sin volver a medir:

```bash
python analisis.py
```

```bash
python graficas.py
```

## Orden de los commits

La predicción está en un commit anterior al de las mediciones:

```bash
git log --date=iso --format="%h %ad %s" -- prediccion.md resultados.csv
```

## Archivos

| Archivo | Qué es |
|---|---|
| `lista_arreglo.py` | Parte A: `ListaArreglo` |
| `test_lista_arreglo.py` | Parte A: contrato, extremos, restricciones y conteo de operaciones |
| `prediccion.md` | Parte B: complejidad derivada antes de medir |
| `medicion.py` | Parte C: mediciones con `timeit` |
| `resultados.csv` | Parte C: tiempos por repetición y mediana |
| `grafica_operaciones.png` | Parte C: una gráfica por operación |
| `comparacion.md` | Parte C: medido contra predicho y por qué difieren |
| `grafica_memoria.png` | Parte C: control de la disposición en memoria |
| `decision.md` | Parte D: cálculo, recomendación y punto de equilibrio |
| `grafica_equilibrio.png` | Parte D: costo según las búsquedas por inserción |
| `analisis.py`, `salida_analisis.txt` | De `resultados.csv` a las cifras de los informes |
| `graficas.py` | Genera las tres gráficas |
| `corrida_descartada.csv` | Primera corrida, descartada; explicada en `comparacion.md` |
| `test_medicion.py`, `test_analisis.py` | Pruebas de la preparación y de las cuentas |
| `conftest.py` | Evita el choque con el `lista_arreglo.py` de act_3 al correr `pytest` desde la raíz |
