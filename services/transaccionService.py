from datetime import datetime
from repositories.transaccionRepository import TransaccionRepository


class TransaccionService:

    def __init__(self):
        self.repo = TransaccionRepository()

    # ===============================
    # AUTO FECHA
    # ===============================
    def autoAsignarFechaHora(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ===============================
    # REGISTRAR TRANSACCION
    # ===============================
    def registrar(self, tipo, cuenta_origen, cuenta_destino, monto, username):

        nueva = {
            "id": len(self.repo.datos) + 1,
            "tipo": tipo,
            "origen": cuenta_origen,
            "destino": cuenta_destino,
            "monto": monto,
            "username": username,
            "fecha_hora": self.autoAsignarFechaHora()
        }

        self.repo.agregar(nueva)

    # ===============================
    # HISTORIAL POR USUARIO
    # ===============================
    def obtener_por_usuario(self, username):

        return [
            t for t in self.repo.datos
            if t["username"] == username
        ]

    # ===============================
    # FILTRAR POR FECHA
    # ===============================
    def filtrar_por_fecha(self, username, fecha_inicio, fecha_fin):

        transacciones = self.obtener_por_usuario(username)

        resultado = []

        for t in transacciones:
            fecha = datetime.strptime(t["fecha_hora"], "%Y-%m-%d %H:%M:%S")

            if fecha_inicio <= fecha <= fecha_fin:
                resultado.append(t)

        return resultado