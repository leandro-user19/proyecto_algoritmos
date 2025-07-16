
#Apartado del cliente
usuarios = []
from io import open

def crear_archivo(archivo, usuarios):
    try:    
        with open(archivo, "a", encoding="UTF-8")as f:
            for i in usuarios:
                f.write(f"{i['Usuario']},  {i['Clave']}\n")
            print("Archivo creado correctamente. ")
    except Exception as e:
        print(f"Error al crear el archivo {e}")


def registrar_usuario(usuarios):
    print("\n REGISTRO ")
    usuario = input("Ingrese el usuario: ")
    contraseña = input("Ingrese su contraseña: ")
    usuarios.append({"Usuario" : usuario, "Clave" : contraseña})
    print("Usted se ha registrado correctamente. ")

def login_usuario(usuarios):
    if not usuarios:
        print("No existen usuarios registrados. ")
        return
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")

    for i in usuarios:
        if i ["Usuario"] == usuario and i["Clave"] == contraseña:
            print("Bienvenido al sistema. ")
            return
    print("Usuario o contraseña incorrectos...\n")

def cargar_datos(archivo):
    try:
        with open(archivo, "r", encoding = "utf-8") as archivo_texto:
            for linea in archivo_texto:
                linea = linea.strip() #Elimina saltos de linea
                if linea: #La linea no esta vacia
                    usuario, contraseña = linea.split(",")
                    usuarios.append({"Usuario": usuario.strip(), "Clave": contraseña.strip()})
        return usuarios
    except FileNotFoundError:
        print("El archivo no existe")
        return[]

def menu():
    print("\n")
    print("/"*40)
    print("Sistema de TURISMO")
    print("/"*40)
    print("1. Registrar usuario")
    print("2. Iniciar sesion")
    print("3. Salir")

    
def main():
    archivo = "usuarios.txt"
    lista_usuarios = cargar_datos(archivo)
    
    while True:
        menu()
        try:
            opcion = int(input("Ingrese una de las opciones: "))
            if opcion == 1:
                registrar_usuario(lista_usuarios)
                crear_archivo(archivo, lista_usuarios)
            elif opcion == 2:
                login_usuario(lista_usuarios)
            elif opcion == 3:
                print("saliendo del sistema. ")
                break
            else:
                print("Opcion no valida...")
        except ValueError:
            print("Digite solo numeros.")

main()







