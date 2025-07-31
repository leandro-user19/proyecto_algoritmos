#Explorar lugares:  organizados jerárquicamente por zonas. 

def explorar_por_zonas(archivo="rutas.txt"):
    try:
        with open (archivo, "r", encoding="utf-8") as f:
            print("\n---Lugares Turisticos Registrados Por ciudades--\n")
            ciudad_actual=""
            for linea in f:
                linea=linea.strip()
                if not linea:
                    continue
                if linea.endswith(":"):
                    ciudad_actual=linea[:-1]
                    print(f"Ciudad: {ciudad_actual}")
                else:
                    lugar, distancia, costo= linea.split("|")
                    print(f" ·Lugar: {lugar}, ·Distancia: {distancia}km, ·Costo: ${float(costo):.2f}")
    except FileNotFoundError:
        print("Error")



def seleccionar_puntos_a_visitar(puntos_turisticos):
    if len (puntos_turisticos)<2:
        print("Debe estar registrado al menos 2 puntos turisticos")
        return
    
    print("\n--Lista de puntos turísticos Disponibles--")
    for i, punto in enumerate(puntos_turisticos):
        print(f"{i+1}. Ciudad: {punto["ciudad"]}  |  Lugar: {punto["lugar"]}  |  Distancia: {punto["distancia"]} km  |  Costo: ${punto["costo"]:.2f}")

        seleccionados =[]
        while len(seleccionados)<2:
            try:
                seleccion=int(input(f"Ingrese el número del punto turistico ·{len(seleccionados)+1} que desea visitar"))
                if 1<=seleccion<=len(puntos_turisticos):
                    punto=puntos_turisticos[seleccion-1]
                    if punto not in seleccionados:
                        seleccionados.append(punto)
                    else:
                        print("Punto ya seleccionado")
                else:
                    print("Numero invalido")
            except ValueError:
                print("Error. Ingrese un número")

    # permitir que el usuario ingrese mas punto si lo desea
    while True:
        respuesta=input("¿Desea agregar otro punto turistico? (s/n): ").lower()
        if respuesta=="s":
            try:
                seleccion=int(input("Ingrese el número del punto turistico: "))
                if 1<=seleccion<=len(puntos_turisticos):
                    punto=puntos_turisticos[seleccion-1]
                    if punto not in seleccionados:
                        seleccionados.append(punto)
                    else:
                        print("Punto ya seleccionado anteriormente")
                else:
                    print("Número invalido")
            except ValueError:
                print("Error. Ingrese un número")
        elif respuesta=="n":
            break
        else:
            print("\nError. Respuesta inválida ingrese 's' o 'n': ")

    print("\n--Puntos turisticos seleccionados--")
    for p in seleccionados:
        print(f"Ciudad: {p["ciudad"]}  |  Lugar: {p["lugar"]}  |  Distancia: {p["distancia"]}km  |  Costo: ${p["costo"]:.2f}")
