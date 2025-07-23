from io import open

CLAVE = "1234"  #Clave de administrador
USUARIO = "admin"  #Usuario de administrador

# Validar usuario funcion
def usuario_validar(usuario):
    partes=usuario.split("@")
    if len(partes)!=2:
        return False
    
    usuario,dominio=partes

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
            return texto
        print("El campo no puede estar vacío. Por favor, ingrese un texto.")
        
def validar_edad(mensaje):
    while True:
        try:
            edad = int(input(mensaje))
            if edad >= 0:
                return edad
            else:
                print("La edad debe ser de 0 años o más.")
        except ValueError:
            print("Por favor, ingrese un número válido para la edad.")
 
def registrar_usuario(usuarios):
    print("\n--Registro de Usuario--")
    nombres = validar_vacio("Ingrese su nombre y apellido: ")
    edad = validar_edad("Ingrese su edad: ")
    usuario = validar_vacio("Ingrese su usuario: ")
    clave = validar_vacio("Ingrese su contraseña: ")

    if not usuario_validar(usuario):
        print("Error. El formato debe de ser nombre.apellido@dominio.com")
        return False
    
    if not contraseña_segura(clave):
        print("Error de contraseña")
        return False
    
    for u in usuarios:
        if u["usuario"] == usuario:
            print("El usuario ya existe. Por favor, elija otro.")
            return False
        
    usuarios.append({
        "nombres": nombres.strip(),
        "edad": edad,
        "usuario": usuario.strip(),
        "clave": clave.strip()
    })
    print("Cliente registrado exitosamente.")
    return True

def guardar_datos(usuarios,archivo):
    try:
        with open(archivo, "w", encoding="utf-8") as file:
            for usuario in usuarios:
                file.write(f"Usuario: {usuario['usuario']}\n")
                file.write(f"Contraseña: {usuario['clave']}\n")
                file.write(f"Nombres: {usuario['nombres']}\n")
                file.write(f"Edad: {usuario['edad']}\n")
                file.write("-" * 50 + "\n")
        print("Datos guardados exitosamente.")
    except Exception as e:
        print(f"Error al guardar los datos: {e}")

def cargar_datos(archivo):
    usuarios = []
    try:
        with open(archivo, "r", encoding="utf-8") as file:
            contenido = file.read().split("-" * 50 + "\n")
            for bloque in contenido:
                if bloque.strip():
                    lineas = bloque.strip().split("\n")
                    if len(lineas) >= 4:
                        usuario = lineas[0].split(": ")[1]
                        clave = lineas[1].split(": ")[1]
                        nombres = lineas[2].split(": ")[1]
                        edad = int(lineas[3].split(": ")[1])
                        usuarios.append({
                            "usuario": usuario,
                            "clave": clave,
                            "nombres": nombres,
                            "edad": edad
                        })
        return usuarios
    except FileNotFoundError:
        return []    

#funcion para agregar punto turistico
def agregar_datos_turisticos(puntos_turisticos):
    print("Ingrese los siguientes datos")
    ciudad = validar_vacio("Ciudad: ")
    lugar = validar_vacio("Lugar turístico: ")
    while True:
        try:
            distancia=int(input("Distancia (en km): "))
            costo=float(input("Costo de la entrada (en USD): $"))
            if distancia < 0 or costo < 0:
                print("La distancia y el costo deben ser valores positivos.")
            break
        except ValueError:
            print("\nERROR: Ingrese un número valido para la distancia y el costo.")

    punto={
        "ciudad":ciudad.strip(),
        "lugar":lugar.strip(),
        "distancia":distancia,
        "costo":costo
    }
    puntos_turisticos.append(punto)
    print("\nDatos del punto turistico agregada correctamente.")

def mostrar_puntos_turisticos(puntos_turisticos,mensaje):
    print(f"\n--- {mensaje} ---")
    for i, punto in enumerate(puntos_turisticos):
        print(f"{i + 1}. Ciudad: {punto['ciudad']} | Lugar: {punto['lugar']} | Distancia: {punto['distancia']} km | Costo: ${punto['costo']:.2f}")

def listar_puntos_turisticos(puntos_turisticos):
    if not puntos_turisticos:
        print("\nAun no hay datos agregados")
        return
    
    while True:
        print("\n--- Elija como desea ordenar los puntos turísticos ---")
        print("1. Alfabéticamente por ciudad (A-Z)")
        print("2. Alfabéticamente por ciudad (Z-A)")
        print("3. Por distancia (menor a mayor)")
        print("4. Por distancia (mayor a menor)")
        print("5. Por costo (menor a mayor)")
        print("6. Por costo (mayor a menor)")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            puntos_turisticos_ordenados = sorted(puntos_turisticos, key=lambda x: x['ciudad'].lower())
            mostrar_puntos_turisticos(puntos_turisticos_ordenados, "Puntos turísticos ordenados alfabéticamente por ciudad (A-Z)")
            break
        elif opcion == "2":
            puntos_turisticos_ordenados = sorted(puntos_turisticos, key=lambda x: x['ciudad'].lower(), reverse=True)
            mostrar_puntos_turisticos(puntos_turisticos_ordenados, "Puntos turísticos ordenados alfabéticamente por ciudad (Z-A)")
            break
        elif opcion == "3":
            puntos_turisticos_ordenados = sorted(puntos_turisticos, key=lambda x: x['distancia'])
            mostrar_puntos_turisticos(puntos_turisticos_ordenados, "Puntos turísticos ordenados por distancia (menor a mayor)")
            break
        elif opcion == "4":
            puntos_turisticos_ordenados = sorted(puntos_turisticos, key=lambda x: x['distancia'], reverse=True)
            mostrar_puntos_turisticos(puntos_turisticos_ordenados, "Puntos turísticos ordenados por distancia (mayor a menor)")
            break
        elif opcion == "5":
            puntos_turisticos_ordenados = sorted(puntos_turisticos, key=lambda x: x['costo'])
            mostrar_puntos_turisticos(puntos_turisticos_ordenados, "Puntos turísticos ordenados por costo (menor a mayor)")
            break
        elif opcion == "6":
            puntos_turisticos_ordenados = sorted(puntos_turisticos, key=lambda x: x['costo'], reverse=True)
            mostrar_puntos_turisticos(puntos_turisticos_ordenados, "Puntos turísticos ordenados por costo (mayor a menor)")
            break
        else:
            print("Opción no válida. Por favor, intente nuevamente.")
            continue
    
def consultar_punto_turistico(puntos_turisticos):
    if not puntos_turisticos:
        print("\nAun no hay datos agregados")
        return
    ciudad = validar_vacio("Ingrese la ciudad que desea consultar: ")
    for punto in puntos_turisticos:
        if punto["ciudad"].lower() == ciudad.lower():
            print(f"Ciudad: {punto['ciudad']} | Lugar: {punto['lugar']} | Distancia: {punto['distancia']} km | Costo: ${punto['costo']:.2f}")
            return
    print("No se encontraron puntos turísticos en esa ciudad.")

def actualizar_punto_turistico(puntos_turisticos):
    if not puntos_turisticos:
        print("\nAun no hay datos agregados")
        return
    print("\nPuntos turísticos disponibles:")
    for i, punto in enumerate(puntos_turisticos):
        print(f"{i + 1}. Ciudad: {punto['ciudad']} | Lugar: {punto['lugar']} | Distancia: {punto['distancia']} km | Costo: ${punto['costo']:.2f}")
    while True:
        try:
            indice_actualizar = int(input("Ingrese el número del punto turístico que desea actualizar: ")) - 1
            if 0 <= indice_actualizar.strip() < len(puntos_turisticos):
                ciudad = validar_vacio("Nueva ciudad: ")
                lugar = validar_vacio("Nuevo lugar turístico: ")
                while True:
                    try:
                        distancia = int(input("Nueva distancia (en km): "))
                        costo = float(input("Nuevo costo de la entrada (en USD): $"))
                        if distancia < 0 or costo < 0:
                            print("La distancia y el costo deben ser valores positivos.")
                        break
                    except ValueError:
                        print("\nERROR: Ingrese un número valido para la distancia y el costo.")
                puntos_turisticos[indice_actualizar] = {
                    "ciudad": ciudad.strip(),
                    "lugar": lugar.strip(),
                    "distancia": distancia.strip(),
                    "costo": costo.strip()
                }
                print(f"Punto turístico actualizado exitosamente.")
                return
            else:
                print("Número de índice inválido. Por favor, intente de nuevo.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número.")

def eliminar_punto_turistico(puntos_turisticos):
    if not puntos_turisticos:
        print("\nAún no hay datos agregados.")
        return

    print("\nPuntos turísticos disponibles:")
    for i, punto in enumerate(puntos_turisticos):
        print(f"{i + 1}. Ciudad: {punto['ciudad']} | Lugar: {punto['lugar']} | Distancia: {punto['distancia']} km | Costo: ${punto['costo']:.2f}")

    while True:
        try:
            indice_eliminar = int(input("Ingrese el número del punto turístico que desea eliminar: ")) - 1
            if 0 <= indice_eliminar.strip() < len(puntos_turisticos):
                punto_eliminado = puntos_turisticos.pop(indice_eliminar)
                print(f"Punto turístico '{punto_eliminado['lugar']}' de {punto_eliminado['ciudad']} eliminado exitosamente.")
                return
            else:
                print("Número de índice inválido. Por favor, intente de nuevo.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número.")

def guardar_puntos_turisticos(puntos_turisticos, archivo):
    try:
        with open(archivo, "w", encoding="utf-8") as file:
            for punto in puntos_turisticos:
                file.write(f"Ciudad: {punto['ciudad']}\n")
                file.write(f"Lugar: {punto['lugar']}\n")
                file.write(f"Distancia: {punto['distancia']} km\n")
                file.write(f"Costo: ${punto['costo']:.2f}\n")
                file.write("-" * 50 + "\n")
    except Exception as e:
        print(f"Error al guardar los puntos turísticos: {e}")

def cargar_puntos_turisticos(archivo):
    puntos_turisticos = []
    try:
        with open(archivo, "r", encoding="utf-8") as file:
            contenido = file.read().split("-" * 50 + "\n")
            for bloque in contenido:
                if bloque.strip():
                    lineas = bloque.strip().split("\n")
                    if len(lineas) >= 4:
                        ciudad = lineas[0].split(": ")[1]
                        lugar = lineas[1].split(": ")[1]
                        distancia = int(lineas[2].split(": ")[1].replace(" km", ""))
                        costo = float(lineas[3].split(": ")[1].replace("$", ""))
                        puntos_turisticos.append({
                            "ciudad": ciudad,
                            "lugar": lugar,
                            "distancia": distancia,
                            "costo": costo
                        })
        return puntos_turisticos
    except FileNotFoundError:
        return []
    
def menu_turismo_admin():
    archivo = "rutas.txt"
    puntos_turisticos = cargar_puntos_turisticos(archivo)
    while True:
        print("\n-----Puntos Turisticos-----")
        print("1. Agregar datos turísticos")
        print("2. Listar puntos turísticos")
        print("3. Consultar puntos turísticos")
        print("4. Actualizar puntos turísticos")
        print("5. Eliminar puntos turísticos")
        print("6. Volver al menú principal")
        opcion=input("Seleccione una opción: ")

        if opcion=="1":
            agregar_datos_turisticos(puntos_turisticos)
            guardar_puntos_turisticos(puntos_turisticos, archivo)
        elif opcion=="2":
            listar_puntos_turisticos(puntos_turisticos)
        elif opcion=="3":
            consultar_punto_turistico(puntos_turisticos)
        elif opcion=="4":
            actualizar_punto_turistico(puntos_turisticos)
            guardar_puntos_turisticos(puntos_turisticos, archivo)
        elif opcion=="5":
            eliminar_punto_turistico(puntos_turisticos)
            guardar_puntos_turisticos(puntos_turisticos, archivo)
        elif opcion=="6":
            print("\nVolviendo al menú principal...")
            break
        else:
            print("Opción no válida.")

def menu_turismo_cliente():
    print("¡Acceso al menú de cliente!")

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
            menu_turismo_cliente() 
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
