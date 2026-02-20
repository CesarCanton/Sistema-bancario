from repositories.baseRepository import BaseRepository

class TransaccionRepository(BaseRepository):
    
    def __init__(self):
        super().__init__("data/transacciones.txt",
                         ["id","cuentaId","tipo","monto","fecha"]
                         )