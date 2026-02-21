import sys
import os
from services.authService import validarUsuario
from interfaces.adminInterface import mostrarInterfazAdmin
from interfaces.clienteInterface import mostrarInterfazCliente



def Login():
    credenciales=input("Ingrese sus credenciales\n")
    contra=input("Ingrese su contraseña\n")
    rol=validarUsuario(credenciales,contra)

    match rol:
        case "ADMIN":
            mostrarInterfazAdmin()
            
        case "CLIENTE":
            mostrarInterfazCliente()