from repositories.baseRepository import BaseRepository

class UsuarioRepository(BaseRepository):

    def __init__(self):
        super().__init__(
            "data/usuarios.txt",
            ["id","rol", "nombres", "apellidos", "dui", "pin","username"]
        )