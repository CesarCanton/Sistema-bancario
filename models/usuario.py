class Usuario:

    def __init__(self, id, nombres, apellidos, dui, pin, rol, username):
        self.id = str(id)
        self.nombres = nombres
        self.apellidos = apellidos
        self.dui = dui
        self.pin = pin
        self.rol = rol
        self.username = username

    def to_dict(self):
        return {
            "id": self.id,
            "rol": self.rol,
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "dui": self.dui,
            "pin": self.pin,
            "username": self.username
        }