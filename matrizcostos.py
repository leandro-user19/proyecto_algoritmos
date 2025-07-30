def mostrar_mapa_distancias(rutas_conectadas):
#construir la matriz
    if not rutas_conectadas:
        print("No hay rutas conectadas para mostrar el mapa de distancias.")
        return

    lugares = sorted(set(r["origen"] for r in rutas_conectadas) | set(r["destino"] for r in rutas_conectadas))

    matriz = {origen: {destino: "/" for destino in lugares} for origen in lugares}

    for lugar in lugares:
        matriz[lugar][lugar] = 0

    for ruta in rutas_conectadas:
        origen = ruta["origen"]
        destino = ruta["destino"]
        distancia = ruta["distancia"]
        matriz[origen][destino] = distancia

    print("\nMapa de Distancias (en km):")
    encabezado = " " * 15 + "".join(f"{lugar[:12]:>13}" for lugar in lugares)
    print(encabezado)
    print("-" * len(encabezado))
    for origen in lugares:
        fila = f"{origen[:12]:<15}"
        for destino in lugares:
            valor = matriz[origen][destino]
            fila += f"{str(valor):>13}"
        print(fila)
    print("-" * len(encabezado))
