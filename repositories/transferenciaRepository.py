from repositories.baseRepository import BaseRepository

class TransferenciaRepository(BaseRepository):

    def __init__(self):
        super().__init__(
            "data/transferencias.txt",
            ["id", "cuentaOrigen", "cuentaDestino", "monto", "fecha"]
        )
        self.cargar_datos()
    
    def cargar_datos(self):
        return super().cargar_datos()