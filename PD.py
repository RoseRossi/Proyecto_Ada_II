# Datos proporcionados
materias = {
    '100': 1,
    '101': 3,
    '102': 2
}

solicitudes = {
    '1000': {'101': 2},
    '100': {'101': 3, '102': 2},
    '101': {'100': 2},
    '1001': {'101': 3},
    '102': {'100': 5},
    '1002': {'100': 1},
    '1003': {'100': 2},
    '1004': {'101': 4}
}

cupos = {
    '100': 1,
    '101': 3,
    '102': 2
}

# Función para calcular la insatisfacción de una asignación
def calcular_insatisfaccion(asignacion, solicitudes):
    insatisfaccion_total = 0
    for estudiante, cursos in asignacion.items():
        insatisfaccion_estudiante = 0
        capacidad_priorizar = 3 * len(solicitudes[estudiante]) - 1  # Cálculo de la capacidad de priorización
        for curso in cursos:
            insatisfaccion_estudiante += solicitudes[estudiante].get(curso, 0)
        insatisfaccion_estudiante *= (1 - len(cursos) / capacidad_priorizar)
        insatisfaccion_total += insatisfaccion_estudiante
    return insatisfaccion_total / len(asignacion)

# Datos proporcionados
materias = {
    '100': 1,
    '101': 3,
    '102': 2
}

solicitudes = {
    '1000': {'101': 2},
    '100': {'101': 3, '102': 2},
    '101': {'100': 2},
    '1001': {'101': 3},
    '102': {'100': 5},
    '1002': {'100': 1},
    '1003': {'100': 2},
    '1004': {'101': 4}
}

cupos = {
    '100': 1,
    '101': 3,
    '102': 2
}

# Función para calcular la insatisfacción de una asignación
def calcular_insatisfaccion(asignacion, solicitudes):
    insatisfaccion_total = 0
    for estudiante, cursos in asignacion.items():
        insatisfaccion_estudiante = 0
        capacidad_priorizar = 3 * len(solicitudes[estudiante]) - 1  # Cálculo de la capacidad de priorización
        for curso in cursos:
            insatisfaccion_estudiante += solicitudes[estudiante].get(curso, 0)
        insatisfaccion_estudiante *= (1 - len(cursos) / capacidad_priorizar)
        insatisfaccion_total += insatisfaccion_estudiante
    return insatisfaccion_total / len(asignacion)

# Algoritmo de la mochila
def algoritmo_mochila(materias, solicitudes, cupos):
    estudiantes = list(solicitudes.keys())
    asignacion = {estudiante: [] for estudiante in estudiantes}
    insatisfacciones = {}

    while True:
        max_insatisfaccion = -float('inf')
        max_estudiante = None
        max_curso = None

        for estudiante in estudiantes:
            for curso, cantidad in solicitudes[estudiante].items():
                if cantidad > 0 and cupos[curso] > 0 and curso not in asignacion[estudiante]:
                    asignacion[estudiante].append(curso)
                    insat = calcular_insatisfaccion(asignacion, solicitudes)
                    asignacion[estudiante].remove(curso)

                    if insat > max_insatisfaccion:
                        max_insatisfaccion = insat
                        max_estudiante = estudiante
                        max_curso = curso

        if max_estudiante is None:
            break

        asignacion[max_estudiante].append(max_curso)
        cupos[max_curso] -= 1
        solicitudes[max_estudiante][max_curso] -= 1
        insatisfacciones[max_estudiante] = max_insatisfaccion

    # Eliminar estudiantes sin asignaciones
    asignacion = {estudiante: cursos for estudiante, cursos in asignacion.items() if cursos}

    return asignacion, insatisfacciones

# Encontrar la asignación óptima
mejor_asignacion, mejor_insatisfaccion = algoritmo_mochila(materias, solicitudes, cupos)

# Imprimir resultados
print(mejor_asignacion, mejor_insatisfaccion)
