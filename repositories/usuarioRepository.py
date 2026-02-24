from repositories.baseRepository import BaseRepository

class UsuarioRepository(BaseRepository):

    def __init__(self):
        super().__init__(
            "data/usuarios.txt",
            ["id","rol", "nombres", "apellidos", "dui", "pin","username"]
        )
        self.cargar_datos()
        self.guardar_datos()
        
        
    def cargar_datos(self):
        return super().cargar_datos()
    
    def guardar_datos(self):
        return super().guardar_datos()
    
    def agregar(self,usuario):
        if hasattr(usuario,'__dict__'):
            usuarioDict=usuario.__dict__
        else:
            usuarioDict=usuario
        return super().agregar(usuarioDict)

    def buscar_por_credenciales(self, credencial, pin):

        for usuario in self.datos:
            if usuario["pin"] == pin and (
                usuario["dui"] == credencial or usuario["username"] == credencial
            ):
                return usuario

        return None
    
