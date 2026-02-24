from repositories.usuarioRepository import UsuarioRepository
from repositories.cuentaRepository import CuentaRepository
from repositories.transaccionRepository import TransaccionRepository
import numpy as np
from models.usuario import Usuario
from analytics.numpyAnalisis import constructor_matrices, estadisticas_por_cuenta, estadisticas_admin

usuario_repo = UsuarioRepository()

def get_next_id():
    if not usuario_repo.datos:
        return 1
    return max(int(u["id"]) for u in usuario_repo.datos) + 1

def generar_username_admin(nombres, apellidos, id):
    siglas = nombres[0].lower() + apellidos[0].lower()
    username = siglas + str(id)
    return username 

def crear_admin(nombres, apellidos, dui, pin, rol):

    repo=UsuarioRepository()
    if len(pin) != 4 or not pin.isdigit():
        raise Exception("PIN inválido")
    
    id=len(repo.datos)+1

    
    username=generar_username_admin(nombres, apellidos, id)   
    nuevoAdmin= Usuario(id,nombres,apellidos,dui,pin,rol,username)
    repo.agregar(nuevoAdmin) 

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

    X_dep, X_gas, cuentas, fechas = constructor_matrices(transacciones.datos)

    # stats_cuentas = estadisticas_por_cuenta(X_dep, X_gas)
    stats_admin = estadisticas_admin(X_dep, X_gas, cuentas, fechas)

    # print("\033[1;36;40m=== Estadísticas por Cuenta ===\033[0m")
    # for i, cuenta in enumerate(cuentas):
    #     print(f"\033[1;36;40mCuenta {cuenta}:\033[0m Total Depósitos: {stats_cuentas['total_depositos'][i]:.2f}, "
    #         f"Promedio Diario: {stats_cuentas['promedio_diario'][i]:.2f}, "
    #         f"Desviación Estándar: {stats_cuentas['desviacion'][i]:.2f}")
    
    print("\n\033[1;36;40m=== Estadísticas Administrativas ===\033[0m")
    
    print(f"\033[1;36;40mSuma total de todos los depósitos: \033[0m{np.sum(stats_admin['total_diario_depositos'])}" )
    print(f"\033[1;36;40mTotal diario de gastos: \033[0m{np.sum(stats_admin['total_diario_gastos'])}")
    print(f"\033[1;36;40mTotal diario neto: \033[0m{np.sum(stats_admin['total_diario_neto'])}")

    print("\n\n\033[1;36;40m=== TOP 10 DEPOSITOS ===\033[0m\n")
    for i, cuenta in enumerate(stats_admin['top_10_depositos'],start=1):
        print(f"\033[1;36;40m{i}. Cuenta: {cuenta['cuenta']} \033[0m Total:{cuenta['total_depositos']:.2f}")
    
    print("\n\n\033[1;36;40m=== TOP 10 GASTOS ===\033[0m\n")
    
    for i, cuenta in enumerate(stats_admin['top_10_gastos'],start=1):
        print(f"\033[1;36;40m{i}. Cuenta: {cuenta['cuenta']} \033[0m Total:{cuenta['total_gastos']:.2f}")
    
    
    
    print("\n\n\033[1;36;40m=== TOP 5 DIAS CON MAYOR ACTIVIDAD ===\033[0m\n")
    
    for i, dia in enumerate(stats_admin['top_5_dias'],start=1):
        print(f"\033[1;36;40m{i}. Fecha: {dia['fecha']} \033[0m Deposito: {dia['total_depositos']:.2f} " 
              f"Gastos: ${dia['total_gastos']:.2f} Neto: ${dia['neto']:.2f}")
    # return stats_cuentas, stats_admin
    

