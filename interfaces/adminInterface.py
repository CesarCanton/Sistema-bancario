import os
from services.adminService import (
    crear_cliente, listar_usuarios, crear_admin,
    listaDeCuentas, cambiar_estado_cuenta
)
from repositories.transaccionRepository import TransaccionRepository
from services.analiticaService import AnaliticaService

# Titulo del sistema
titulo = "\n\033[1;36;40m === SISTEMA BANCARIO(ADMIN) === \033[0m\n"


# =====================================================
# FUNCIONES DE ADMINISTRACIÓN
# =====================================================

def crearCliente():
    while True:
        os.system('cls')
        print(titulo)
        print("Creando cliente")
        try:
            nombres = input("Ingrese los nombres del cliente: ").strip()
            if not nombres:
                print("El campo no puede estar vacío")
                input("Presione Enter para continuar...")
                continue

            apellidos = input("Ingrese los apellidos del cliente: ").strip()
            if not apellidos:
                print("El campo no puede estar vacío")
                input("Presione Enter para continuar...")
                continue

            dui = input("Ingrese el DUI del cliente (formato 12345678-9): ").strip()
            if not dui or len(dui) != 10 or dui[-2] != "-":
                print("DUI inválido. Intente nuevamente")
                input("Presione Enter para continuar...")
                continue

            pin = input("Ingrese el PIN del cliente (4 dígitos): ").strip()
            if not pin or len(pin) != 4 or not pin.isdigit():
                print("PIN inválido. Intente nuevamente")
                input("Presione Enter para continuar...")
                continue

            rol = "CLIENTE"
            crear_cliente(nombres, apellidos, dui, pin, rol)
            print("\033[32mCliente creado exitosamente.\033[0m")
            input("Presione Enter para continuar...")
            return

        except Exception as e:
            print(f"\033[31mError al crear cliente: {e}\033[0m")
            input("Presione Enter para continuar...")


def crearAdmin():
    while True:
        os.system('cls')
        print(titulo)
        print("Creando administrador")
        try:
            nombres = input("Ingrese los nombres del admin: ").strip()
            if not nombres:
                print("El campo no puede estar vacío")
                input("Presione Enter para continuar...")
                continue

            apellidos = input("Ingrese los apellidos del admin: ").strip()
            if not apellidos:
                print("El campo no puede estar vacío")
                input("Presione Enter para continuar...")
                continue

            dui = input("Ingrese el DUI del admin (formato 12345678-9): ").strip()
            if not dui or len(dui) != 10 or dui[-2] != "-":
                print("DUI inválido. Intente nuevamente")
                input("Presione Enter para continuar...")
                continue

            pin = input("Ingrese el PIN del admin (4 dígitos): ").strip()
            if not pin or len(pin) != 4 or not pin.isdigit():
                print("PIN inválido. Intente nuevamente")
                input("Presione Enter para continuar...")
                continue

            rol = "ADMIN"
            crear_admin(nombres, apellidos, dui, pin, rol)
            print("\033[32mAdministrador creado exitosamente.\033[0m")
            input("Presione Enter para continuar...")
            return

        except Exception as e:
            print(f"\033[31mError al crear admin: {e}\033[0m")
            input("Presione Enter para continuar...")


def listarUsuarios():
    os.system('cls')
    print(titulo)
    print("=== LISTADO DE USUARIOS ===\n")
    try:
        usuarios = listar_usuarios()
        for u in usuarios:
            print(u)
    except Exception as e:
        print(f"Error: {e}")

    input("\nPresione Enter para continuar...")


def listarCuentas():
    os.system('cls')
    print(titulo)
    print("=== LISTADO DE CUENTAS ===\n")
    try:
        listaDeCuentas()
    except Exception as e:
        print(f"Error: {e}")
    input("\nPresione Enter para continuar...")


def cambiarEstadoCuenta():
    os.system('cls')
    print(titulo)
    print("=== CAMBIAR ESTADO DE CUENTA ===\n")
    try:
        listaDeCuentas()
        idCuenta = input("\nIngrese el ID de la cuenta: ").strip()

        print("\n1. ACTIVA")
        print("2. BLOQUEADA")
        opc = input("Seleccione estado: ").strip()
        estado = "ACTIVA" if opc == "1" else "BLOQUEADA" if opc == "2" else None

        if not estado:
            print("Opción inválida")
            input("Presione Enter para continuar...")
            return

        cambiar_estado_cuenta(idCuenta, estado)
        print("Estado actualizado correctamente")

    except Exception as e:
        print(f"Error: {e}")

    input("\nPresione Enter para continuar...")


# =====================================================
# MÓDULO DE ANALÍTICA
# =====================================================

def analitica():
    os.system('cls')
    print(titulo)
    print("=== ANÁLITICA DE CUENTAS ===\n")
    try:
        repo = TransaccionRepository()
        service = AnaliticaService(repo)
        resultado = service.ejecutar_modulo_anomalias()

        print("--- ANOMALÍAS Z-SCORE ---")
        for a in resultado["z_score"]:
            print(a)

        print("\n--- STRUCTURING ---")
        for a in resultado["structuring"]:
            print(a)

        print("\n--- ACTIVIDAD NOCTURNA ---")
        for a in resultado["actividad_nocturna"]:
            print(a)

    except Exception as e:
        print(f"Error al ejecutar analítica: {e}")

    input("\nPresione Enter para continuar...")


# =====================================================
# MENÚ PRINCIPAL ADMIN
# =====================================================

def mostrarInterfazAdmin():
    while True:
        os.system('cls')
        print(titulo)
        print("Bienvenido al sistema bancario (ADMIN)\n")
        print("1. Crear cliente")
        print("2. Listar usuarios")
        print("3. Crear admin")
        print("4. Listar cuentas")
        print("5. Analítica de cuentas")
        print("6. Cambiar estado de cuenta")
        print("9. Salir")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            crearCliente()
        elif opcion == "2":
            listarUsuarios()
        elif opcion == "3":
            crearAdmin()
        elif opcion == "4":
            listarCuentas()
        elif opcion == "5":
            analitica()
        elif opcion == "6":
            cambiarEstadoCuenta()
        elif opcion == "9":
            print("\033[32mSaliendo del sistema...\033[0m")
            break
        else:
            print("\033[31mOpción no válida. Intente nuevamente.\033[0m")
            input("Presione Enter para continuar...")