import heapq



class PuntoTuristico:
    def __init__(self, id, ciudad, lugar, distancia, costo):
        self.id = id
        self.ciudad = ciudad
        self.lugar = lugar
        self.distancia = distancia
        self.costo = costo
        self.conexiones = {}  # id del destino

    def agregar_conexion(self, destino_id, costo):
        self.conexiones[destino_id] = costo

grafo={}

for id_punto, datos in punto.items():
    grafo[id_punto]= PuntoTuristico(
        id=id_punto, 
        ciudad=datos["ciudad"], 
        lugar=datos["lugar"], 
        distancia=datos["distancia"],
        costo=datos["costo"]
    )

def conectar_puntos():
    while True:
        try:
            origen=int(input("Id del punto de origen (escriba 0 para salir): "))
            if origen == 0:
                break
            destino=int(input("Id del punto del destino: "))
            if destino== origen:
                print("No se puede conectar con el mismo punto de origen")
                continue
            costo= float(input("Costo del viaje entre origen y punto de destino: "))

            grafo[origen].agregarconexion(destino, costo)
            print(f"Conexión agregada de {origen} a {destino} con costo {costo}.\n")
        except KeyError:
            print("Alguno de los IDs no existe en el grafo.")
        except ValueError:
            print("Entrada inválida. Asegúrate de ingresar números.")

