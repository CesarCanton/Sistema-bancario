from repositories.usuarioRepository import UsuarioRepository
from repositories.cuentaRepository import CuentaRepository
from models.usuario import Usuario

usuario_repo = UsuarioRepository()

def get_next_id():
    if not usuario_repo.datos:
        return 1
    return max(int(u["id"]) for u in usuario_repo.datos) + 1

def generar_username(nombres, apellidos):

    siglas = nombres.split()[0][0].lower() + apellidos.split()[0][0].lower()

    ids = []

    for u in usuario_repo.datos:
        username = u["username"]

        if username.startswith(siglas):
            try:
                ids.append(int(username[len(siglas):]))
            except:
                pass

    next_id = max(ids) + 1 if ids else 1

    return f"{siglas}{next_id}"

def crear_cliente(nombres, apellidos, dui, pin, rol="CLIENTE"):

    # Validación DUI duplicado
    if any(u["dui"] == dui for u in usuario_repo.datos):
        raise Exception("El DUI ya existe")

    if len(pin) != 4 or not pin.isdigit():
        raise Exception("PIN inválido")

    id_user = get_next_id()
    username = generar_username(nombres, apellidos)

    usuario = Usuario(
        id_user,
        nombres,
        apellidos,
        dui,
        pin,
        rol,
        username
    )

    usuario_repo.agregar(usuario.to_dict())

    return username

def crear_admin(nombres, apellidos, dui, pin, rol="ADMIN"):

    if len(pin) != 4 or not pin.isdigit():
        raise Exception("PIN inválido")

    id_user = get_next_id()
    username = generar_username(nombres, apellidos)

    admin = Usuario(
        id_user,
        nombres,
        apellidos,
        dui,
        pin,
        rol,
        username
    )

    usuario_repo.agregar(admin.to_dict())

    return username

def listar_usuarios():

    if not usuario_repo.datos:
        print("No hay usuarios")
        return

    for u in usuario_repo.datos:
        print(
            f"ID: {u['id']} | "
            f"{u['nombres']} {u['apellidos']} | "
            f"DUI: {u['dui']} | "
            f"Rol: {u['rol']} | "
            f"Username: {u['username']}"
        )

def cambiar_estado_cuenta(cuenta_id, nuevo_estado):

    cuentas_repo = CuentaRepository()

    cuenta = next((c for c in cuentas_repo.datos if c["id"] == str(cuenta_id)), None)

    if not cuenta:
        raise Exception("Cuenta no encontrada")

    cuenta["estado"] = nuevo_estado
    cuentas_repo.guardar_datos()

    print(f"Cuenta {cuenta_id} ahora está {nuevo_estado}")

def listaDeCuentas():

    cuentas_repo = CuentaRepository()

    if not cuentas_repo.datos:
        print("No hay cuentas")
        return

    for cuenta in cuentas_repo.datos:
        print(
            f"\033[1;36;40mId\033[0m {cuenta['id']} | "
            f"Tipo: {cuenta['tipo']} | "
            f"Propietario: {cuenta['propietarioId']} | "
            f"Estado: {cuenta['estado']} | "
            f"Saldo: {cuenta['saldo']}\n"
        )