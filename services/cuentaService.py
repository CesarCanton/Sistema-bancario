import csv
from datetime import datetime
from models.cuenta import Cuenta
from analytics.numpyAnalisis import constructor_matrices, estadisticas_por_cuenta, totales_diarios_por_cuenta
from repositories.transaccionRepository import TransaccionRepository


class CuentaService:

    CUENTAS = "data/cuentas.txt"
    TRANSACCIONES = "data/transacciones.txt"
    TRANSFERENCIAS = "data/transferencias.txt"

    # =========================
    # HELPERS
    # =========================

    @staticmethod
    def _leer_cuentas():
        cuentas = []
        with open(CuentaService.CUENTAS, newline='', encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="|"):
                row["saldo"] = float(row["saldo"])
                cuentas.append(Cuenta(**row))
        return cuentas

    @staticmethod
    def _guardar_cuentas(cuentas):
        with open(CuentaService.CUENTAS, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f, delimiter="|")
            writer.writerow(["id", "propietarioId", "tipo", "saldo", "estado"])
            for c in cuentas:
                writer.writerow([c.id, c.propietarioId, c.tipo, c.saldo, c.estado])

    @staticmethod
    def _estado_activo(estado):
        return str(estado).strip().upper() == "ACTIVA"

    @staticmethod
    def _next_id(path):
        try:
            with open(path, encoding="utf-8") as f:
                return len(list(csv.reader(f)))
        except:
            return 0

    @staticmethod
    def _registrar_transaccion(cuentaId, tipo, monto):
        tx_id = CuentaService._next_id(CuentaService.TRANSACCIONES)

        with open(CuentaService.TRANSACCIONES, "a", newline='', encoding="utf-8") as f:
            writer = csv.writer(f, delimiter="|")
            writer.writerow([
                tx_id,
                cuentaId,
                tipo,
                monto,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ])

    # =========================
    # CONSULTAS
    # =========================

    @staticmethod
    def obtener_cuentas_de_usuario(usuarioId):
        cuentas = CuentaService._leer_cuentas()
        return [c for c in cuentas if str(c.propietarioId) == str(usuarioId)]

    @staticmethod
    def existe_cuenta(cuentaId):
        cuentas = CuentaService._leer_cuentas()
        return any(str(c.id) == str(cuentaId) for c in cuentas)

    @staticmethod
    def ver_saldo(cuentaId):
        cuentas = CuentaService._leer_cuentas()
        for c in cuentas:
            if str(c.id) == str(cuentaId):
                return c.saldo
        raise Exception("Cuenta no existe")

    # =========================
    # DEPOSITAR
    # =========================

    @staticmethod
    def depositar(cuentaId, monto):

        if monto <= 0:
            raise Exception("Monto inválido")

        cuentas = CuentaService._leer_cuentas()

        for c in cuentas:
            if str(c.id) == str(cuentaId):

                if not CuentaService._estado_activo(c.estado):
                    raise Exception("Cuenta bloqueada")

                c.saldo += monto
                CuentaService._registrar_transaccion(cuentaId, "deposito", monto)
                CuentaService._guardar_cuentas(cuentas)
                return

        raise Exception("Cuenta no existe")

    # =========================
    # RETIRAR
    # =========================

    @staticmethod
    def retirar(cuentaId, monto):

        if monto <= 0:
            raise Exception("Monto inválido")

        cuentas = CuentaService._leer_cuentas()

        for c in cuentas:
            if str(c.id) == str(cuentaId):

                if not CuentaService._estado_activo(c.estado):
                    raise Exception("Cuenta bloqueada")

                if c.saldo < monto:
                    raise Exception("Saldo insuficiente")

                c.saldo -= monto
                CuentaService._registrar_transaccion(cuentaId, "retiro", monto)
                CuentaService._guardar_cuentas(cuentas)
                return

        raise Exception("Cuenta no existe")

    # =========================
    # TRANSFERIR
    # =========================

    @staticmethod
    def transferir(origenId, destinoId, monto):

        # normalizar tipos
        origenId = str(origenId)
        destinoId = str(destinoId)

        try:
            monto = float(monto)
        except:
            raise Exception("Monto inválido")

        if monto <= 0:
            raise Exception("Monto inválido")

        if origenId == destinoId:
            raise Exception("No puedes transferirte a la misma cuenta")

        cuentas = CuentaService._leer_cuentas()

        origen = None
        destino = None

        for c in cuentas:
            if str(c.id) == origenId:
                origen = c
            if str(c.id) == destinoId:
                destino = c

        if not origen:
            raise Exception("Cuenta origen no existe")

        if not destino:
            raise Exception("Cuenta destino no existe")

        if not CuentaService._estado_activo(origen.estado):
            raise Exception("Cuenta origen bloqueada")

        if not CuentaService._estado_activo(destino.estado):
            raise Exception("Cuenta destino bloqueada")

        if origen.saldo < monto:
            raise Exception("Saldo insuficiente")

        # transferencia
        origen.saldo -= monto
        destino.saldo += monto

        # historial
        CuentaService._registrar_transaccion(origenId, "transferencia_salida", monto)
        CuentaService._registrar_transaccion(destinoId, "transferencia_entrada", monto)

        #  guardar cuentas
        CuentaService._guardar_cuentas(cuentas)

        # log de transferencias
        tx_id = CuentaService._next_id(CuentaService.TRANSFERENCIAS)

        with open(CuentaService.TRANSFERENCIAS, "a", newline='', encoding="utf-8") as f:
            writer = csv.writer(f, delimiter="|")
            writer.writerow([
                tx_id,
                origenId,
                destinoId,
                monto,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ])
            
    @staticmethod
    def analisis_por_dia(cuentaId):
        transacciones = TransaccionRepository()

        X_dep, X_gas, cuentas, fechas = constructor_matrices(transacciones.datos)
        resultado= totales_diarios_por_cuenta(cuentaId,X_dep,X_gas,cuentas,fechas)

        print("\033[1;36;40m=== Estadísticas De Las cuentas ===\033[0m")
        
        for dia in resultado:
                    print(
                    f"Fecha: {dia['fecha']} | "
                    f"Depósitos: ${dia['depositos']:.2f} | "
                    f"Gastos: ${dia['gastos']:.2f} | "
                    f"Neto: ${dia['neto']:.2f}")
        
    @staticmethod
    def analisis_general(cuentaId):
        transacciones = TransaccionRepository()

        X_dep, X_gas, cuentas, fechas= constructor_matrices(transacciones.datos)
        stats_cuentas= estadisticas_por_cuenta(X_dep,X_gas)
        
            
        for i, cuenta in enumerate(cuentas):
            if cuenta==cuentaId:
                print("\033[1;36;40m=== Estadísticas de la cuenta ===\033[0m")
                
                print(f"\033[1;36;40mCuenta {cuenta}:\033[0m"
                f"\nTotal Depósitos: {stats_cuentas['total_depositos'][i]:.2f}, "
                f"\nPromedio Diario: {stats_cuentas['promedio_diario'][i]:.2f}, "
                f"\nDesviación Estándar: {stats_cuentas['desviacion'][i]:.2f}")
        
            
        
        
        