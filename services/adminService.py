from repositories.usuarioRepository import UsuarioRepository
from repositories.cuentaRepository import CuentaRepository
from repositories.transaccionRepository import TransaccionRepository
from services.analiticaService import AnaliticaService
import numpy as np
from models.usuario import Usuario
from analytics.numpyAnalisis import constructor_matrices, estadisticas_admin

usuario_repo = UsuarioRepository()

def get_next_id():
    if not usuario_repo.datos:
        return 1
    return max(int(u["id"]) for u in usuario_repo.datos) + 1

def generar_username_admin(nombres, apellidos, id):
    siglas = nombres[0].lower() + apellidos[0].lower()
    username = siglas + str(id)
    return username 

def crear_admin(nombres, apellidos, dui, pin, rol="ADMIN"):

    if len(pin) != 4 or not pin.isdigit():
        raise Exception("PIN inválido")

    id_user = get_next_id()
    username = generar_username_admin(nombres, apellidos,id_user)

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


def crear_cliente(nombres, apellidos, dui, pin, rol="CLIENTE"):

    # Validación DUI duplicado
    if any(u["dui"] == dui for u in usuario_repo.datos):
        raise Exception("El DUI ya existe")

    if len(pin) != 4 or not pin.isdigit():
        raise Exception("PIN inválido")

    id_user = get_next_id()
    username = " "

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
    
def listar_usuarios(usuarios):
    for usuario in usuarios:
        print(f"ID: {usuario.id}, Nombres: {usuario.nombres},"
              f"Apellidos: {usuario.apellidos}, DUI: {usuario.dui}, Rol: {usuario.rol}, Username: {usuario.username}")

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

def listaDeCuentas():
    cuentasRepo=CuentaRepository()
    for cuenta in cuentasRepo.datos:
        print(f"\033[1;36;40mId\033[0m {cuenta["id"]}. "
              f"Tipo de cuenta: {cuenta["tipo"]}. "
              f"Id del propietario: {cuenta["propietarioId"]}. "
              f"Estado de cuenta: {cuenta["estado"]}. "
              f"Saldo: {cuenta["saldo"]}\n")
        
def cambiar_estado_cuenta(cuenta_id, nuevo_estado):

    cuentas_repo = CuentaRepository()

    cuenta = next((c for c in cuentas_repo.datos if c["id"] == str(cuenta_id)), None)

    if not cuenta:
        raise Exception("Cuenta no encontrada")

    cuenta["estado"] = nuevo_estado
    cuentas_repo.guardar_datos()

    print(f"Cuenta {cuenta_id} ahora está {nuevo_estado}")

def ejecutar_analitica():

    transacciones = TransaccionRepository()
    analitica_service = AnaliticaService(transacciones)

    X_dep, X_gas, cuentas, fechas = constructor_matrices(transacciones.datos)
    stats_admin = estadisticas_admin(X_dep, X_gas, cuentas, fechas)

    print("\n\033[1;36;40m=== Estadísticas Administrativas ===\033[0m")
    print(f"Suma total de todos los depósitos: {np.sum(stats_admin['total_diario_depositos'])}")
    print(f"Total diario de gastos: {np.sum(stats_admin['total_diario_gastos'])}")
    print(f"Total diario neto: {np.sum(stats_admin['total_diario_neto'])}")

    # Top 10 depósitos
    print("\n=== TOP 10 DEPOSITOS ===")
    for i, cuenta in enumerate(stats_admin['top_10_depositos'], start=1):
        print(f"{i}. Cuenta: {cuenta['cuenta']} Total:{cuenta['total_depositos']:.2f}")

    # Top 10 gastos
    print("\n=== TOP 10 GASTOS ===")
    for i, cuenta in enumerate(stats_admin['top_10_gastos'], start=1):
        print(f"{i}. Cuenta: {cuenta['cuenta']} Total:{cuenta['total_gastos']:.2f}")

    # Top 5 días con mayor actividad
    print("\n=== TOP 5 DIAS CON MAYOR ACTIVIDAD ===")
    for i, dia in enumerate(stats_admin['top_5_dias'], start=1):
        print(f"{i}. Fecha: {dia['fecha']} Depósitos:{dia['total_depositos']:.2f} "
              f"Gastos:{dia['total_gastos']:.2f} Neto:{dia['neto']:.2f}")

    # ==============================
    # ANOMALÍAS
    # ==============================
    anomalias = analitica_service.ejecutar_modulo_anomalias()

    print("\n=== ANOMALÍAS Z-SCORE ===")
    for a in anomalias["z_score"]:
        print(a)

    print("\n=== ANOMALÍAS STRUCTURING ===")
    for a in anomalias["structuring"]:
        print(a)

    print("\n=== ANOMALÍAS ACTIVIDAD NOCTURNA ===")
    for a in anomalias["actividad_nocturna"]:
        print(a)

