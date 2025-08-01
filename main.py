from io import open
import heapq
from collections import deque

CLAVE = "1234"  #Clave de administrador
USUARIO = "admin"  #Usuario de administrador

def bubble_sort(arr, key = lambda x: x):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if key(arr[j]) > key(arr[j + 1]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# registrar usuario
def usuario_validar(usuario):
    parte=usuario.split("@")
    if len(parte)!=2:
        return False
    usuario,dominio=parte
    nombre_usuario=usuario.split(".")  #para el formato nombre.apellido del usuario
    if len(nombre_usuario)!=2:
        return False
    if not usuario_valido(nombre_usuario[0]) or not usuario_valido(nombre_usuario[1]):
        return False
    if "." not in dominio:   #valida que el dominio despues del @ contenga un punto
        return False
    return True

def usuario_valido(nombre):
    for c in nombre:
        if not (c.isalpha() or c in "ÁÉÍÓÚáéíóúÑñ"):
            return False
    return True

def contraseña_segura(contraseña):
    if(len(contraseña)>=6 and
       any(c.isupper()for c in contraseña) and
       any(c.islower() for c in contraseña) and
       any(c.isdigit()for c in contraseña)):
        return True
    return False

def validar_vacio(mensaje):
    while True:
        texto = input(mensaje)
        if texto.strip():
            return texto.strip()
        print("El campo no puede estar vacío. Por favor, ingrese un texto.")
        
def validar_numero(mensaje,tipo=float):
    while True:
        try:
            numero = tipo(input(mensaje))
            if numero < 0:
                print("El número debe ser positivo.")
                continue
            return numero
        except ValueError:
            print("Por favor, ingrese un número válido.")

def registrar_usuario(usuarios):
    print("\n--Registro de Usuario--")
    nombres = validar_vacio("Ingrese su nombre y apellido: ")
    edad = validar_numero("Ingrese su edad: ", int)
    while True:
        usuario = validar_vacio("Ingrese su usuario: ")
        if usuario_validar(usuario):
            usuario_existente = False
            for u in usuarios:
                if u["usuario"] == usuario:
                    print("El usuario ya existe. Por favor, elija otro.")
                    usuario_existente = True
                    break
            if not usuario_existente:
                break
        else:
            print("Error. El formato debe de ser nombre.apellido@dominio.com")
    while True:
        clave = validar_vacio("Ingrese su contraseña: ")
        if contraseña_segura(clave):
            break
        else:
            print("Error de contraseña. Debe tener al menos 6 caracteres, una mayúscula, una minúscula y un número.")
    usuarios.append({
        "nombres": nombres,
        "edad": edad,
        "usuario": usuario,
        "clave": clave
    })
    print("Cliente registrado exitosamente.")
    return True

def guardar_datos(usuarios, archivo):
    try:
        with open(archivo, "w", encoding="utf-8") as file:
            for usuario in usuarios:
                file.write(f"{usuario['usuario']},{usuario['clave']},{usuario['nombres']},{usuario['edad']}\n")
        print("Datos guardados exitosamente.")
    except Exception as e:
        print(f"Error al guardar los datos: {e}")

def cargar_datos(archivo):
    usuarios = []
    try:
        with open(archivo, "r", encoding="utf-8") as file:
            for linea in file:
                linea = linea.strip()
                if linea:
                    usuario, clave, nombres, edad = linea.split(",")
                    usuarios.append({
                        "usuario": usuario,
                        "clave": clave,
                        "nombres": nombres,
                        "edad": int(edad)
                    })
        return usuarios
    except FileNotFoundError:
        print(f"El archivo '{archivo}' no fue encontrado. Se retornará una lista vacía de usuarios.")
        return []
    except Exception as e:
        print(f"Error al cargar los datos: {e}. Se retornará una lista vacía.")
        return []

#rol administrador
def agregar_datos_turisticos(puntos_turisticos):
    print("Ingrese los siguientes datos")
    ciudad = validar_vacio("Ciudad: ")
    lugar = validar_vacio("Lugar turístico: ")

    punto={
        "ciudad":ciudad,
        "lugar":lugar,
    }
    puntos_turisticos.append(punto)
    print("\nDatos del punto turistico agregada correctamente.")

def conectar_puntos_turisticos(puntos_turisticos,rutas_conectadas):
    if not puntos_turisticos:
        print("\nAun no hay datos agregados")
        return
    print("\n--- Conectar Puntos Turísticos ---")
    print("Seleccione dos puntos turísticos para conectar:")
    for i, punto in enumerate(puntos_turisticos):
        print(f"{i + 1}. Ciudad: {punto['ciudad']} | Lugar turístico: {punto['lugar']}")
    while True:
        try:
            indice1 = int(input("Ingrese el número del primer punto turístico (origen): ")) - 1
            indice2 = int(input("Ingrese el número del segundo punto turístico (destino): ")) - 1
            if not (0 <= indice1 < len(puntos_turisticos) and 0 <= indice2 < len(puntos_turisticos)):
                print("Índices inválidos. Por favor, intente de nuevo.")
                continue
            if indice1 == indice2:
                print("No se puede conectar un punto turístico consigo mismo. Intente de nuevo.")
                continue
            origen = puntos_turisticos[indice1]
            destino = puntos_turisticos[indice2]
            ruta_existente = False
            for r in rutas_conectadas:
                if (r['origen'] == origen['lugar'] and r['destino'] == destino['lugar']) or \
                   (r['origen'] == destino['lugar'] and r['destino'] == origen['lugar']):
                    print(f"La conexión entre {origen['lugar']} y {destino['lugar']} ya existe.")
                    ruta_existente = True
                    break
            if ruta_existente:
                break # Salir del bucle si la ruta ya existe
            distancia = validar_numero(f"Ingrese la distancia entre {origen['lugar']} y {destino['lugar']} (en km): ", float)
            costo = validar_numero(f"Ingrese el costo del viaje entre {origen['lugar']} y {destino['lugar']} (en USD): ", float)
            ruta_ida = {
                "origen": origen['lugar'],
                "destino": destino['lugar'],
                "distancia": distancia,
                "costo": costo
            }
            rutas_conectadas.append(ruta_ida)
            print(f"\nConexión creada: {origen['lugar']} <-> {destino['lugar']}")
            ruta_vuelta = {
                "origen": destino['lugar'],
                "destino": origen['lugar'],
                "distancia": distancia, # Misma distancia
                "costo": costo        # Mismo costo
            }
            rutas_conectadas.append(ruta_vuelta)
            break
        except ValueError:
            print("Entrada inválida. Por favor, ingrese números válidos.")

def guardar_rutas_conectadas(rutas_conectadas, archivo):
    try:
        with open(archivo, "w", encoding="utf-8") as file:
            for ruta in rutas_conectadas:
                file.write(f"{ruta['origen']},{ruta['destino']},{ruta['distancia']:.2f},{ruta['costo']:.2f}\n")
    except Exception as e:
        print(f"Error al guardar las rutas conectadas: {e}")

def cargar_rutas_conectadas(archivo):
    rutas_conectadas = []
    try:
        with open(archivo, "r", encoding="utf-8") as file:
            for linea in file:
                linea = linea.strip()
                if linea:
                    origen, destino, distancia, costo = linea.split(",")
                    rutas_conectadas.append({
                        "origen": origen,
                        "destino": destino,
                        "distancia": float(distancia),
                        "costo": float(costo)
                    })
        return rutas_conectadas
    except FileNotFoundError:
        print(f"El archivo '{archivo}' no fue encontrado. Se retornará una lista vacía de rutas conectadas.")
        return []
    except Exception as e:
        print(f"Error al cargar las rutas conectadas: {e}. Se retornará una lista vacía.")
        return []

def listar_rutas_conectadas(rutas_conectadas):
    if not rutas_conectadas:
        print("\nAun no hay rutas conectadas.")
        return
    while True:
        print("\n--- Elija como desea ordenar las rutas conectadas ---")
        print("1. Por distancia (menor a mayor)")
        print("2. Por costo (menor a mayor)")
        opcion = input("Seleccione una opción: ")
        rutas_solo_ida = []
        rutas_ya_vistas = set() # Usamos un conjunto para almacenar las claves de las rutas ya vistas
        for ruta in rutas_conectadas:
            key = tuple(sorted((ruta['origen'], ruta['destino'])))
            if key not in rutas_ya_vistas:
                rutas_solo_ida.append(ruta)
                rutas_ya_vistas.add(key)
        if not rutas_solo_ida:
            print("No hay rutas únicas para mostrar.")
            return
        rutas_conectadas_ordenadas = list(rutas_solo_ida) # Ahora ordenamos solo las rutas "ida"
        if opcion == "1":
            rutas_conectadas_ordenadas = bubble_sort(rutas_conectadas_ordenadas, key=lambda x: x['distancia'])
        elif opcion == "2":
            rutas_conectadas_ordenadas = bubble_sort(rutas_conectadas_ordenadas, key=lambda x: x['costo'])
        else:
            print("Opción no válida. Por favor, intente nuevamente.")
            continue
        print("\n--- Rutas Conectadas ---")
        for i, ruta in enumerate(rutas_conectadas_ordenadas):
            print(f"{i + 1}. De {ruta['origen']} a {ruta['destino']} | Distancia: {ruta['distancia']:.2f} km | Costo: ${ruta['costo']:.2f}")
        break

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

def actualizar_datos_turisticos(puntos_turisticos, rutas_conectadas):
    print("\n--- Actualizar Datos ---")
    print("1. Actualizar Punto Turístico")
    print("2. Actualizar Ruta Conectada")
    print("3. Volver al menú principal")
    opcion = validar_numero("Seleccione una opción: ", int)
    if opcion == 1:
        if not puntos_turisticos:
            print("\nNo hay puntos turísticos para actualizar.")
            return
        print("\n--- Actualizar Punto Turístico ---")
        for i, punto in enumerate(puntos_turisticos):
            print(f"{i + 1}. Ciudad: {punto['ciudad']} | Lugar turístico: {punto['lugar']}")
        while True:
            try:
                indice = int(input("Ingrese el número del punto turístico a actualizar: ")) - 1
                if 0 <= indice < len(puntos_turisticos):
                    punto_a_actualizar = puntos_turisticos[indice]
                    antiguo_lugar = punto_a_actualizar['lugar']
                    nueva_ciudad = validar_vacio("Nueva Ciudad: ")
                    nuevo_lugar = validar_vacio("Nuevo Lugar turístico: ")
                    punto_a_actualizar['ciudad'] = nueva_ciudad
                    punto_a_actualizar['lugar'] = nuevo_lugar
                    print("\nPunto turístico actualizado correctamente.")
                    for ruta in rutas_conectadas:
                        if ruta['origen'] == antiguo_lugar:
                            ruta['origen'] = nuevo_lugar
                        if ruta['destino'] == antiguo_lugar:
                            ruta['destino'] = nuevo_lugar
                    print("Rutas conectadas actualizadas con los nuevos nombres de lugares.")
                    break
                else:
                    print("Índice inválido. Por favor, intente de nuevo.")
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un número válido.")
    elif opcion == 2:
        if not rutas_conectadas:
            print("\nNo hay rutas conectadas para actualizar.")
            return
        print("\n--- Actualizar Ruta Conectada ---")
        rutas_unicas_mostradas = []
        indices_originales = []
        for i, ruta in enumerate(rutas_conectadas):
            key = tuple(sorted((ruta['origen'], ruta['destino'])))
            if key not in [tuple(sorted((r['origen'], r['destino']))) for r in rutas_unicas_mostradas]:
                rutas_unicas_mostradas.append(ruta)
                indices_originales.append(i) # Guardamos el índice original para futuras referencias
        if not rutas_unicas_mostradas:
            print("No hay rutas únicas para mostrar.")
            return
        for i, ruta_unica in enumerate(rutas_unicas_mostradas):
            print(f"{i + 1}. Origen: {ruta_unica['origen']} | Destino: {ruta_unica['destino']} | Distancia: {ruta_unica['distancia']} km | Costo: ${ruta_unica['costo']}")
        while True:
            try:
                seleccion_unica = int(input("Ingrese el número de la ruta a actualizar: ")) - 1
                if 0 <= seleccion_unica < len(rutas_unicas_mostradas):
                    ruta_seleccionada_unica = rutas_unicas_mostradas[seleccion_unica]
                    nueva_distancia = validar_numero("Nueva Distancia: ", float)
                    nuevo_costo = validar_numero("Nuevo Costo: ", float)
                    for ruta in rutas_conectadas:
                        if (ruta['origen'] == ruta_seleccionada_unica['origen'] and ruta['destino'] == ruta_seleccionada_unica['destino']) or \
                           (ruta['origen'] == ruta_seleccionada_unica['destino'] and ruta['destino'] == ruta_seleccionada_unica['origen']):
                            ruta['distancia'] = nueva_distancia
                            ruta['costo'] = nuevo_costo
                    print("\nRuta conectada (ida y vuelta) actualizada correctamente.")
                    break
                else:
                    print("Índice inválido. Por favor, intente de nuevo.")
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un número válido.")
    elif opcion == 3:
        print("Volviendo al menú principal.")
    else:
        print("Opción inválida. Intente de nuevo.")

def eliminar_datos_turisticos(puntos_turisticos, rutas_conectadas):
    print("\n--- Eliminar Datos ---")
    print("1. Eliminar Punto Turístico")
    print("2. Volver al menú principal")
    opcion = validar_numero("Seleccione una opción: ", int)
    if opcion == 1:
        if not puntos_turisticos:
            print("\nNo hay puntos turísticos para eliminar.")
            return
        print("\n--- Eliminar Punto Turístico ---")
        for i, punto in enumerate(puntos_turisticos):
            print(f"{i + 1}. Ciudad: {punto['ciudad']} | Lugar turístico: {punto['lugar']}")
        while True:
            try:
                indice = int(input("Ingrese el número del punto turístico a eliminar: ")) - 1
                if 0 <= indice < len(puntos_turisticos):
                    punto_eliminado = puntos_turisticos.pop(indice)
                    lugar_eliminado = punto_eliminado['lugar']
                    print(f"\nLugar turístico '{lugar_eliminado}' eliminado correctamente.")
                    rutas_a_mantener = []
                    rutas_eliminadas_count = 0
                    for ruta in rutas_conectadas:
                        if ruta['origen'] == lugar_eliminado or ruta['destino'] == lugar_eliminado:
                            rutas_eliminadas_count += 1
                        else:
                            rutas_a_mantener.append(ruta)
                    rutas_conectadas[:] = rutas_a_mantener # Actualiza la lista original
                    if rutas_eliminadas_count > 0:
                        print(f"Se eliminaron {rutas_eliminadas_count} rutas conectadas que incluían '{lugar_eliminado}'.")
                    else:
                        print("No se encontraron rutas conectadas que incluyeran este punto turístico.")
                    break
                else:
                    print("Índice inválido. Por favor, intente de nuevo.")
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un número válido.")
    elif opcion == 2:
        print("Volviendo al menú principal.")
    else:
        print("Opción inválida. Intente de nuevo.")

def guardar_puntos_turisticos(puntos_turisticos, archivo):
    try:
        with open(archivo, "w", encoding="utf-8") as file:
            for punto in puntos_turisticos:
                file.write(f"{punto['ciudad']},{punto['lugar']}\n")
    except Exception as e:
        print(f"Error al guardar los puntos turísticos: {e}")

def cargar_puntos_turisticos(archivo):
    puntos_turisticos = []
    try:
        with open(archivo, "r", encoding="utf-8") as file:
            for linea in file:
                linea = linea.strip()
                if linea:
                    ciudad, lugar = linea.split(",")
                    puntos_turisticos.append({
                        "ciudad": ciudad,
                        "lugar": lugar,
                    })
        return puntos_turisticos
    except FileNotFoundError:
        print(f"El archivo '{archivo}' no fue encontrado. Se retornará una lista vacía de puntos turísticos.")
        return []
    except Exception as e:
        print(f"Error al cargar los puntos turísticos: {e}. Se retornará una lista vacía.")
        return []
 
def menu_turismo_admin():
    archivo_puntos = "puntos_turisticos.txt"
    archivo_rutas = "rutas_conectadas.txt"
    puntos_turisticos = cargar_puntos_turisticos(archivo_puntos)
    rutas_conectadas = cargar_rutas_conectadas(archivo_rutas)
    while True:
        print("\n--- Menú de Administración de Turismo ---")
        print("1. Agregar puntos turísticos")
        print("2. Conectar puntos turísticos")
        print("3. Listar rutas conectadas")
        print("4. Consultar ruta conectada")
        print("5. Actualizar datos turísticos")
        print("6. Eliminar datos turísticos")
        print("7. Volver al menú principal")
        opcion=input("Seleccione una opción: ")
        if opcion=="1":
            agregar_datos_turisticos(puntos_turisticos)
            guardar_puntos_turisticos(puntos_turisticos, archivo_puntos)
        elif opcion=="2":
            conectar_puntos_turisticos(puntos_turisticos, rutas_conectadas)
            guardar_rutas_conectadas(rutas_conectadas, archivo_rutas)
        elif opcion=="3":
            listar_rutas_conectadas(rutas_conectadas)
        elif opcion=="4":
            consultar_ruta_conectada(rutas_conectadas)
        elif opcion=="5":
            actualizar_datos_turisticos(puntos_turisticos, rutas_conectadas)
            guardar_puntos_turisticos(puntos_turisticos, archivo_puntos)
            guardar_rutas_conectadas(rutas_conectadas, archivo_rutas)
        elif opcion=="6":
            eliminar_datos_turisticos(puntos_turisticos, rutas_conectadas)
            guardar_puntos_turisticos(puntos_turisticos, archivo_puntos)
            guardar_rutas_conectadas(rutas_conectadas, archivo_rutas)
        elif opcion=="7":
            print("\nVolviendo al menú principal...")
            break
        else:
            print("Opción no válida.")

#rol cliente
def cargar_grafo_conexiones(archivo):
    grafo = {}
    try:
        with open(archivo, "r", encoding="utf-8") as file:
            for linea in file:
                linea = linea.strip()
                if not linea:
                    continue
                origen, destino, distancia, costo = linea.split(",")
                distancia = float(distancia)
                costo = float(costo)
                if origen not in grafo:
                    grafo[origen] = []
                grafo[origen].append({"destino": destino, "distancia": distancia, "costo": costo})
        return grafo
    except FileNotFoundError:
        print(f"El archivo '{archivo}' no fue encontrado. Se retornará un grafo vacío.")
        return {}
    except Exception as e:
        print(f"Error al cargar el grafo: {e}. Se retornará un grafo vacío.")
        return {}

#mapa de distancia entre lugares turisticos basa en matriz
def mostrar_mapa_lugares_conectados(grafo):
    if not grafo:
        print("No hay datos de rutas cargados.")
        return
    print("\n--- Mapa de Lugares Turísticos Conectados ---")
    conexiones_mostradas = set()
    for origen, conexiones in grafo.items():
        for conexion in conexiones:
            destino = conexion['destino']
            distancia = conexion['distancia']
            costo = conexion['costo']
            key = tuple(sorted((origen, destino)))
            if key not in conexiones_mostradas:
                print(f"{origen} <-> {destino} (Distancia: {distancia:.2f} km, Costos: ${costo:.2f})")
                conexiones_mostradas.add(key)
    print("-----------------------------")

def mostrar_mapa_distancias(rutas_conectadas):
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
    print("\nMapa de Distancias:")
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

def mostrar_matriz_distancias_cliente():
    archivo = "rutas_conectadas.txt"
    rutas = cargar_rutas_conectadas(archivo)
    mostrar_mapa_distancias(rutas)

def dijkstra(grafo, inicio, fin):
    if inicio not in grafo or fin not in grafo:
        return None, float('inf'), float('inf') # Retornar ruta nula, costo infinito y distancia infinita
    distancias = {vertice: (float('inf'), float('inf')) for vertice in grafo}
    distancias[inicio] = (0, 0) # (costo, distancia) inicial
    prioridades = [(0, 0, inicio)] # (costo, distancia, vertice)
    caminos = {vertice: [] for vertice in grafo}
    caminos[inicio] = [inicio]
    while prioridades:
        costo_actual, distancia_actual, vertice_actual = heapq.heappop(prioridades)
        if costo_actual > distancias[vertice_actual][0]:
            continue
        if vertice_actual == fin:
            return caminos[vertice_actual], distancias[vertice_actual][0], distancias[vertice_actual][1]
        for conexion in grafo.get(vertice_actual, []):
            vecino = conexion["destino"]
            costo_viaje = conexion["costo"]
            distancia_viaje = conexion["distancia"] # Obtener la distancia de la conexión
            nuevo_costo = costo_actual + costo_viaje
            nueva_distancia = distancia_actual + distancia_viaje
            if nuevo_costo < distancias[vecino][0]:
                distancias[vecino] = (nuevo_costo, nueva_distancia)
                caminos[vecino] = caminos[vertice_actual] + [vecino]
                heapq.heappush(prioridades, (nuevo_costo, nueva_distancia, vecino))
            elif nuevo_costo == distancias[vecino][0] and nueva_distancia < distancias[vecino][1]:
                distancias[vecino] = (nuevo_costo, nueva_distancia)
                caminos[vecino] = caminos[vertice_actual] + [vecino]
                heapq.heappush(prioridades, (nuevo_costo, nueva_distancia, vecino))
    return None, float('inf'), float('inf') # No se encontró un camino

def consultar_ruta_optima(grafo):
    if not grafo:
        print("No hay datos de rutas cargados para consultar.")
        return
    print("\n--- Consultar Ruta Óptima ---")
    puntos_disponibles = bubble_sort(list(grafo.keys()))
    print("Puntos disponibles:", ", ".join(puntos_disponibles))
    origen = input("Ingrese el punto de origen: ").strip()
    destino = input("Ingrese el punto de destino: ").strip()
    if origen not in grafo:
        print(f"Error: El punto de origen '{origen}' no se encuentra en el mapa.")
        return
    if destino not in grafo:
        print(f"Error: El punto de destino '{destino}' no se encuentra en el mapa.")
        return
    if origen == destino:
        print("El origen y el destino son el mismo punto. El costo es $0.")
        return
    ruta, costo, distancia = dijkstra(grafo, origen, destino)
    if ruta:
        print(f"\nRuta óptima de {origen} a {destino}:")
        print(" -> ".join(ruta))
        print(f"Costo total: ${costo:.2f}")
        print(f"Distancia total: {distancia:.2f} km")
    else:
        print(f"No se encontró una ruta de {origen} a {destino}.")
    print("-----------------------------")

#Creo el arbol jerarquico que listara ciudades con sus respectivos puntos turisticos
def inorden(nodo):
    if nodo is not None:
        inorden(nodo.izq)
        print(f"- {nodo.ciudad} {nodo.punto}")
        inorden(nodo.der)

class NodoCiudad:
    def __init__(self, ciudad):
        self.ciudad = ciudad
        self.puntos_t = []
        self.izq = None
        self.der = None
    def agregar_punto(self, punto):
        self.puntos_t.append(punto)

def insertar_ciudad(raiz, ciudad, punto):
    if raiz is None:
        nodo = NodoCiudad(ciudad)
        nodo.agregar_punto(punto)
        return nodo
    if ciudad.lower() < raiz.ciudad.lower():
        raiz.izq = insertar_ciudad(raiz.izq, ciudad, punto)
    elif ciudad.lower() > raiz.ciudad.lower():
        raiz.der = insertar_ciudad(raiz.der, ciudad, punto)
    else:
        raiz.agregar_punto(punto)
    return raiz

def construir_arbol_desde_archivo(archivo):
    raiz = None
    try:
        with open(archivo ,"r", encoding="UTF-8") as arbol:
            for linea in arbol:
                if linea.strip():
                    ciudad, punto = linea.strip().split(",")
                    raiz = insertar_ciudad(raiz, ciudad.strip(), punto.strip())
        return raiz
    except Exception as f:
        print(f"Error al intentar leer el archivo {f}")

def listar_ciudad_inorden(nodo, lista):
    if nodo:
        listar_ciudad_inorden(nodo.izq, lista)
        lista.append(nodo)
        listar_ciudad_inorden(nodo.der, lista)

def menu_ciudades(raiz):
    ciudades = []
    listar_ciudad_inorden(raiz, ciudades)
    if not ciudades:
        print("No hay registros de ciudades aun.")
        return
    print("\nCIUDADES DISPONIBLES   ")
    for i, ciudad in enumerate(ciudades, 1):
        print(f"{i}. {ciudad.ciudad}")
    try:
        opcion = int(input("Selecciona una ciudad por su numero: "))
        if 1 <= opcion <= len(ciudades):
            seleccion = ciudades[opcion - 1]
            print(f"\n Lugares turisticos en {seleccion.ciudad}")
            for punto in seleccion.puntos_t:
                print(f"- {punto}")
        else:
            print("EL numero seleccionado no existe en esta lista.")
    except ValueError:
        print("Entrada invalida")

def seleccionar_puntos_visita(grafo, ruta_cliente):
    print("\n--- Seleccionar Lugares Turísticos a Visitar para tu Itinerario ---")
    puntos_disponibles = bubble_sort(list(grafo.keys()))
    if not puntos_disponibles:
        print("No hay lugares turísticos disponibles en el mapa para seleccionar.")
        return
    print("Lugares Turísticos disponibles:")
    for i, punto in enumerate(puntos_disponibles):
        print(f"{i+1}. {punto}")
    print("\nIngrese los lugares que desea visitar (ingrese 'fin' para terminar).")
    print("Mínimo dos lugares.")
    puntos_seleccionados_para_nuevo_itinerario = []
    while True:
        punto_str = validar_vacio("Ingrese un punto turístico: ")
        if punto_str.lower() == 'fin':
            if len(puntos_seleccionados_para_nuevo_itinerario) < 2:
                print("Debe seleccionar al menos dos puntos turísticos.")
            else:
                break
        punto_seleccionado = None
        try:
            idx = int(punto_str) - 1
            if 0 <= idx < len(puntos_disponibles):
                punto_seleccionado = puntos_disponibles[idx]
        except ValueError:
            if punto_str in puntos_disponibles:
                punto_seleccionado = punto_str
        if punto_seleccionado:
            if punto_seleccionado not in puntos_seleccionados_para_nuevo_itinerario:
                puntos_seleccionados_para_nuevo_itinerario.append(punto_seleccionado)
                print(f"'{punto_seleccionado}' añadido. Itinerario actual: {', '.join(puntos_seleccionados_para_nuevo_itinerario)}")
            else:
                print(f"'{punto_seleccionado}' ya está en tu itinerario.")
        else:
            print(f"'{punto_str}' no es un punto válido. Por favor, elija de la lista.")
    if puntos_seleccionados_para_nuevo_itinerario:
        nuevo_itinerario = {
            "puntos_visita": puntos_seleccionados_para_nuevo_itinerario,
            "costo_total": 0.0,
            "distancia_total": 0.0
        }
        ruta_cliente.append(nuevo_itinerario)
        print("\nSelección de puntos finalizada y guardada en el itinerario.")
    else:
        print("\nNo se seleccionaron puntos para un nuevo itinerario.")
    print("-------------------------------------------------------------------")

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

def actualizar_eliminar_seleccion(ruta_cliente, grafo):
    if not ruta_cliente:
        print("\nSu itinerario está vacío. No hay nada que actualizar.")
        return
    print("\n--- Actualizar Itinerario ---")
    if not ruta_cliente:
        print("No hay itinerarios para actualizar.")
        return
    while True:
        print("\nItinerarios disponibles:")
        for i, itinerario in enumerate(ruta_cliente):
            print(f"{i+1}. Puntos: {', '.join(itinerario['puntos_visita'])}")
        try:
            opcion_itinerario_str = input("Seleccione el número de itinerario a actualizar (0 para terminar): ").strip()
            if opcion_itinerario_str == '0':
                break
            opcion_itinerario_idx = int(opcion_itinerario_str) - 1
            if not (0 <= opcion_itinerario_idx < len(ruta_cliente)):
                print("Número de itinerario inválido. Intente de nuevo.")
                continue
            itinerario_a_modificar = ruta_cliente[opcion_itinerario_idx]
            puntos_actuales = itinerario_a_modificar["puntos_visita"]
            print(f"\nEditando Itinerario #{opcion_itinerario_idx + 1}. Puntos actuales: {', '.join(puntos_actuales)}")
            while True:
                print("Opciones de actualización para este itinerario:")
                print("1. Añadir un punto")
                print("2. Eliminar un punto")
                print("0. Terminar edición de este itinerario")
                opcion = input("Ingrese su opción: ").strip()
                if opcion == '1':
                    puntos_disponibles_mapa = bubble_sort(list(grafo.keys()))
                    puntos_para_anadir = [p for p in puntos_disponibles_mapa if p not in puntos_actuales]
                    if not puntos_para_anadir:
                        print("\nNo hay más puntos turísticos disponibles para añadir a este itinerario.")
                        continue 
                    print("\nLugares turísticos disponibles para añadir:")
                    for i, punto in enumerate(puntos_para_anadir): # Ahora itera sobre los puntos_para_anadir
                        print(f"{i+1}. {punto}")
                    punto_a_anadir = input("Ingrese el nombre o número del punto a añadir: ").strip()
                    punto_validado = None
                    try:
                        idx = int(punto_a_anadir) - 1
                        if 0 <= idx < len(puntos_para_anadir): # Cambiado a puntos_para_anadir
                            punto_validado = puntos_para_anadir[idx]
                    except ValueError:
                        if punto_a_anadir in puntos_para_anadir: # Cambiado a puntos_para_anadir
                            punto_validado = punto_a_anadir
                    if punto_validado:
                        if punto_validado not in puntos_actuales: 
                            puntos_actuales.append(punto_validado)
                            print(f"'{punto_validado}' ha sido añadido.")
                        else:
                            print(f"'{punto_validado}' ya está en el itinerario (esto no debería ocurrir si la lista de disponibles se filtra correctamente).")
                    else:
                        print("Punto no válido o no disponible para añadir.")
                elif opcion == '2':
                    if not puntos_actuales:
                        print("El itinerario está vacío para eliminar.")
                        continue
                    if len(puntos_actuales) <= 2:
                        print("No puedes eliminar un punto. Debes mantener al menos dos puntos en tu itinerario.")
                        continue
                    print("\nLugares turísticos en su itinerario para eliminar:")
                    for i, punto in enumerate(puntos_actuales):
                        print(f"{i+1}. {punto}")
                    punto_a_eliminar_str = input("Ingrese el nombre o número del punto a eliminar: ").strip()
                    punto_a_eliminar = None
                    try:
                        idx = int(punto_a_eliminar_str) - 1
                        if 0 <= idx < len(puntos_actuales):
                            punto_a_eliminar = puntos_actuales[idx]
                    except ValueError:
                        punto_a_eliminar = punto_a_eliminar_str
                    if punto_a_eliminar in puntos_actuales:
                        if len(puntos_actuales) > 2: 
                            puntos_actuales.remove(punto_a_eliminar)
                            print(f"'{punto_a_eliminar}' ha sido eliminado.")
                        else:
                            print("\nNo puedes eliminar este punto. Debes mantener al menos dos puntos en tu itinerario.")
                    else:
                        print("Punto no encontrado en tu itinerario.")
                elif opcion == '0':
                    print("Edición de itinerario finalizada.")
                    break
                else:
                    print("Opción inválida. Intente de nuevo.")
                print("Itinerario actual para este cliente:", ", ".join(puntos_actuales))
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número.")
    print("---------------------------")

def guardar_ruta_cliente(archivo, ruta_cliente):
    if not ruta_cliente:
        print("\nNo hay itinerarios para guardar.")
        return
    try:
        with open(archivo, "w", encoding="utf-8") as file:
            for idx, itinerario in enumerate(ruta_cliente):
                puntos_str = ", ".join(itinerario["puntos_visita"])
                file.write(f"Itinerario {idx+1}: {puntos_str}, Costo Total: {itinerario['costo_total']:.2f}, Distancia Total: {itinerario['distancia_total']:.2f}\n")
        print(f"Itinerarios guardados exitosamente en '{archivo}'.")
    except Exception as e:
        print(f"\nError al guardar los itinerarios: {e}")
    print("-------------------------------------------")

def cargar_rutas_cliente(archivo):
    rutas_cargadas = [] # Inicializa una lista vacía para almacenar las rutas
    try:
        with open(archivo, "r", encoding="utf-8") as file:
            for linea in file:
                linea = linea.strip()
                if linea:
                    try:
                        partes = linea.split(", Costo Total: ")
                        puntos_parte_bruta = partes[0].replace("Itinerario ", "")
                        if ": " in puntos_parte_bruta:
                            puntos_str_limpio = puntos_parte_bruta.split(": ", 1)[1].strip()
                        else:
                            print(f"Advertencia: Formato de línea inesperado en el archivo: {linea}. Saltando esta línea.")
                            continue
                        puntos_visita = [p.strip() for p in puntos_str_limpio.split(", ")]
                        if len(partes) > 1 and ", Distancia Total: " in partes[1]:
                            costo_distancia_parte = partes[1].split(", Distancia Total: ")
                            costo_total = float(costo_distancia_parte[0])
                            distancia_total = float(costo_distancia_parte[1])
                        else:
                            print(f"Advertencia: Formato de costo/distancia inesperado en la línea: {linea}. Usando 0.0.")
                            costo_total = 0.0
                            distancia_total = 0.0

                        rutas_cargadas.append({
                            "puntos_visita": puntos_visita,
                            "costo_total": costo_total,
                            "distancia_total": distancia_total
                        })
                    except Exception as parse_error:
                        print(f"Error al parsear línea '{linea}': {parse_error}. Saltando esta línea.")
        return rutas_cargadas # Siempre retorna la lista, vacía si no hay nada o hay errores.
    except FileNotFoundError:
        print(f"El archivo '{archivo}' no fue encontrado. Se iniciará con una lista vacía de itinerarios.")
        return [] # Retorna una lista vacía si el archivo no existe
    except Exception as e:
        print(f"Error general al cargar los itinerarios desde '{archivo}': {e}. Se iniciará con una lista vacía.")
        return [] 

def menu_turismo_cliente(nombre_cliente):
    archivo_conexiones = "rutas_conectadas.txt"
    archivo_zonas = "puntos_turisticos.txt"
    grafo_conexiones = cargar_grafo_conexiones(archivo_conexiones)
    cliente_archivo = f"rutas-{nombre_cliente.replace(' ', '_').lower()}.txt"
    ruta_cliente = cargar_rutas_cliente(cliente_archivo)
    while True:
        print(f"\n--- Menú Cliente ---")
        print("1. Mostrar mapa de distancias entre lugares turísticos")  # NUEVA OPCIÓN
        print("2. Mostrar mapa de lugares conectados")
        print("3. Consultar ruta óptima entre dos puntos")
        print("4. Explorar lugares por zona/ciudad")
        print("5. Seleccionar puntos a visitar")
        print("6. Lista de tus lugares turísticos seleccionados con costo total y distancia total")
        print("7. Actualizar o Eliminar selección de lugares turísticos")
        print("8. Volver al menú principal")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == '1':
            mostrar_matriz_distancias_cliente()
        elif opcion=='2':
            mostrar_mapa_lugares_conectados(grafo_conexiones)
        elif opcion == '3':
            consultar_ruta_optima(grafo_conexiones)
        elif opcion == '4':
            punto_padre = construir_arbol_desde_archivo(archivo_zonas)
            if punto_padre:
                menu_ciudades(punto_padre)
        elif opcion == '5':
            seleccionar_puntos_visita(grafo_conexiones,ruta_cliente)
            guardar_ruta_cliente(cliente_archivo,ruta_cliente)
        elif opcion == '6':
            listar_itinerario(ruta_cliente,grafo_conexiones)
            guardar_ruta_cliente(cliente_archivo,ruta_cliente)
        elif opcion == '7':
            actualizar_eliminar_seleccion(ruta_cliente,grafo_conexiones)
            guardar_ruta_cliente(cliente_archivo,ruta_cliente)
        elif opcion == '8':
            print("\nVolviendo al menú principal...")
            break

#inicio de sesión
def menu_inicio_sesion():
    print("\n--- Menú de Inicio de Sesión ---")
    print("1. Administrador")
    print("2. Cliente")
    print("3. Salir")

def menu_cliente():
    print("\n--- Menú Cliente ---")
    print("1. Iniciar sesión")
    print("2. Registrarse")
    print("3. Volver al menú principal")

def iniciar_sesion_admin():
    usuario = validar_vacio("Ingrese su usuario: ")
    clave = validar_vacio("Ingrese su contraseña: ")

    if usuario.strip() == USUARIO and clave.strip() == CLAVE:
        print("\nBienvenido, administrador.")
        menu_turismo_admin()
    else:
        print("Usuario o contraseña incorrectos. Intente nuevamente.")

def iniciar_sesion_cliente(usuarios):
    usuario = validar_vacio("Ingrese su usuario: ")
    clave = validar_vacio("Ingrese su contraseña: ")
    login_exitoso = False

    for u in usuarios:
        if u["usuario"] == usuario.strip() and u["clave"] == clave.strip():
            print(f"\nBienvenido, {u['nombres']}.")
            menu_turismo_cliente(f"{u['nombres']}") 
            login_exitoso = True
            break
    if not login_exitoso:
        print("Usuario o contraseña incorrectos. Intente nuevamente o regístrese.")

def menu_principal():
    archivo = "usuarios.txt"
    usuarios = cargar_datos(archivo)
    while True:
        print("\nSISTEMA DE RUTAS TURÍSTICAS")
        menu_inicio_sesion()
        opcion_uno = input("Seleccione una opción: ")
        if opcion_uno == '1':
            iniciar_sesion_admin()
        elif opcion_uno == '2':
            menu_cliente()
            opcion_dos = input("Seleccione una opción: ")
            if opcion_dos == '1':
                iniciar_sesion_cliente(usuarios)
            elif opcion_dos == '2':
                registrar_usuario(usuarios)
                guardar_datos(usuarios,archivo)
            elif opcion_dos == '3':
                print("\nVolviendo al menú principal...")
                continue
            else:
                print("Opción no válida. Intente nuevamente.")
        elif opcion_uno == '3':
            print("Saliendo del sistema...")
            break

menu_principal()