def algoritmo_MergeSort(ruta):
    if len(ruta) == 1:
        return ruta
    else:
        indice_mitad = int(len(ruta)/2)
        mitad_izquierda = ruta[:indice_mitad]
        mitad_derecha = ruta[indice_mitad:]

        mitad_derecha = algoritmo_MergeSort(mitad_derecha)
        mitad_izquierda = algoritmo_MergeSort(mitad_izquierda)

        return combinar(mitad_derecha, mitad_izquierda)
    
def combinar(izquierda, derecha):
    resultado = []
    indice_izq = 0
    indice_der = 0

    while indice_izq < len(izquierda) and indice_der < len(derecha):
        if izquierda[indice_izq] < derecha[indice_der]:
            resultado.append(izquierda[indice_izq])
            indice_izq += 1
        else:
            resultado.append(derecha[indice_der])
            indice_der += 1
    if indice_der == len(derecha):
        resultado.extend(izquierda[indice_izq:])
    else:
        resultado.extend(derecha[indice_der:])
    return resultado


