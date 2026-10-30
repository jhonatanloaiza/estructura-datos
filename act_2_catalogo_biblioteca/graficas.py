"""Genera las gráficas a partir de `resultados.csv`, sin volver a medir.

- `grafica_operaciones.png`: una gráfica por operación, medido contra predicho.
- `grafica_memoria.png`: costo por elemento según la disposición en memoria.
- `grafica_equilibrio.png`: costo total según las búsquedas por inserción.

Ejecutar:  python graficas.py
"""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator

import analisis
from analisis import EPOCAS, TAMANOS, es

SUPERFICIE = "#fcfcfb"
TINTA = "#0b0b0b"
TINTA_SECUNDARIA = "#52514e"
TINTA_TENUE = "#898781"
REJILLA = "#e1e0d9"
EJE = "#c3c2b7"
AZUL = "#2a78d6"
NARANJA = "#eb6834"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Segoe UI", "DejaVu Sans"],
    "font.size": 10,
    "figure.facecolor": SUPERFICIE,
    "axes.facecolor": SUPERFICIE,
    "axes.edgecolor": EJE,
    "axes.linewidth": 0.8,
    "axes.labelcolor": TINTA_SECUNDARIA,
    "axes.labelsize": 9.5,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": REJILLA,
    "grid.linewidth": 0.7,
    "xtick.color": TINTA_SECUNDARIA,
    "ytick.color": TINTA_SECUNDARIA,
    "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.5,
    "xtick.major.size": 0,
    "ytick.major.size": 0,
    "xtick.minor.size": 0,
    "ytick.minor.size": 0,
    "lines.solid_capstyle": "round",
    "savefig.dpi": 200,
    "savefig.facecolor": SUPERFICIE,
})

LINEA = {"linewidth": 1.8, "solid_joinstyle": "round"}
PUNTO = {"marker": "o", "markersize": 6.5, "markeredgecolor": SUPERFICIE,
         "markeredgewidth": 1.2}

# operación, título, clase, escala del eje y, forma predicha
PANELES = [
    ("obtener", "obtener", "O(1)", "linear", lambda n: 1),
    ("insertar_inicio", "insertar al inicio", "O(n)", "log", lambda n: n),
    ("insertar_final", "insertar al final", "O(1) amortizado", "linear", lambda n: 1),
    ("insertar_ordenado", "insertar_ordenado", "O(n)", "log", lambda n: n),
    ("buscar_lineal", "buscar_lineal", "O(n)", "log", lambda n: n),
    ("buscar_binaria", "buscar_binaria", "O(log n)", "linear",
     lambda n: n.bit_length() + 1),
]


def _formato_entero(valor, _):
    return es(valor, 0)


def _ejes_de_tamano(ax):
    ax.set_xscale("log")
    ax.xaxis.set_major_locator(FixedLocator(TAMANOS))
    ax.xaxis.set_major_formatter(FuncFormatter(_formato_entero))
    ax.xaxis.set_minor_locator(NullLocator())


def _veredicto(tabla, operacion, clase):
    clave = "O(1)" if clase.startswith("O(1)") else clase
    if clave == "O(n)":
        medido = f"pendiente {es(analisis.pendiente(tabla, operacion), 2)}"
    else:
        medido = f"crece ×{es(analisis.crecimiento(tabla, operacion), 2)}"
    marca = "coincide" if analisis.coincide(clave, tabla, operacion) else "no coincide"
    return f"{medido}: {marca}"


def grafica_operaciones(tabla):
    fig, ejes = plt.subplots(2, 3, figsize=(11, 6.6))
    for ax, (op, titulo, clase, escala_y, forma) in zip(ejes.flat, PANELES):
        medido = [analisis.mediana(tabla, op, n) for n in TAMANOS]
        predicho = [medido[0] * forma(n) / forma(TAMANOS[0]) for n in TAMANOS]
        ax.plot(TAMANOS, predicho, color=TINTA_TENUE, linewidth=1.4,
                linestyle=(0, (4, 3)), label="Predicción, anclada en n = 1.000")
        ax.plot(TAMANOS, medido, color=AZUL, label="Mediana medida", **LINEA, **PUNTO)
        _ejes_de_tamano(ax)
        ax.set_yscale(escala_y)
        if escala_y == "linear":
            ax.set_ylim(bottom=0, top=max(medido + predicho) * 1.25)
        else:
            ax.yaxis.set_major_formatter(FuncFormatter(_formato_entero))
            ax.yaxis.set_minor_locator(NullLocator())
            ax.grid(True, which="major")
        ax.set_title(f"{titulo}, {clase}", loc="left", fontsize=11, color=TINTA,
                     fontweight="semibold", pad=20)
        ax.text(0, 1.03, _veredicto(tabla, op, clase), transform=ax.transAxes,
                fontsize=9, color=TINTA_SECUNDARIA)
        nombre_escala = "log" if escala_y == "log" else "lineal"
        ax.set_ylabel(f"Tiempo por operación (µs, escala {nombre_escala})")
        ax.set_xlabel("Registros n (escala log)")

    manejadores, etiquetas = ejes.flat[0].get_legend_handles_labels()
    fig.legend(manejadores[::-1], etiquetas[::-1], loc="upper left", ncol=2,
               frameon=False, bbox_to_anchor=(0.008, 0.965), fontsize=9.5,
               labelcolor=TINTA_SECUNDARIA)
    fig.suptitle("Recorrer memoria contigua sigue la predicción; "
                 "saltar por ella se aleja desde n = 80.000",
                 x=0.012, y=0.995, ha="left", fontsize=13.5, color=TINTA,
                 fontweight="semibold")
    fig.tight_layout(rect=(0, 0, 1, 0.94), h_pad=2.4, w_pad=2.2)
    fig.savefig(analisis.CARPETA / "grafica_operaciones.png")
    plt.close(fig)


def grafica_memoria(tabla):
    fig, ax = plt.subplots(figsize=(8.6, 4.9))
    estilos = {"contigua": "-", "dispersa": (0, (4, 2))}
    colores = {"Mover": AZUL, "Comparar": NARANJA}
    for accion, memoria, op in analisis.COSTOS_POR_ELEMENTO:
        valores = [analisis.mediana(tabla, op, n) * 1000 / n for n in TAMANOS]
        ax.plot(TAMANOS, valores, color=colores[accion], linestyle=estilos[memoria],
                label=f"{accion}, memoria {memoria}", linewidth=1.8, **PUNTO)
        ax.annotate(f"{accion}, {memoria}: {es(valores[-1], 0)} ns", (TAMANOS[-1], valores[-1]),
                    xytext=(9, 0), textcoords="offset points", va="center",
                    fontsize=9, color=TINTA_SECUNDARIA)
    _ejes_de_tamano(ax)
    ax.set_ylim(0, 200)
    ax.set_xlim(right=TAMANOS[-1] * 1.08)
    ax.set_ylabel("Nanosegundos por elemento tocado (escala lineal)")
    ax.set_xlabel("Registros n (escala log)")
    ax.set_title("Lo que encarece mover y comparar es saltar por la memoria, no la operación",
                 loc="left", fontsize=12.5, color=TINTA, fontweight="semibold", pad=34)
    ax.legend(loc="lower left", bbox_to_anchor=(-0.01, 1.0), ncol=4, frameon=False,
              fontsize=8.8, labelcolor=TINTA_SECUNDARIA, handlelength=2.4,
              columnspacing=1.3)
    fig.tight_layout(rect=(0, 0, 0.84, 1))
    fig.savefig(analisis.CARPETA / "grafica_memoria.png")
    plt.close(fig)


def grafica_equilibrio(tabla):
    proporciones = [round(0.5 * 1.25 ** i, 3) for i in range(35)]
    fig, ejes = plt.subplots(1, 2, figsize=(11, 5), sharey=True)
    for ax, n in zip(ejes, TAMANOS[2:]):
        ordenado = [analisis.costo_ordenado(tabla, n, s) / 1000 for s in proporciones]
        desordenado = [analisis.costo_desordenado(tabla, n, s) / 1000 for s in proporciones]
        ax.plot(proporciones, ordenado, color=AZUL, label="Catálogo ordenado", **LINEA)
        ax.plot(proporciones, desordenado, color=NARANJA, label="Catálogo desordenado", **LINEA)

        equilibrio = analisis.equilibrio(tabla, n)
        costo = analisis.costo_ordenado(tabla, n, equilibrio) / 1000
        ax.plot([equilibrio], [costo], color=TINTA, **PUNTO)
        ax.annotate(f"Equilibrio: {es(equilibrio, 2)} búsquedas", (equilibrio, costo),
                    xytext=(-2, -19), textcoords="offset points", ha="left", fontsize=9.5,
                    color=TINTA, fontweight="semibold")

        for epoca, s in EPOCAS.items():
            ax.axvline(s, color=EJE, linewidth=0.9, zorder=0)
            ax.annotate(f"{epoca}\n{s}:1", (s, 0.03), xycoords=ax.get_xaxis_transform(),
                        xytext=(4, 0), textcoords="offset points", ha="left", va="bottom",
                        fontsize=8.5, color=TINTA_SECUNDARIA, linespacing=1.25)

        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.xaxis.set_major_locator(FixedLocator([1, 5, 50, 300]))
        ax.xaxis.set_major_formatter(FuncFormatter(_formato_entero))
        ax.xaxis.set_minor_locator(NullLocator())
        ax.yaxis.set_major_formatter(FuncFormatter(_formato_entero))
        ax.yaxis.set_minor_locator(NullLocator())
        ax.set_xlim(proporciones[0], 950)
        ax.set_title(f"{es(n, 0)} registros", loc="left", fontsize=11.5, color=TINTA,
                     fontweight="semibold")
        ax.set_xlabel("Búsquedas por inserción (escala log)")
    ejes[0].set_ylabel("Costo de s búsquedas + 1 inserción (ms, escala log)")

    manejadores, etiquetas = ejes[0].get_legend_handles_labels()
    fig.legend(manejadores, etiquetas, loc="upper left", ncol=2, frameon=False,
               bbox_to_anchor=(0.008, 0.945), fontsize=9.5, labelcolor=TINTA_SECUNDARIA)
    fig.suptitle("El catálogo ordenado gana en las tres épocas; en vacaciones por poco",
                 x=0.012, y=0.99, ha="left", fontsize=13.5, color=TINTA, fontweight="semibold")
    fig.tight_layout(rect=(0, 0, 1, 0.91), w_pad=2.5)
    fig.savefig(analisis.CARPETA / "grafica_equilibrio.png")
    plt.close(fig)


def main():
    tabla = analisis.leer()
    grafica_operaciones(tabla)
    grafica_memoria(tabla)
    grafica_equilibrio(tabla)


if __name__ == "__main__":
    main()
