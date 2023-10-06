from itertools import product, combinations

materiasA = {}
solicitudesA = {}
cantidadEstudiantesA = 0
cantidadmateriasA = 0
archivo = 'entrada.txt'

# Lectura Archivo

def lecturaArchivo(nombreArchivo):

  global cantidadmateriasA, cantidadEstudiantesA
  entrada = open(file=(nombreArchivo), mode="r", encoding='utf-8')

  cantidadmateriasA = int(entrada.readline())

# lectura de las asignaturas

  for lineas in range(0, cantidadmateriasA):
    linea = entrada.readline()
    linea = linea.split(",")
    materiasA[linea[0]] = int(linea[1])

# lectura de las solicitudes

  cantidadEstudiantesA = int(entrada.readline())

  for estudiantes in range(0, cantidadEstudiantesA):

    estudiante = entrada.readline()
    estudiante = estudiante.split(",")

    nuevoEstudiante = {}
    cantidadAsignaturaEstudiante = int(estudiante[1])

    for linea in range(0, cantidadAsignaturaEstudiante):
      asigSolicitada = entrada.readline()
      asigSolicitada = asigSolicitada.split(",")
      nuevoEstudiante[asigSolicitada[0]] = int(asigSolicitada[1].strip())

    solicitudesA[estudiante[0]] = nuevoEstudiante

  entrada.close()

def salidaArchivo(distribucion, inconformidad, tipoSalida):
    nombre_salida = f"salida{tipoSalida}.txt"

    with open(nombre_salida, mode="w", encoding='utf-8') as salida:
        salida.write(str(inconformidad) + "\n")

        for estudiante in distribucion:
            salida.write(estudiante + "," +
                         str(len(distribucion[estudiante])) + "\n")

            for asignatura in distribucion[estudiante]:
                salida.write(asignatura + "\n")

lecturaArchivo(archivo)

# insatisfaccion

def insatisfaccionEstudiante(estudiante, distribucion, solicitudes):

  solicitud = set(solicitudes[estudiante])
  asignacion = set(distribucion[estudiante])
  noAsignadas = solicitud - asignacion
  puntosPrioridad = 3*len(solicitud)-1

  # puntos de cursos no asignados-----------------------------
  puntosNoAsignados = 0

  if len(noAsignadas) <= len(solicitud)/2:
    for noAsig in noAsignadas:
      puntosNoAsignados += solicitudes[estudiante][noAsig]
  else:
    puntosNoAsignados = puntosPrioridad
    for asig in asignacion:
      puntosNoAsignados -= solicitudes[estudiante][asig]

  insatistaccion = (1 - (len(asignacion)/len(solicitud))) * \
      (puntosNoAsignados/puntosPrioridad)

  return insatistaccion

def insatisfaccionTotal(cantidadEstudiantes, distribucion, solicitudes):
  insatistaccionGeneral = 0

  for estudiante in solicitudes:
    insatistaccionGeneral += insatisfaccionEstudiante(
        estudiante, distribucion, solicitudes)

  return insatistaccionGeneral/cantidadEstudiantes

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

# Pruebas

lecturaArchivo(archivo)

fuerzaBruta = rocFB(cantidadmateriasA, cantidadEstudiantesA,
                    materiasA, solicitudesA)
print(f"Fuerza Bruta: {fuerzaBruta}")
salidaArchivo(fuerzaBruta[0], fuerzaBruta[1], "FB")

# voraz = rocV(cantidadmateriasA, cantidadEstudiantesA, materiasA, solicitudesA)
# print(f"Algoritmo Voraz: {voraz}")
# salidaArchivo(voraz[0], voraz[1], "V")
