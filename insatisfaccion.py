from itertools import product, combinations

# insatisfaccion

def insatisfaccionEstudiante(estudiante, distribucion, solicitudes):
    #print(f"Estudiante: {estudiante}")
    #print(f"Solicitudes: {solicitudes}") 
    solicitud = set(solicitudes.get(estudiante, {}))
    #print(f"Solicitud: {solicitud}")
    asignacion = set(distribucion[estudiante])
    noAsignadas = solicitud - asignacion
    puntosPrioridad = 3 * len(solicitud) - 1

    if len(solicitud) > 0:
        puntosNoAsignados = 0

        if len(noAsignadas) <= len(solicitud) / 2:
            for noAsig in noAsignadas:
                puntosNoAsignados += solicitudes[estudiante][noAsig]
        else:
            puntosNoAsignados = puntosPrioridad
            for asig in asignacion:
                puntosNoAsignados -= solicitudes[estudiante][asig]

        insatistaccion = (1 - (len(asignacion) / len(solicitud))) * (puntosNoAsignados / puntosPrioridad)
    else:
        insatistaccion = 0.0  # Establecer insatisfacción a cero si no hay solicitudes

    return insatistaccion



def insatisfaccionTotal(cantidadEstudiantes, distribucion, solicitudes):
  insatistaccionGeneral = 0

  for estudiante in solicitudes:
    insatistaccionGeneral += insatisfaccionEstudiante(
        estudiante, distribucion, solicitudes)

  return insatistaccionGeneral/cantidadEstudiantes
