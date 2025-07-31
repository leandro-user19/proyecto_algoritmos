
from respaldo3 import dijkstra
from respaldo3 import bubble_sort

def listar_itinerario(ruta_cliente, grafo):
    if not ruta_cliente:
        print("\nNo hay itinerarios guardados para listar.")
        return
    print("\n--- Tus Itinerarios Guardados ---")
    for idx, itinerario in enumerate(ruta_cliente):
        print(f"\nItinerario #{idx + 1}:")
        puntos = itinerario["puntos_visita"]
        if not puntos:
            print("  Este itinerario no tiene puntos seleccionados.")
            continue
        itinerario_ordenado = bubble_sort(puntos[:])  # Copia para no modificar la original
        costo_total_itinerario = 0.0
        distancia_total_itinerario = 0.0
        ruta_detallada = []
        print("  Puntos en este itinerario (orden alfabético):")
        for i, punto in enumerate(itinerario_ordenado):
            print(f"    {i+1}. {punto}")
        if len(itinerario_ordenado) >= 2:
            print("\n  Calculando costo y distancia de ruta sugerida:")
            for i in range(len(itinerario_ordenado) - 1):
                origen = itinerario_ordenado[i]
                destino = itinerario_ordenado[i+1]
                ruta_tramo, costo_tramo, distancia_tramo = dijkstra(grafo, origen, destino)
                if ruta_tramo:
                    costo_total_itinerario += costo_tramo
                    distancia_total_itinerario += distancia_tramo
                    ruta_detallada.append(f"    {origen} -> {destino} (Costo: ${costo_tramo:.2f}) (Distancia: {distancia_tramo:.2f} km)")
                else:
                    print(f"    Advertencia: No se encontró ruta directa entre {origen} y {destino}.")
            print("\n  Resumen por tramo:")
            for tramo in ruta_detallada:
                print(tramo)
            itinerario["costo_total"] = costo_total_itinerario
            itinerario["distancia_total"] = distancia_total_itinerario
            print(f"\n  Costo total: ${itinerario['costo_total']:.2f} | Distancia total: {itinerario['distancia_total']:.2f} km")
        elif len(itinerario_ordenado) == 1:
            print("\n  Solo hay un punto en el itinerario. Necesitas al menos dos puntos para una ruta.")
        print("----------------------------------")