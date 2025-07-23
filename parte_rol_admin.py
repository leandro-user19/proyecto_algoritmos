def acutalizar_rutas (punto):
    if not punto:
        print("No hay rutas")
        return
    for id, datos in punto.items():
        print(f"{id}. {datos['ciudad']} - {datos['lugar']} ({datos['distancia']} km, ${datos['costo']})\n")
    try:
        opcionactualizar=int(input("Eliga el punto turistico a actualizar: "))
        if opcionactualizar in punto:
                print("Ingrese los nuevos datos: ")
                ciudad= input("Ingrese la nueva ciudad: ")
                lugar=input("Ingrese el nuevo lugar: ")
                distancia=int(input("Ingrese la nueva distancia: "))
                costo=float(input("Ingrese el nuevo costo: "))

                punto[opcionactualizar]={
                    "ciudad": ciudad,
                    "lugar": lugar,
                    "distancia": distancia,
                    "costo": costo
                }
                print("Punto turistico actualizado correctamente👍")
                with open("rutas.txt", "w")as archivo:
                    for id, datos in punto.items():
                        linea=f"{id};{datos['ciudad']};{datos['lugar']};{datos['distancia']};{datos['costo']}\n"
                        archivo.write(linea)
                    print(f"Se guardó correctamente en {'rutas.txt'}")
        else: 
            print("No existe dicho punto turistico")
    except ValueError:
        print("Ingrese un caracter númerico porfavor")

def eliminar_rutas(punto):
    if not punto:
        print("No hay rutas")
        return
    for id, datos in punto.items():
        print(f"{id}. {datos['ciudad']} - {datos['lugar']} ({datos['distancia']} km, ${datos['costo']})\n")
    try:
        opcioneliminar=int(input("Ingrese el punto túristico a elminar: "))
        if opcioneliminar in punto:
            confirmacion=input("¿Esta seguro que desea eliminar el punto túristico seleccionado?: ")
            if confirmacion =="si":
                punto.pop(opcioneliminar)
                with open("rutas.txt", "w") as archivo:
                    for id, datos in punto.items():
                        linea = f"{id};{datos['ciudad']};{datos['lugar']};{datos['distancia']};{datos['costo']}\n"
                        archivo.write(linea)
                print("Punto túristico eliminado con exito")
        else:
            print("Acción cancelada")
            return
    except ValueError:
        print("Ingrese un número o caracter valido porfavor")

            
