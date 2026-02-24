import numpy as np
from datetime import datetime


#Total de depositos y gastos por cada dia

def constructor_matrices(transacciones):
    
    cuentas = set()
    fechas = set()
    registros = []

    # Parsing permitido
    for t in transacciones:
        cuenta = t["cuentaId"]
        tipo = t["tipo"]
        monto = float(t["monto"])

        # Si fecha viene como string
        if isinstance(t["fecha"], str):
            fecha_obj = datetime.strptime(t["fecha"], "%Y-%m-%d %H:%M:%S")
        else:
            fecha_obj = t["fecha"]

        fecha = fecha_obj.date()

        cuentas.add(cuenta)
        fechas.add(fecha)

        registros.append((cuenta, fecha, tipo, monto))

    cuentas = sorted(list(cuentas))
    fechas = sorted(list(fechas))

    n_cuentas = len(cuentas)
    n_dias = len(fechas)

    cuenta_index = {c: i for i, c in enumerate(cuentas)}
    fecha_index = {f: i for i, f in enumerate(fechas)}

    X_depositos = np.zeros((n_cuentas, n_dias))
    X_gastos = np.zeros((n_cuentas, n_dias))

    for cuenta, fecha, tipo, monto in registros:
        i = cuenta_index[cuenta]
        j = fecha_index[fecha]

        if tipo == "DEPOSITO":
            X_depositos[i, j] += monto
        else:
            X_gastos[i, j] += monto

    return X_depositos, X_gastos, cuentas, fechas

def estadisticas_por_cuenta(X_depositos, X_gastos):
    """
    Nota para mis compas: Para hacer uso de este metodo, previamente se tuvo que llamar
    al metodo de arriba para hacer las matrices.
    Pasos:
    1. Crear un objeto de tipo "TransaccionRepository" y enviar "transacciones.datos" al metodo
    de aqui arriba
    2. Desempaquetar con: X_dep, X_gas, cuentas, fechas = constructor_matrices(transacciones.datos)
    3. Llamar a este metodo con los dos arrays desempaquetados:
    stats_cuentas = estadisticas_por_cuenta(X_dep, X_gas)
    
    PD: En el servicio "adminService" deje comentada una solucion en la que recorri todas las cuentas,
    para que te hagas una idea
    
    """

    total_depositos = np.sum(X_depositos, axis=1)
    promedio_diario = np.mean(X_depositos, axis=1)
    desviacion = np.std(X_depositos, axis=1)

    p50 = np.percentile(X_depositos, 50, axis=1)
    p90 = np.percentile(X_depositos, 90, axis=1)
    p99 = np.percentile(X_depositos, 99, axis=1)

    total_gastos = np.sum(X_gastos, axis=1)

    ratio = np.divide(
        total_depositos,
        total_gastos,
        out=np.zeros_like(total_depositos),
        where=total_gastos != 0
    )

    return {
        "total_depositos": total_depositos,
        "promedio_diario": promedio_diario,
        "desviacion": desviacion,
        "p50": p50,
        "p90": p90,
        "p99": p99,
        "ratio": ratio
    }
    

def estadisticas_admin(X_depositos, X_gastos, cuentas, fechas):
    total_diario_depositos = np.sum(X_depositos, axis=0)
    total_diario_gastos = np.sum(X_gastos, axis=0)
    total_diario_neto = total_diario_depositos - total_diario_gastos

    top_5_dias = np.argsort(total_diario_depositos)[-5:][::-1]

    total_cuenta_depositos = np.sum(X_depositos, axis=1)
    total_cuenta_gastos = np.sum(X_gastos, axis=1)
    
    indices_top_dep = np.argsort(total_cuenta_depositos)[-10:][::-1]

    top_10_depositos = [
        {
            "cuenta": cuentas[i],
            "total_depositos": total_cuenta_depositos[i]
        }
        for i in indices_top_dep
    ]

    indices_top_gas = np.argsort(total_cuenta_gastos)[-10:][::-1]

    top_10_gastos = [
        {
            "cuenta": cuentas[i],
            "total_gastos": total_cuenta_gastos[i]
        }
        for i in indices_top_gas
    ]
    
    indices_top_dias = np.argsort(total_diario_depositos)[-5:][::-1]

    top_5_dias = [
        {
            "fecha": fechas[i],
            "total_depositos": total_diario_depositos[i],
            "total_gastos": total_diario_gastos[i],
            "neto": total_diario_neto[i]
        }
        for i in indices_top_dias
    ]


    return {
        "total_diario_depositos": total_diario_depositos,
        "total_diario_gastos": total_diario_gastos,
        "total_diario_neto": total_diario_neto,
        "top_5_dias": top_5_dias,
        "top_10_depositos": top_10_depositos,
        "top_10_gastos": top_10_gastos
    }

def totales_diarios_por_cuenta(account_id, X_depositos, X_gastos, cuentas, fechas):

    # Verificar que la cuenta existe
    if account_id not in cuentas:
        raise ValueError("La cuenta no existe en la matriz")

    # Obtener índice de la cuenta
    indice = cuentas.index(account_id)

    # Extraer la fila correspondiente
    depositos_diarios = X_depositos[indice, :]
    gastos_diarios = X_gastos[indice, :]

    # Calcular neto diario
    neto_diario = depositos_diarios - gastos_diarios

    # Construir resultado estructurado
    resultado = [
        {
            "fecha": fechas[i],
            "depositos": depositos_diarios[i],
            "gastos": gastos_diarios[i],
            "neto": neto_diario[i]
        }
        for i in range(len(fechas))
    ]

    return resultado
    
    