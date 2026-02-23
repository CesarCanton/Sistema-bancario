import sys
import os
from services.adminService import crear_cliente, listar_usuarios, crear_admin

titulo = "\n\033[1;36;40m === SISTEMA BANCARIO(ADMIN) === \033[0m\n"
def crearCliente():
       while True:
            os.system('cls')
            print(titulo)
            print("Creando cliente")
            try:
                
                nombres=input("Ingrese los nombres del cliente: ")
                if not nombres.strip():
                    print("El campo no pueden estar vacios. Intente nuevamente")
                    input("Presione Enter para continuar...")
                    continue

                apellidos=input("Ingrese los apellidos del cliente: ")
                if not apellidos.strip():
                    print("El campo no puede estar vacio. Intente nuevamente")
                    input("Presione Enter para continuar...")
                    continue
                
                
                dui=input("Ingrese el DUI del cliente: ")
                if not dui.strip() or len(dui) != 10 or not dui[-2]=="-":
                    print("Ingrese correctamente los datos. Intente nuevamente")
                    input("Presione Enter para continuar...")
                    continue
                
                pin=input("Ingrese el PIN del cliente: ")
                if not pin.strip() or len(pin) != 4:
                    print("Ingrese correctamente los datos. Intente nuevamente")
                    input("Presione Enter para continuar...")
                    continue
                
                rol="CLIENTE"
                crear_cliente(nombres,apellidos,dui,pin,rol)
                print("\033[32mCliente creado exitosamente.\033[0m")
                input("Presione Enter para continuar...")
                mostrarInterfazAdmin()
                break
            except Exception as e:
                print(f"\033[31mError al crear cliente: {e}\033[0m")
                input("Presione Enter para continuar...")

                
        
def listarUsuarios():
    pass
def crearAdmin():
    while True:
        os.system('cls')
        print(titulo)
        try:
            print("Creando admin")
            nombres=input("Ingrese los nombres del admin: ")
            if not nombres.strip():
                print("El campo no puede estar vacio. Intente nuevamente")
                input("Presione Enter para continuar...")
                continue
            
            apellidos=input("Ingrese los apellidos del admin: ")
            if not apellidos.strip():
                print("El campo no puede estar vacio. Intente nuevamente")
                input("Presione Enter para continuar...")
                continue
            
            dui=input("Ingrese el DUI del admin: ")
            if not dui.strip() or len(dui) != 10 or not dui[-2]=="-":
                print("Ingrese correctamente los datos. Intente nuevamente")
                input("Presione Enter para continuar...")
                continue
            
            pin=input("Ingrese el PIN del admin: ")
            if not pin.strip() or len(pin) != 4:
                print("Ingrese correctamente los datos. Intente nuevamente")
                input("Presione Enter para continuar...")
                continue
            
            rol="ADMIN"
            crear_admin(nombres,apellidos,dui,pin,rol)
            print("\033[32mAdmin creado exitosamente.\033[0m")
            input("Presione Enter para continuar...")
            mostrarInterfazAdmin()
            break
        except Exception as e:
            print(f"\033[31mError al crear admin: {e}\033[0m")
            input("Presione Enter para continuar...")
    
def listarCuentas():
    pass

def mostrarInterfazAdmin():
    os.system('cls')
    
    while True:
        print(titulo)
        print("Bienvenido al sistema bancario")
    
        opcion=int(input("Seleccione una opcion: \n1.Crear cliente\n2.Listar usuarios\n3.Crear admin\n4.Listar cuentas\n9.Salir\n"))

        match opcion:
            case 1: 
                crearCliente()
                break                
            case 2: 
                
                pass
            case 3: 
                crearAdmin()
                pass
            case 4: 
                pass
            case 5: 
                pass
            case 6: 
                pass
            case 9:
                print("\033[32mSaliendo del sistema...\033[0m")
                break
            case _:
                print("\033[31mOpcion no valida. Intente nuevamente.\033[0m")
                input("Presione Enter para continuar...")
    
    