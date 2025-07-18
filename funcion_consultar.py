def consultar (arreglo):
    if not arreglo:
        print("El arreglo está vacío.")
        return None
    
    punto_turistico = input("Ingrese el punto turístico a consultar: ")

    for item in arreglo:
            if item["punto turistico"].lower() == punto_turistico.lower():
                return item
    return None