from repositories.baseRepository import BaseRepository

class CuentaRepository(BaseRepository):

    def __init__(self):
        super().__init__(
            "data/cuentas.txt",
            ["id", "propietarioId", "tipo", "saldo", "estado"]
        )