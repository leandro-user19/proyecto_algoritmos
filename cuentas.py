from io import open

import re

def validar_clave(mensaje):
    clave = input(mensaje)
    if not re.search(r"[A-Z],clave"):
        print("La clave debe contener al menos una letra mayúscula.")
        return validar_clave(mensaje)
    
    if not re.search(r"[0-9]", clave):
        print("La clave debe contener al menos un número.")
        return validar_clave(mensaje)
    
    return clave

def validar_vacio(mensaje):
    texto = input(mensaje)
    if texto.strip():
        return texto
    else:
        print("El campo no puede estar vacío.")
        return validar_vacio(mensaje)
    
def validar_edad(mensaje,tipo=int):
    try:
        edad = tipo(input(mensaje))
        if edad < 0:
            print("La edad no puede ser negativa.")
            return validar_edad(mensaje, tipo)
        return edad
    except ValueError:
        print("Por favor, ingrese un número válido.")
        return validar_edad(mensaje, tipo)



