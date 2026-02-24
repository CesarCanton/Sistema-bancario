from models.usuario import Usuario


class UsuarioService:

    def __init__(self, usuario_repo):
        self.usuario_repo = usuario_repo

    # =============================
    # USERNAME AUTO
    # =============================

    def generar_username(self, nombres, apellidos):
        siglas = nombres.split()[0][0].lower() + apellidos.split()[0][0].lower()
        next_id = self.usuario_repo.get_next_username_id(siglas)
        return f"{siglas}{next_id}"

    # =============================
    # CREAR CLIENTE
    # =============================

    def crear_cliente(self, nombres, apellidos, dui, pin):

        if self.usuario_repo.buscar_por_dui(dui):
            raise Exception("El DUI ya existe")

        id_user = self.usuario_repo.get_next_id()
        username = self.generar_username(nombres, apellidos)

        usuario = Usuario(
            id_user,
            nombres,
            apellidos,
            dui,
            pin,
            "cliente",
            username
        )

        self.usuario_repo.agregar_usuario(usuario)

        return username

    # =============================
    # CREAR ADMIN
    # =============================

    def crear_admin(self, nombres, apellidos, pin):

        id_user = self.usuario_repo.get_next_id()
        username = self.generar_username(nombres, apellidos)

        usuario = Usuario(
            id_user,
            nombres,
            apellidos,
            "N/A",
            pin,
            "admin",
            username
        )

        self.usuario_repo.agregar_usuario(usuario)

        return username

    # =============================
    # LOGIN
    # =============================

    def login_cliente(self, dui, pin):
        user = self.usuario_repo.buscar_por_dui(dui)

        if not user or user["pin"] != pin:
            raise Exception("Credenciales inválidas")

        return user

    def login_admin(self, username, pin):
        user = self.usuario_repo.buscar_por_username(username)

        if not user or user["pin"] != pin:
            raise Exception("Credenciales inválidas")

        return user