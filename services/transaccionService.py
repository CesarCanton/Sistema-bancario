from datetime import datetime

def autoAsignarFechaHora():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def filtrarTransaccionesPorFecha(transacciones, fecha_inicio, fecha_fin):
    transacciones_filtradas = []
    for transaccion in transacciones:
        fecha_transaccion = datetime.strptime(transaccion['fecha_hora'], "%Y-%m-%d %H:%M:%S")
        if fecha_inicio <= fecha_transaccion <= fecha_fin:
            transacciones_filtradas.append(transaccion)    
    return transacciones_filtradas


