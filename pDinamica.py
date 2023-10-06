import numpy as np
from itertools import product
import insatisfaccion
import lecturaArchivo

def rocPD(materias, solicitudes, cupos=None):
    estudiantes = list(solicitudes.keys())
    cursos = list(materias.keys())
    cantidad_estudiantes = len(estudiantes)
    
    # matriz para almacenar las insatisfacciones acumulativas
    # dp[i][j] es la insatisfacción acumulativa para los primeros i estudiantes y los primeros j cursos
    dp = np.zeros((cantidad_estudiantes + 1, len(cursos) + 1))

    for i in range(1, cantidad_estudiantes + 1):
        for j in range(1, len(cursos) + 1):
            estudiante_actual = estudiantes[i - 1]
            curso_actual = cursos[j - 1]

            solicitud_estudiante = solicitudes.get(estudiante_actual, {})
            insatisfaccion_si_toma = dp[i - 1][j - 1] + insatisfaccion.insatisfaccionEstudiante(
                estudiante_actual, {estudiante_actual: [curso_actual]}, solicitud_estudiante)

            insatisfaccion_si_no_toma = dp[i][j - 1]

            dp[i][j] = min(insatisfaccion_si_toma, insatisfaccion_si_no_toma)

    asignacion_optima = {}
    i, j = cantidad_estudiantes, len(cursos)
    while i > 0 and j > 0:
        estudiante_actual = estudiantes[i - 1]
        curso_actual = cursos[j - 1]

        solicitud_estudiante = solicitudes.get(estudiante_actual, {})

        insatisfaccion_si_toma = dp[i - 1][j - 1] + insatisfaccion.insatisfaccionEstudiante(
            estudiante_actual, {estudiante_actual: [curso_actual]}, solicitud_estudiante)
        insatisfaccion_si_no_toma = dp[i][j - 1]
        if insatisfaccion_si_toma < insatisfaccion_si_no_toma:
            if estudiante_actual in asignacion_optima:
                asignacion_optima[estudiante_actual].append(curso_actual)
            else:
                asignacion_optima[estudiante_actual] = [curso_actual]
            i -= 1
            j -= 1
        else:
            j -= 1

    return asignacion_optima, dp[cantidad_estudiantes][len(cursos)]
