from io import open

# Validar correo funcion
def usuario_validar(correo):
    partes=correo.split("@")
    if len(partes)!=2:
        return False
    
    usuario, dominio =partes

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
    if( len(contraseña)>=6 and
       any(c.isupper()for c in contraseña) and
       any(c.islower() for c in contraseña) and
       any(c.isdigit()for c in contraseña)):
        return True
    return False

# Funcion inicio de sesion
def inicio_sesion():
    print("\nIniciar Sesion--")
    usuario=input("Usuario: ")
    contraseña=input("Constraseña: ")
    
    #Validacion del correo y contraseña antes de continuar
    if not usuario_validar(usuario):
        print("Error. El formato debe de ser nombre.apellido@dominio.com")
        return False
    
    if not contraseña_segura(contraseña):
        print("Error de contraseña")
        return False
    
    try:
        with open ("Usuarios.txt", "r", encoding="utf-8") as archivo:
            contenido=archivo.read().split("-"*50)
            for bloque in contenido:
                if f"Usuario: {usuario}" in bloque and f"Contraseña: {contraseña}" in bloque:
                    print("Autentificacion exitosa")
                    return True
                print("Usuario o contraseña incorrectos")
                return False
    except FileNotFoundError:
        print("No hay usuarios registrados")
        return False


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
        costo=float(input("Costo de la entrada (en USD) : $"))

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

def menu_turismo():
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

def menu_principal():
    while True:
        print("\nSISTEMA DE RUTAS TURÍSTICAS")
        print("1.Iniciar sesión")
        print("2.Salir")
        opcion=input("Seleccione una opción: ")

        if opcion=="1":
            if inicio_sesion():
                menu_turismo()

        elif opcion=="2":
            print("Saliendo del sistema...")
            break

        else:
            print("Opcion no valida")

menu_principal()
