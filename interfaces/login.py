import os
from repositories.usuarioRepository import UsuarioRepository
from interfaces.adminInterface import mostrarInterfazAdmin
from interfaces.clienteInterface import mostrarInterfazCliente


titulo = "\n\033[1;36;40m === LOGIN === \033[0m\n"


def limpiar():
    os.system("cls" if os.name == "nt" else "clear")


def Login():

    repo = UsuarioRepository()

    intentos_vacios = 0
    intentos_invalidos = 0

    while True:

        limpiar()
        print(titulo)

        credenciales = input("Ingrese sus credenciales: ").strip()
        pin = input("Ingrese PIN: ").strip()

        # =========================
        # VALIDAR CAMPOS VACIOS
        # =========================
        if credenciales == "" and pin == "":
            intentos_vacios += 1
            print(f"\033[33mCampos vacíos ({intentos_vacios}/3)\033[0m")
            input("Enter...")

            if intentos_vacios >= 3:
                print("\033[31mDemasiados intentos vacíos. Saliendo...\033[0m")
                break

            continue

        # reinicia si escribe algo
        intentos_vacios = 0

        # =========================
        # VALIDAR CREDENCIALES
        # =========================
        usuario_logueado = repo.buscar_por_credenciales(credenciales, pin)

        if not usuario_logueado:
            intentos_invalidos += 1
            print(f"\033[31mCredenciales incorrectas ({intentos_invalidos}/3)\033[0m")
            input("Enter...")

            if intentos_invalidos >= 3:
                print("\033[31mDemasiados intentos fallidos. Acceso bloqueado.\033[0m")
                break

            continue

        # =========================
        # LOGIN EXITOSO
        # =========================
        intentos_invalidos = 0

        if usuario_logueado["rol"] == "ADMIN":
            mostrarInterfazAdmin()
        else:
            mostrarInterfazCliente(usuario_logueado)

        break