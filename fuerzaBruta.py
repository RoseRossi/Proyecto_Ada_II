from itertools import product, combinations
from lecturaArchivo import *
from insatisfaccion import insatisfaccionEstudiante, insatisfaccionTotal

# Algoritmo de fuerza bruta

# Producto cartesiano
# Se usa al final para tener todas las diferentes combinaciones
def product(*args, repeat=1):
    pools = [tuple(pool) for pool in args] * repeat
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)
# ---------------------------------------------------------
# Hacer combinaciones
# El resultado de aqui luego lo usamos en producto cartesiano

def combinations(iterable, r):
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)
# ---------------------------------------------------------


def combinacionesAsignatura(curso, asignaturas, solicitudes):

  elementos = [e for e, asignacion in solicitudes.items()
               if curso in asignacion]
  combinaciones = []

  if asignaturas[curso] > len(elementos):
    combinaciones.append(tuple(elementos))
  else:
    combinaciones = list(combinations(elementos, asignaturas[curso]))

  return combinaciones


def combinacionesPosibles(asignaturas, solicitudes):

  clavesAsignaturas = list(asignaturas.keys())
  opcionesCombinar = []

  for asignatura in clavesAsignaturas:
    opcionesCombinar.append(combinacionesAsignatura(
        asignatura, asignaturas, solicitudes))

  opciones = list(product(*opcionesCombinar))
  return opciones


def rocFB(cantidadAsignaturas, cantidadEstudiantes, asignaturas, solicitudes):
    clavesAsignaturas = list(asignaturas.keys())
    opciones = combinacionesPosibles(asignaturas, solicitudes)

    mejorOpcion = {}
    insatistaccion = 1

    for opcion in range(0, len(opciones)):
        distribucion = {}
        for estudiante in solicitudes:
            distribucion[estudiante] = []

        for asignatura in range(0, cantidadAsignaturas):
            for estudiante in list(opciones[opcion][asignatura]):
                distribucion[estudiante].append(clavesAsignaturas[asignatura])

        posibleinsatistaccion = insatisfaccionTotal(
            cantidadEstudiantes, distribucion, solicitudes)

        if posibleinsatistaccion < insatistaccion:
            mejorOpcion = dict(distribucion)
            insatistaccion = posibleinsatistaccion

    return [mejorOpcion, insatistaccion]
