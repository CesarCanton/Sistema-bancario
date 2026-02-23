import sys
import os
from services.authService import validarUsuario
from interfaces.adminInterface import mostrarInterfazAdmin
from interfaces.clienteInterface import mostrarInterfazCliente


titulo = "\n\033[1;36;40m === LOGIN === \033[0m\n"
def Login():
    
    while True:
        os.system('cls')
        print(titulo)
        credenciales=input("Ingrese sus credenciales\n")
        contra=input("Ingrese su contraseña\n")
        rol=validarUsuario(credenciales,contra)

        match rol:
            case "ADMIN":
                mostrarInterfazAdmin()
                break
            case "CLIENTE":
                mostrarInterfazCliente()
                break
            case _:
                print("\033[31mCredenciales incorrectas. Intente nuevamente.\033[0m")
                input("Presione Enter para continuar...")
                if __name__ == "__main__":    Login()
        