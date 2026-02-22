from repositories.baseRepository import BaseRepository

class UsuarioRepository(BaseRepository):

    def __init__(self):
        super().__init__(
            "data/usuarios.txt",
            ["id","rol", "nombres", "apellidos", "dui", "pin","username"]
        )
        self.cargar_datos()
        
    def cargar_datos(self):
        return super().cargar_datos()