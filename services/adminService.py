"""Funciones:

crear_cliente()

listar_usuarios()

Generación de username admin:

siglas + id_autoincremental"""

"""La forma de ingresar es a través de un username generado con las siglas de
su primer nombre y primer apellido, así como un id autoincremental, es decir
siglas + id_admin.
"""
from models.usuario import Usuario

def generar_username_admin(nombres, id):
    siglas = nombres[0].lower() 
    username = siglas + str(id)
    return username 

def crear_cliente(id, nombres, apellidos, dui, pin, rol):
    username = generar_username_admin(nombres, id)
    nuevo_usuario = Usuario(id, nombres, apellidos, dui, pin, rol, username)
    return nuevo_usuario

def listar_usuarios(usuarios):
    for usuario in usuarios:
        print(f"ID: {usuario.id}, Nombres: {usuario.nombres},"
              f"Apellidos: {usuario.apellidos}, DUI: {usuario.dui}, Rol: {usuario.rol}, Username: {usuario.username}")
        

