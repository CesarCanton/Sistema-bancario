import csv
from datetime import datetime
from models.cuenta import Cuenta
from models.transaccion import Transaccion
from models.transferencia import Transferencia


class CuentaService:

    CUENTAS = "data/cuentas.txt"
    TRANSACCIONES = "data/transacciones.txt"
    TRANSFERENCIAS = "data/transferencias.txt"

    # =========================
    # helpers
    # =========================

    @staticmethod
    def _leer_cuentas():
        cuentas = []
        with open(CuentaService.CUENTAS, newline='', encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="|"):
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
    def _registrar_transaccion(cuentaId, tipo, monto):
        rows = list(csv.reader(open(CuentaService.TRANSACCIONES)))
        tx_id = len(rows)

        with open(CuentaService.TRANSACCIONES, "a", newline='', encoding="utf-8") as f:
            writer = csv.writer(f, delimiter="|")
            writer.writerow([
                tx_id,
                cuentaId,
                tipo,
                monto,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ])

    @staticmethod
    def ver_saldo(cuentaId):

        cuentas = CuentaService._leer_cuentas()

        for c in cuentas:
            if str(c.id) == str(cuentaId):
                return c.saldo

        raise Exception("Cuenta no existe")

    # =========================

    @staticmethod
    def depositar(cuentaId, monto):

        if monto <= 0:
            raise Exception("Monto inválido")

        cuentas = CuentaService._leer_cuentas()

        for c in cuentas:
            if str(c.id) == str(cuentaId):

                if c.estado != "activa":
                    raise Exception("Cuenta bloqueada")

                c.saldo += monto
                CuentaService._registrar_transaccion(cuentaId, "deposito", monto)
                CuentaService._guardar_cuentas(cuentas)

                return

        raise Exception("Cuenta no existe")

    # =========================

    @staticmethod
    def retirar(cuentaId, monto):

        if monto <= 0:
            raise Exception("Monto inválido")

        cuentas = CuentaService._leer_cuentas()

        for c in cuentas:
            if str(c.id) == str(cuentaId):

                if c.estado != "activa":
                    raise Exception("Cuenta bloqueada")

                if c.saldo < monto:
                    raise Exception("Saldo insuficiente")

                c.saldo -= monto
                CuentaService._registrar_transaccion(cuentaId, "retiro", monto)
                CuentaService._guardar_cuentas(cuentas)

                return

        raise Exception("Cuenta no existe")

    # =========================

    @staticmethod
    def transferir(origenId, destinoId, monto):

        if monto <= 0:
            raise Exception("Monto inválido")

        cuentas = CuentaService._leer_cuentas()

        origen = None
        destino = None

        for c in cuentas:
            if str(c.id) == str(origenId):
                origen = c
            if str(c.id) == str(destinoId):
                destino = c

        if not origen:
            raise Exception("Cuenta origen no existe")

        if not destino:
            raise Exception("Cuenta destino no existe")

        if origen.estado != "activa":
            raise Exception("Cuenta origen bloqueada")

        if destino.estado != "activa":
            raise Exception("Cuenta destino bloqueada")

        if origen.saldo < monto:
            raise Exception("Saldo insuficiente")

        origen.saldo -= monto
        destino.saldo += monto

        CuentaService._guardar_cuentas(cuentas)

        # registrar transferencia
        rows = list(csv.reader(open(CuentaService.TRANSFERENCIAS)))
        tx_id = len(rows)

        with open(CuentaService.TRANSFERENCIAS, "a", newline='', encoding="utf-8") as f:
            writer = csv.writer(f, delimiter="|")
            writer.writerow([
                tx_id,
                origenId,
                destinoId,
                monto,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ])