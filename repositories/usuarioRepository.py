from repositories.baseRepository import BaseRepository

class UsuarioRepository(BaseRepository):

    def __init__(self):
        super().__init__(
            "data/usuarios.txt",
            ["id", "nombres", "apellidos", "dui", "pin", "rol"]
        )