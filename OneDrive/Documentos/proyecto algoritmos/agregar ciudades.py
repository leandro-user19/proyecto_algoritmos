from io import open

CLAVE = "1234"  #Clave de administrador
USUARIO = "ad.min@gmail.com"  #Usuario de administrador


# Validar correo funcion
def usuario_validar(correo):
    partes=correo.split("@")
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
    texto = input(mensaje)
    if texto.strip():
        return texto
    else:
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
    usuario = input("Ingrese su usuario: ")
    clave = input("Ingrese su contraseña: ")

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
        "nombres": nombres,
        "edad": edad,
        "usuario": usuario,
        "clave": clave
    })
    print("Cliente registrado exitosamente.")



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
        print("No se encontró el archivo de usuarios.")
        return []    



# Agregar las nuevas ciudades/puntos turísticos , distancias y costos.

#Almacenar ciudades/puntos turísticos , distancias y costos.
puntos_turisticos=[]

#funcion para agregar punto turistico
def agregar_datos_turisticos():
    print("Ingrese los siguientes datos ")
    ciudad=input("Ciudad: ")
    lugar=input("Punto turistico: ")
    try:
        distancia=int(input("Distancia (en km): "))
        costo=float(input("Costo de la entrada (en USD): $"))

        punto={    #diccionario  para almacenar de una manera estructurada
            "ciudad":ciudad,
            "lugar":lugar,
            "distancia":distancia,
            "costo":costo
        }
        puntos_turisticos.append(punto)
        print("Datos del punto turistico agregada correctamente\n")
    except ValueError:
        print("\nERROR: Ingrese un numero valido para la distancia y el costo.")

# funcion para mostrar el punto ingresado
def mostrar_puntos_turisticos():
    if not puntos_turisticos:
        print("Aun no hay datos agregados")
        return
    print("Lista de puntos Turisticos:")
    for i, punto in enumerate(puntos_turisticos, start=1):
        print(f"{i}Ciudad: {punto["ciudad"]} | Lugar: {punto["lugar"]} | Distancia: {punto["distancia"]} km | Costo: ${punto["costo"]:.2f} ")

def menu_turismo_admin():
    while True:
        print("\n-----Puntos Turisticos-----")
        print("1.Agregar datos turísticos")
        print("2.Mostrar puntos turisticos")
        print("3.Volver")
        opcion2=input("Seleccione una opción: ")

        if opcion2=="1":
            agregar_datos_turisticos()
        elif opcion2=="2":
            mostrar_puntos_turisticos()
        elif opcion2=="3":
            print("Volviendo al menú de registro...")
            break
        else:
            print("Opcion no valida")

def menu_turismo_cliente():
    pass

def menu_inicio_sesion():
    print("1. Administrador")
    print("2. Cliente")
    print("3. Salir")

def menu_cliente():
    print("1. Iniciar sesión")
    print("2. Registrarse")
    print("3. Volver al menú principal")


def iniciar_sesion_admin():
    usuario = input("Ingrese su usuario: ")
    clave = input("Ingrese su contraseña: ")

    if usuario == USUARIO and clave == CLAVE:
        print("\nBienvenido, administrador.")
        menu_turismo_admin()
    else:
        print("Usuario o contraseña incorrectos. Intente nuevamente.")

def iniciar_sesion_cliente(usuarios):
    usuario = input("Ingrese su usuario: ")
    clave = input("Ingrese su contraseña: ")
    for u in usuarios:
        if u["usuario"] == usuario and u["clave"] == clave:
            print(f"\nBienvenido, {u['nombres']}.")
            menu_turismo_cliente()
    print("Usuario o contraseña incorrectos. Intente nuevamente.")

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
                print("Volviendo al menú principal...")
                break
            else:
                print("Opción no válida. Intente nuevamente.")

menu_principal()
