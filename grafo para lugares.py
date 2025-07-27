def grafo_informacion(archivo_rutas):
    grafo = {}
    with open(archivo_rutas, "r") as archivo:
        for linea in archivo:
            origen, destino, distancia, costo = linea.strip().split(",")
            distancia = int(distancia)
            costo = float(costo)

            if origen not in grafo:
                grafo[origen] = {}
            if destino not in grafo:
                grafo[destino] = {}

            grafo[origen][destino] = {"distancia": distancia, "costo": costo}
            grafo[destino][origen] = {"distancia": distancia, "costo": costo}

    return grafo

def mapa(grafo):
    print("\nMapa de lugares turísticos conectados:\n")
    mostrados = set()
    for origen in grafo:
        for destino in grafo[origen]:
            ruta = tuple(sorted([origen, destino]))
            if ruta not in mostrados:
                info = grafo[origen][destino]
                print(f"{origen} ----> {destino}: {info['distancia']} km - ${info['costo']:.2f}")
                mostrados.add(ruta)
