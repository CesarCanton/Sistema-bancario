import numpy as np
from collections import defaultdict
from datetime import datetime, time
from models.transaccion import Transaccion

class AnaliticaService:
    def __init__(self, transaccion_repository):
        self.transaccion_repository = transaccion_repository

    # Convertir diccionarios a objetos Transaccion
    def _cargar_transacciones(self):
        transacciones_dict = self.transaccion_repository.get_all()
        transacciones = []

        for t in transacciones_dict:
            transacciones.append(
                Transaccion(
                    id=t["id"],
                    cuentaId=t["cuentaId"],
                    tipo=t["tipo"],
                    monto=t["monto"],
                    fecha=t["fecha"]
                )
            )
        return transacciones

    # ================== ANOMALÍA 1 ==================
    def detectar_anomalias_zscore(self):
        transacciones = self._cargar_transacciones()
        anomalías = []
        cuentas = defaultdict(lambda: defaultdict(float))

        for t in transacciones:
            if t.tipo.upper() == "DEPOSITO":
                fecha_dia = t.fecha.date()
                cuentas[t.cuentaId][fecha_dia] += t.monto

        for cuentaId, dias in cuentas.items():
            valores = np.array(list(dias.values()))
            if len(valores) < 2: continue
            media = np.mean(valores)
            std = np.std(valores)
            if std == 0: continue

            z_scores = (valores - media) / std
            fechas = list(dias.keys())

            for i, z in enumerate(z_scores):
                if abs(z) > 3:
                    anomalías.append({
                        "cuentaId": cuentaId,
                        "fecha": str(fechas[i]),
                        "total_dia": float(valores[i]),
                        "z_score": float(z)
                    })
        return anomalías

    # ================== ANOMALÍA 2 ==================
    def detectar_structuring(self):
        transacciones = self._cargar_transacciones()
        anomalías = []
        cuentas = defaultdict(lambda: defaultdict(list))

        for t in transacciones:
            if t.tipo.upper() == "DEPOSITO":
                fecha_dia = t.fecha.date()
                cuentas[t.cuentaId][fecha_dia].append(t.monto)

        for cuentaId, dias in cuentas.items():
            for fecha, montos in dias.items():
                montos_np = np.array(montos)
                if len(montos_np) >= 4 and np.all(montos_np <= 50):
                    anomalías.append({
                        "cuentaId": cuentaId,
                        "fecha": str(fecha),
                        "cantidad_depositos": int(len(montos_np)),
                        "detalle_montos": montos_np.tolist()
                    })
        return anomalías

    # ================== ANOMALÍA 3 ==================
    def detectar_actividad_nocturna(self):
        transacciones = self._cargar_transacciones()
        anomalías = []
        cuentas = defaultdict(lambda: defaultdict(int))

        for t in transacciones:
            hora = t.fecha.time()
            if hora >= time(21, 0) or hora <= time(4, 0):
                fecha_dia = t.fecha.date()
                cuentas[t.cuentaId][fecha_dia] += 1

        for cuentaId, dias in cuentas.items():
            valores = np.array(list(dias.values()))
            if len(valores) < 2: continue
            media = np.mean(valores)
            std = np.std(valores)
            if std == 0: continue

            z_scores = (valores - media) / std
            fechas = list(dias.keys())

            for i, z in enumerate(z_scores):
                if z > 3:
                    anomalías.append({
                        "cuentaId": cuentaId,
                        "fecha": str(fechas[i]),
                        "transacciones_nocturnas": int(valores[i]),
                        "z_score": float(z)
                    })
        return anomalías

    # Ejecutar todas las anomalías
    def ejecutar_modulo_anomalias(self):
        return {
            "z_score": self.detectar_anomalias_zscore(),
            "structuring": self.detectar_structuring(),
            "actividad_nocturna": self.detectar_actividad_nocturna()
        }