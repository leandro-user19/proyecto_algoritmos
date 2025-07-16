from io import open

def crear_archivo(archivo):
    try:    
        with open(archivo, "w", encoding="UTF-8")as f:
            f.write("Archivo.txt")
            print("Archivo creado correctamente. ")
    except Exception as e:
        print(f"Error al crear el archivo {e}")


