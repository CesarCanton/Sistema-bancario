from repositories.usuarioRepository import UsuarioRepository
from models.usuario import Usuario

def generar_username_admin(nombres, apellidos, id):
    siglas = nombres[0].lower() + apellidos[0].lower()
    username = siglas + str(id)
    return username 

def crear_cliente(nombres, apellidos, dui, pin, rol):
    repo=UsuarioRepository()
    id=len(repo.datos)+1
    username=" "#Ya que es cliente, no se genera un Username, solo los administradores pueden tener ese privilegio
    usuarioNuevo= Usuario(id,nombres,apellidos,dui,pin,rol,username)
    repo.agregar(usuarioNuevo)
    

def crear_admin(nombres, apellidos, dui, pin, rol):
    repo=UsuarioRepository()
    id=len(repo.datos)+1
    
    username=generar_username_admin(nombres, apellidos, id)   
    nuevoAdmin= Usuario(id,nombres,apellidos,dui,pin,rol,username)
    repo.agregar(nuevoAdmin) 
    
    
    

def listar_usuarios(usuarios):
    for usuario in usuarios:
        print(f"ID: {usuario.id}, Nombres: {usuario.nombres},"
              f"Apellidos: {usuario.apellidos}, DUI: {usuario.dui}, Rol: {usuario.rol}, Username: {usuario.username}")
        

