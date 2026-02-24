from repositories.baseRepository import BaseRepository

class TransaccionRepository(BaseRepository):
    
    def __init__(self):
        super().__init__("data/transacciones.txt",
                         ["id","cuentaId","tipo","monto","fecha"]
                         )
        self.cargar_datos()
    
    def cargar_datos(self):
        return super().cargar_datos()