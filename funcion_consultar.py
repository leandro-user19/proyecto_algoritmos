
import respaldo3

def consultar_ruta_conectada(rutas_conectadas):
    if not rutas_conectadas:
        print("\nAun no hay rutas conectadas.")
        return
    origen = validar_vacio("Ingrese el lugar turístico de origen: ")
    destino = validar_vacio("Ingrese el lugar turístico de destino: ")
    for ruta in rutas_conectadas:
        if ruta["origen"].lower() == origen.lower() and ruta["destino"].lower() == destino.lower():
            print(f"Ruta encontrada: De {ruta['origen']} a {ruta['destino']} | Distancia: {ruta['distancia']:.2f} km | Costo: ${ruta['costo']:.2f}")
            return
    print("No se encontró una ruta conectada entre esos puntos.")