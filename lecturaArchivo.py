from insatisfaccion import insatisfaccionEstudiante, insatisfaccionTotal
import lecturaArchivo

materiasA = {}
solicitudesA = {}
cantidadEstudiantesA = 0
cantidadmateriasA = 0

# Lectura Archivo

def lecturaArchivo(nombreArchivo):
    global cantidadmateriasA, cantidadEstudiantesA
    entrada = open(file=nombreArchivo, mode="r", encoding='utf-8')

    cantidadmateriasA = int(entrada.readline())

    # Lectura de las asignaturas
    for lineas in range(cantidadmateriasA):
        linea = entrada.readline()
        linea = linea.split(",")
        materiasA[linea[0]] = int(linea[1])

    cantidadEstudiantesA = int(entrada.readline())

    # Lectura de las solicitudes
    for estudiantes in range(cantidadEstudiantesA):
        estudiante = entrada.readline().strip().split(",")
        nombre_estudiante = estudiante[0]
        cantidad_asignaturas = int(estudiante[1])
        solicitudes_estudiante = {}

        for _ in range(cantidad_asignaturas):
            asignatura = entrada.readline().strip().split(",")
            nombre_asignatura = asignatura[0]
            cantidad_solicitada = int(asignatura[1])
            solicitudes_estudiante[nombre_asignatura] = cantidad_solicitada

        solicitudesA[nombre_estudiante] = solicitudes_estudiante

    entrada.close()
