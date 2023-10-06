from itertools import product, combinations
from lecturaArchivo import *
from insatisfaccion import insatisfaccionEstudiante, insatisfaccionTotal

# Algoritmo Voraz

def prioridadPuntosCurso(curso, solicitudes):
  elementos = [e for e, asignacion in solicitudes.items()
               if curso in asignacion]
  puntosCurso = {}
  puntosEstudiante = {}

  for estudiante in solicitudes:
    puntosEstudiante[estudiante] = 3*len(solicitudes[estudiante].keys())-1

  for estudiante in elementos:
    puntosCurso[estudiante] = solicitudes[estudiante][curso] / \
        puntosEstudiante[estudiante]  # +

  return puntosCurso

def prioridadCupos(asignaturas, solicitudes):
  prioridadCupos1 = {}

  for asignatura in asignaturas:
    elementos = [e for e, asignacion in solicitudes.items()
                 if asignatura in asignacion]
    prioridadCupos1[asignatura] = asignaturas[asignatura] / len(elementos)

  claves_ordenadas = [clave for clave, valor in sorted(
      prioridadCupos1.items(), key=lambda item: item[1], reverse=True)]

  return claves_ordenadas

def rocV(cantidadAsignaturas, cantidadEstudiantes, asignaturas, solicitudes):

  solucion = {}
  cuposRestantes = dict(asignaturas)
  prioridadC = prioridadCupos(asignaturas, solicitudes)
  cantidadAsignaturasEstudiante = {}

  for estudiante in solicitudes:
    solucion[estudiante] = []
    cantidadAsignaturasEstudiante[estudiante] = 0

  for curso in prioridadC:
    prioridadPC = prioridadPuntosCurso(curso, solicitudes)

    while prioridadPC and cuposRestantes[curso] > 0:
      mayorPrioridad = max(prioridadPC.values())

      # retorna una lista con los estudiantes que estan viendo el curso y tienen la misma prioridad
      estudiantesMP = [e for e, valor in prioridadPC.items()
                       if mayorPrioridad == valor]
      estudianteElegido = estudiantesMP[0]

      if not len(estudiantesMP) == 1:
        estudianteC = {}
        for cMV in estudiantesMP:
          estudianteC[cMV] = cantidadAsignaturasEstudiante[cMV]

        estudianteElegido = min(estudianteC, key=estudianteC.get)

      solucion[estudianteElegido].append(curso)
      cuposRestantes[curso] -= 1
      cantidadAsignaturasEstudiante[estudianteElegido] += 1
      del prioridadPC[estudianteElegido]

  insatistaccion = insatisfaccionTotal(
      cantidadEstudiantes, solucion, solicitudes)

  return [solucion, insatistaccion]