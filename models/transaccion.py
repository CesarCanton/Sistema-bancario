from datetime import datetime

class Transaccion:
    def __init__(self,id,cuentaId,tipo,monto,fecha):
        self.id = int(id)
        self.cuentaId = int(cuentaId)
        self.tipo = tipo
        self.monto = float(monto)
        self.fecha = datetime.strptime(fecha.strip(), "%Y-%m-%d %H:%M:%S")