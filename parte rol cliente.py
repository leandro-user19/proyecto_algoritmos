def actualizar_rutas_cliente(puntos_cliente):
    if not puntos_cliente:
        print("No hay rutas cargadas.")
        return

    for id, datos in puntos_cliente.items():
        print(f"{id}. {datos['ciudad']} - {datos['lugar']} ({datos['distancia']} km, ${datos['costo']})\n")
    
    try:
        opcion = int(input("Elija el punto turístico a actualizar: "))
        if opcion in puntos_cliente:
            print("Ingrese los nuevos datos:")
            ciudad = input("Nueva ciudad: ")
            lugar = input("Nuevo lugar: ")
            distancia = int(input("Nueva distancia (km): "))
            costo = float(input("Nuevo costo ($): "))

            puntos_cliente[opcion] = {
                "ciudad": ciudad,
                "lugar": lugar,
                "distancia": distancia,
                "costo": costo
            }

            print("Punto turístico actualizado en tu selección.")
        else:
            print("No existe ese punto en tu selección.")
    except ValueError:
        print("Debes ingresar un número válido.")

def eliminar_rutas_cliente(puntos_cliente):
    if not puntos_cliente:
        print("No hay rutas para eliminar.")
        return

    for id, datos in puntos_cliente.items():
        print(f"{id}. {datos['ciudad']} - {datos['lugar']} ({datos['distancia']} km, ${datos['costo']})\n")

    try:
        opcion = int(input("Elija el punto turístico a eliminar: "))
        if opcion in puntos_cliente:
            confirmacion = input("¿Seguro que deseas eliminar este punto? (si/no): ").lower()
            if confirmacion == "si":
                puntos_cliente.pop(opcion)
                print("Punto eliminado de tu selección.")
            else:
                print("Cancelado.")
        else:
            print("No se encontró el punto.")
    except ValueError:
        print("Ingrese un número válido.")


def guardar_seleccion_cliente(puntos_cliente, nombre_cliente):
    nombre_archivo = f"rutas-{nombre_cliente}.txt"
    with open(nombre_archivo, "w") as archivo:
        for id, datos in puntos_cliente.items():
            linea = f"{id};{datos['ciudad']};{datos['lugar']};{datos['distancia']};{datos['costo']}\n"
            archivo.write(linea)
    print(f"Selección guardada exitosamente en '{nombre_archivo}'")

def cargar_rutas_para_cliente():
    puntos = {}
    try:
        with open("rutas.txt", "r") as archivo:
            for i, linea in enumerate(archivo, start=1):
                partes = linea.strip().split(";")
                if len(partes) == 5:
                    ciudad, lugar, distancia, costo = partes[1], partes[2], int(partes[3]), float(partes[4])
                    puntos[i] = {
                        "ciudad": ciudad,
                        "lugar": lugar,
                        "distancia": distancia,
                        "costo": costo
                    }
    except FileNotFoundError:
        print("El archivo rutas.txt no existe.")
    return puntos


