from io import open
import heapq
from collections import deque

CLAVE = "1234"  #Clave de administrador
USUARIO = "admin"  #Usuario de administrador

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

            # Verificar si la ruta ya existe en alguna dirección
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

            # Agrega la ruta de origen a destino
            ruta_ida = {
                "origen": origen['lugar'],
                "destino": destino['lugar'],
                "distancia": distancia,
                "costo": costo
            }
            rutas_conectadas.append(ruta_ida)
            print(f"\nConexión creada: {origen['lugar']} <-> {destino['lugar']}")

            # Agrega la ruta de destino a origen (bidireccionalidad)
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

        # Crear una lista para almacenar solo las rutas "ida"
        rutas_solo_ida = []
        rutas_ya_vistas = set() # Usamos un conjunto para almacenar las claves de las rutas ya vistas

        for ruta in rutas_conectadas:
            # Creamos una clave única para identificar el par bidireccional
            # Aseguramos que "Origen-Destino" y "Destino-Origen" generen la misma clave
            key = tuple(sorted((ruta['origen'], ruta['destino'])))

            # Si esta clave no ha sido vista, la agregamos a rutas_solo_ida
            if key not in rutas_ya_vistas:
                rutas_solo_ida.append(ruta)
                rutas_ya_vistas.add(key)

        if not rutas_solo_ida:
            print("No hay rutas únicas para mostrar.")
            return

        rutas_conectadas_ordenadas = list(rutas_solo_ida) # Ahora ordenamos solo las rutas "ida"

        if opcion == "1":
            rutas_conectadas_ordenadas.sort(key=lambda x: x['distancia'])
        elif opcion == "2":
            rutas_conectadas_ordenadas.sort(key=lambda x: x['costo'])
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

                    # Actualizar rutas conectadas si la ciudad o lugar cambiaron
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
        # Mostrar solo una de las rutas bidireccionales
        rutas_unicas_mostradas = []
        indices_originales = []
        for i, ruta in enumerate(rutas_conectadas):
            # Crea una clave única para identificar el par bidireccional
            # Asegura que "Origen-Destino" y "Destino-Origen" generen la misma clave
            key = tuple(sorted((ruta['origen'], ruta['destino'])))
            
            # Solo si esta clave no ha sido mostrada, la agregamos
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
                    # Obtenemos la ruta seleccionada de las rutas únicas mostradas
                    ruta_seleccionada_unica = rutas_unicas_mostradas[seleccion_unica]
                    
                    nueva_distancia = validar_numero("Nueva Distancia: ", float)
                    nuevo_costo = validar_numero("Nuevo Costo: ", float)

                    # Actualizar ambas rutas (ida y vuelta) que corresponden a la seleccionada
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

                    # Eliminar rutas conectadas que contengan el lugar turístico eliminado
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
    """
    Carga un grafo de conexiones desde un archivo.
    El archivo debe contener líneas con el formato: origen,destino,distancia,costo
    """
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

def cargar_grafo_zonas(archivo):
    """
    Carga un grafo de zonas desde un archivo.
    El archivo debe contener líneas con el formato: zona,lugar
    Si una zona se repite en el archivo, los lugares se agruparán bajo esa zona.
    """
    grafo_zonas = {}
    try:
        with open(archivo, "r", encoding="utf-8") as file:
            for linea in file:
                linea = linea.strip()
                if not linea:  # Salta líneas vacías
                    continue
                partes = linea.split(",")
                if len(partes) < 2: # Asegura que haya al menos una zona y un lugar
                    print(f"Advertencia: Línea ignorada por formato incorrecto: '{linea}'")
                    continue

                zona = partes[0].strip() # Limpia espacios alrededor del nombre de la ciudad
                lugar = partes[1].strip() # Limpia espacios alrededor del nombre del lugar

                if zona not in grafo_zonas:
                    grafo_zonas[zona] = [] # Si la ciudad no existe, crea una nueva lista para sus lugares
                grafo_zonas[zona].append(lugar) # Agrega el lugar a la lista de la ciudad
        return grafo_zonas
    except FileNotFoundError:
        print(f"El archivo '{archivo}' no fue encontrado. Se retornará un grafo vacío.")
        return {}
    except Exception as e:
        print(f"Error al cargar el grafo de zonas: {e}. Se retornará un grafo vacío.")
        return {}

def mostrar_mapa_lugares_conectados(grafo):
    """
    Muestra un mapa de los lugares turísticos conectados, mostrando cada conexión una sola vez.
    """
    if not grafo:
        print("No hay datos de rutas cargados.")
        return

    print("\n--- Mapa de Lugares Turísticos Conectados ---")
    
    # Usamos un conjunto para almacenar las conexiones ya mostradas para evitar duplicados.
    # Almacenaremos tuplas ordenadas de (origen, destino) para representar cada conexión única.
    conexiones_mostradas = set()

    for origen, conexiones in grafo.items():
        for conexion in conexiones:
            destino = conexion['destino']
            distancia = conexion['distancia']
            costo = conexion['costo']

            # Crea una clave única para identificar el par bidireccional.
            # Asegura que ("origen", "destino") y ("destino", "origen") generen la misma clave.
            key = tuple(sorted((origen, destino)))

            # Si esta conexión no ha sido mostrada, la imprimimos y la agregamos al conjunto.
            if key not in conexiones_mostradas:
                print(f"{origen} <-> {destino} (Distancia: {distancia:.2f} km, Costos: ${costo:.2f})")
                conexiones_mostradas.add(key)
    print("-----------------------------")

def dijkstra(grafo, inicio, fin):
    """
    Implementación del algoritmo de Dijkstra para encontrar la ruta de menor costo.
    Retorna la ruta, el costo total y la distancia total.
    """
    if inicio not in grafo or fin not in grafo:
        return None, float('inf'), float('inf') # Retornar ruta nula, costo infinito y distancia infinita

    # distancias ahora almacena (costo_total, distancia_total)
    distancias = {vertice: (float('inf'), float('inf')) for vertice in grafo}
    distancias[inicio] = (0, 0) # (costo, distancia) inicial
    prioridades = [(0, 0, inicio)] # (costo, distancia, vertice)
    caminos = {vertice: [] for vertice in grafo}
    caminos[inicio] = [inicio]

    while prioridades:
        costo_actual, distancia_actual, vertice_actual = heapq.heappop(prioridades)

        # Usamos solo el costo para la condición de continuación, ya que Dijkstra es por menor costo
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

            # Si encontramos una ruta de menor costo
            if nuevo_costo < distancias[vecino][0]:
                distancias[vecino] = (nuevo_costo, nueva_distancia)
                caminos[vecino] = caminos[vertice_actual] + [vecino]
                heapq.heappush(prioridades, (nuevo_costo, nueva_distancia, vecino))
            # Si el costo es el mismo, pero la distancia es menor (criterio secundario, opcional)
            elif nuevo_costo == distancias[vecino][0] and nueva_distancia < distancias[vecino][1]:
                distancias[vecino] = (nuevo_costo, nueva_distancia)
                caminos[vecino] = caminos[vertice_actual] + [vecino]
                heapq.heappush(prioridades, (nuevo_costo, nueva_distancia, vecino))

    return None, float('inf'), float('inf') # No se encontró un camino

def consultar_ruta_optima(grafo):
    """
    Permite al usuario consultar la ruta óptima y su costo entre dos puntos.
    """
    if not grafo:
        print("No hay datos de rutas cargados para consultar.")
        return

    print("\n--- Consultar Ruta Óptima ---")
    puntos_disponibles = sorted(list(grafo.keys()))
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

def explorar_lugares_por_zona(grafo_zonas):
    """
    Permite al usuario explorar lugares turísticos organizados por zonas/ciudades.
    """
    if not grafo_zonas:
        print("No hay datos de zonas cargados para explorar.")
        return

    print("\n--- Explorar Lugares Turísticos por Ciudades ---")
    zonas_disponibles = sorted(list(grafo_zonas.keys()))

    if not zonas_disponibles:
        print("No hay ciudades disponibles para explorar.")
        return

    for i, zona in enumerate(zonas_disponibles):
        print(f"{i + 1}. {zona}")

    while True:
        try:
            opcion_zona = input("Seleccione el número de una zona para explorar (o '0' para volver): ").strip()
            if opcion_zona == '0':
                break
            
            indice_zona = int(opcion_zona) - 1
            if 0 <= indice_zona < len(zonas_disponibles):
                zona_seleccionada = zonas_disponibles[indice_zona]
                lugares = grafo_zonas.get(zona_seleccionada, [])
                print(f"--- Lugares Turísticos en {zona_seleccionada} ---")
                if lugares:
                    for lugar in sorted(lugares):
                        print(f"- {lugar}")
                else:
                    print("No hay lugares listados para esta ciudad.")
                print("------------------------------------")
            else:
                print("Opción inválida. Intente de nuevo.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número.")
    print("--------------------------------")

def seleccionar_puntos_visita(grafo, ruta_cliente_actual):
    """
    Permite al usuario seleccionar ciudades/puntos turísticos a visitar.
    """
    print("\n--- Seleccionar Lugares Turísticos a Visitar para tu Itinerario ---")
    puntos_disponibles = sorted(list(grafo.keys()))

    if not puntos_disponibles:
        print("No hay lugares turísticos disponibles en el mapa para seleccionar.")
        return ruta_cliente_actual # Retorna la lista sin cambios

    print("Lugares Turísticos disponibles:")
    for i, punto in enumerate(puntos_disponibles):
        print(f"{i+1}. {punto}")

    print("\nIngrese los lugares que desea visitar (ingrese 'fin' para terminar).")
    print("Mínimo dos lugares.")

    nueva_ruta_cliente = ruta_cliente_actual[:] # Copia para no modificar la original directamente

    while True:
        punto_str = input("Ingrese un punto turístico: ").strip()
        if punto_str.lower() == 'fin':
            if len(nueva_ruta_cliente) < 2:
                print("Debe seleccionar al menos dos puntos turísticos.")
            else:
                break
        
        # Permitir seleccionar por número o por nombre
        punto_seleccionado = None
        try:
            idx = int(punto_str) - 1
            if 0 <= idx < len(puntos_disponibles):
                punto_seleccionado = puntos_disponibles[idx]
        except ValueError:
            if punto_str in puntos_disponibles:
                punto_seleccionado = punto_str

        if punto_seleccionado:
            if punto_seleccionado not in nueva_ruta_cliente:
                nueva_ruta_cliente.append(punto_seleccionado)
                print(f"'{punto_seleccionado}' añadido. Itinerario actual: {', '.join(nueva_ruta_cliente)}")
            else:
                print(f"'{punto_seleccionado}' ya está en tu itinerario.")
        else:
            print(f"'{punto_str}' no es un punto válido. Por favor, elija de la lista.")

    print("\nSelección de puntos finalizada.")
    print("-------------------------------------------------------------------")
    return nueva_ruta_cliente

def bubble_sort(arr):
    """Implementa el algoritmo de ordenamiento de burbuja."""
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def listar_itinerario_y_costo(ruta_cliente, grafo):
    """
    Lista las ciudades/puntos turísticos seleccionados, los ordena y calcula el costo total.
    """
    if not ruta_cliente:
        print("\nSu itinerario está vacío. Por favor, seleccione puntos primero.")
        return

    print("\n--- Tu Itinerario Seleccionado ---")

    # Ordenar las ciudades/puntos (usaremos Bubble Sort por simplicidad, puedes cambiarlo)
    itinerario_ordenado = bubble_sort(ruta_cliente[:]) # Copia para no modificar la original

    costo_total_itinerario = 0.0
    distancia_total_itinerario = 0.0
    ruta_detallada_con_costos = []

    print("\nItinerario (orden alfabético):")
    for i, punto in enumerate(itinerario_ordenado):
        print(f"{i+1}. {punto}")

    # Calcular el costo total si hay al menos dos puntos para formar una ruta
    if len(itinerario_ordenado) >= 2:
        print("\nCalculando costo de ruta sugerida:")
        for i in range(len(itinerario_ordenado) - 1):
            origen = itinerario_ordenado[i]
            destino = itinerario_ordenado[i+1]
            ruta, costo_tramo, distancia_tramo = dijkstra(grafo, origen, destino)

            if ruta:
                costo_total_itinerario += costo_tramo
                distancia_total_itinerario += distancia_tramo
                ruta_detallada_con_costos.append(f"  {origen} -> {destino} (Costo: ${costo_tramo:.2f}) (Distancia: {distancia_tramo:.2f} km)")
                # print(f"  Ruta {origen} -> {destino}: {' -> '.join(ruta)} (Costo: ${costo_tramo:.2f})")
            else:
                print(f"  Advertencia: No se encontró ruta directa entre {origen} y {destino}.")
                # Podrías añadir un costo penalidad o avisar al usuario
        
        print("\nResumen de costos por tramo:")
        for tramo in ruta_detallada_con_costos:
            print(tramo)

        print(f"\nCosto total estimado del itinerario: ${costo_total_itinerario:.2f} (Distancia total: {distancia_total_itinerario:.2f} km)")
    elif len(itinerario_ordenado) == 1:
        print("\nSolo hay un punto en el itinerario. Para calcular un costo, necesitas al menos dos puntos para una ruta.")
    
    print("----------------------------------")
    return costo_total_itinerario # Retornar el costo para guardarlo

def actualizar_eliminar_seleccion(ruta_cliente, grafo):
    """
    Permite al usuario añadir o eliminar puntos del itinerario actual.
    """
    if not ruta_cliente:
        print("\nSu itinerario está vacío. No hay nada que actualizar.")
        return []

    print("\n--- Actualizar Itinerario ---")
    print("Itinerario actual:", ", ".join(ruta_cliente))

    while True:
        print("\nOpciones de actualización:")
        print("1. Añadir un punto")
        print("2. Eliminar un punto")
        print("0. Terminar actualización")
        
        opcion = input("Ingrese su opción: ").strip()

        if opcion == '1':
            puntos_disponibles = sorted(list(grafo.keys()))
            print("\nLugares turísticos disponibles para añadir:")
            for i, punto in enumerate(puntos_disponibles):
                if punto not in ruta_cliente:
                    print(f"{i+1}. {punto}")
            
            punto_a_anadir = input("Ingrese el nombre o número del punto a añadir: ").strip()
            
            punto_validado = None
            try:
                idx = int(punto_a_anadir) - 1
                if 0 <= idx < len(puntos_disponibles):
                    punto_validado = puntos_disponibles[idx]
            except ValueError:
                if punto_a_anadir in puntos_disponibles:
                    punto_validado = punto_a_anadir

            if punto_validado:
                if punto_validado not in ruta_cliente:
                    ruta_cliente.append(punto_validado)
                    print(f"'{punto_validado}' ha sido añadido.")
                else:
                    print(f"'{punto_validado}' ya está en el itinerario.")
            else:
                print("Punto no válido o no disponible.")
        
        elif opcion == '2':
            if not ruta_cliente:
                print("El itinerario está vacío para eliminar.")
                continue

            print("\nLugares turísticos en su itinerario para eliminar:")
            for i, punto in enumerate(ruta_cliente):
                print(f"{i+1}. {punto}")

            punto_a_eliminar_str = input("Ingrese el nombre o número del punto a eliminar: ").strip()
            
            punto_a_eliminar = None
            try:
                idx = int(punto_a_eliminar_str) - 1
                if 0 <= idx < len(ruta_cliente):
                    punto_a_eliminar = ruta_cliente[idx]
            except ValueError:
                punto_a_eliminar = punto_a_eliminar_str

            if punto_a_eliminar in ruta_cliente:
                if len(ruta_cliente) > 2: # Mantener el requisito de mínimo 2 puntos
                    ruta_cliente.remove(punto_a_eliminar)
                    print(f"'{punto_a_eliminar}' ha sido eliminado.")
                else:
                    print("No puedes eliminar este punto. Debes mantener al menos dos puntos en tu itinerario.")
            else:
                print("Punto no encontrado en tu itinerario.")

        elif opcion == '0':
            print("Actualización de itinerario finalizada.")
            break
        else:
            print("Opción inválida. Intente de nuevo.")
        
        print("Itinerario actual:", ", ".join(ruta_cliente))
    
    print("---------------------------\n")
    return ruta_cliente

def guardar_ruta_cliente(nombre_cliente, ruta_cliente, costo_total):
    """
    Guarda la selección de ciudades/puntos turísticos en un archivo.
    """
    if not ruta_cliente:
        print("\nNo hay itinerario para guardar.")
        return

    nombre_archivo = f"rutas-{nombre_cliente.replace(' ', '_').lower()}.txt"
    try:
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"Itinerario de: {nombre_cliente}\n")
            file.write("--------------------------------\n")
            file.write("Puntos seleccionados:\n")
            for i, punto in enumerate(ruta_cliente):
                file.write(f"{i+1}. {punto}\n")
            file.write(f"\nCosto total estimado del itinerario: ${costo_total:.2f}\n")
            # Podrías añadir la ruta detallada si lo deseas:
            # for i in range(len(ruta_cliente) - 1):
            #     origen = ruta_cliente[i]
            #     destino = ruta_cliente[i+1]
            #     ruta, costo_tramo = dijkstra(main_grafo, origen, destino) # Necesitas el grafo principal aquí
            #     if ruta:
            #         file.write(f"Ruta {origen} -> {destino}: {' -> '.join(ruta)} (Costo: ${costo_tramo:.2f})\n")
        print(f"Itinerario guardado exitosamente en '{nombre_archivo}'.")
    except Exception as e:
        print(f"\nError al guardar el itinerario: {e}")
    print("-------------------------------------------")

def cargar_rutas_cliente(archivo):
    """
    Carga las rutas guardadas de un cliente desde un archivo.
    Formato del archivo: nombre_cliente,ruta1,ruta2,...
    """
    rutas = []
    try:
        with open(archivo, "r", encoding="utf-8") as file:
            for linea in file:
                linea = linea.strip()
                if linea:
                    partes = linea.split(",")
                    nombre_cliente = partes[0].strip()
                    ruta = [p.strip() for p in partes[1:]]
                    rutas.append({"nombre": nombre_cliente, "ruta": ruta})
        return rutas
    except FileNotFoundError:
        print(f"El archivo '{archivo}' no fue encontrado. Se retornará una lista vacía de rutas.")
        return []
    except Exception as e:
        print(f"Error al cargar las rutas desde '{archivo}': {e}. Se retornará una lista vacía.")
        return []
    
def menu_turismo_cliente(nombre_cliente):
    archivo_conexiones = "rutas_conectadas.txt"
    archivo_zonas = "puntos_turisticos.txt"
    grafo_conexiones = cargar_grafo_conexiones(archivo_conexiones)
    grafo_zonas = cargar_grafo_zonas(archivo_zonas)
    ruta_cliente_actual = []

    while True:
        print(f"\n--- Menú Cliente ---")
        print("1. Mostrar mapa de lugares conectados")
        print("2. Consultar ruta óptima entre dos puntos")
        print("3. Explorar lugares por zona/ciudad")
        print("4. Seleccionar puntos a visitar")
        print("5. Lista de tus lugares turísticos seleccionados con costo total y distancia total")
        print("6. Actualizar o Eliminar selección de lugares turísticos")
        print("7. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == '1':
            mostrar_mapa_lugares_conectados(grafo_conexiones)
        elif opcion == '2':
            consultar_ruta_optima(grafo_conexiones)
        elif opcion == '3':
            explorar_lugares_por_zona(grafo_zonas)
        elif opcion == '4':
            ruta_cliente_actual = seleccionar_puntos_visita(grafo_conexiones, ruta_cliente_actual)

        elif opcion == '5':
            costo_total = listar_itinerario_y_costo(ruta_cliente_actual, grafo_conexiones)
            if costo_total is not None:
                guardar_ruta_cliente(nombre_cliente, ruta_cliente_actual, costo_total) # Guardar automáticamente
        elif opcion == '6':
            ruta_cliente_actual = actualizar_eliminar_seleccion(ruta_cliente_actual, grafo_conexiones)
            
        elif opcion == '7':
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