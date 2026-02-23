import sys
import os
from repositories.usuarioRepository import UsuarioRepository

def validarUsuario(credenciales, contra):
    usuarioRepo=UsuarioRepository()
    
    if len(credenciales)>4 and len(credenciales)<=10:
        # dui=int(credenciales)
        dui=credenciales
        pin=contra
        #Validar que el usuario exista en el repositorio
        for usuario in usuarioRepo.datos:
            if usuario["dui"]==dui and usuario["pin"]==pin:
                return usuario["rol"]
            
    elif len(credenciales)>0 and len(credenciales)<=4:
        username=credenciales
        pin=contra
        #Validar que el usuario exista en el repositorio
        for usuario in usuarioRepo.datos:
            if usuario["username"]==username and usuario["pin"]==pin:
                return usuario["rol"]
    
    
    
    
        
        
        
        