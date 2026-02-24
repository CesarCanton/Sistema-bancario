from repositories.usuarioRepository import UsuarioRepository
from repositories.cuentaRepository import CuentaRepository
from repositories.transaccionRepository import TransaccionRepository
import numpy as np
from models.usuario import Usuario
from analytics.numpyAnalisis import constructor_matrices, estadisticas_por_cuenta, estadisticas_admin

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
        

def listaDeCuentas():
    cuentasRepo=CuentaRepository()
    for cuenta in cuentasRepo.datos:
        print(f"\033[1;36;40mId\033[0m {cuenta["id"]}. "
              f"Tipo de cuenta: {cuenta["tipo"]}. "
              f"Id del propietario: {cuenta["propietarioId"]}. "
              f"Estado de cuenta: {cuenta["estado"]}. "
              f"Saldo: {cuenta["saldo"]}\n")


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
    

