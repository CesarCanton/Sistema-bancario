from services.cuentaService import CuentaService


class InterfazCliente:

    def __init__(self):
            self.cuenta_service = CuentaService()
    # =========================
    # MENU
    # =========================
    def menu(self, cliente):

        while True:
            print("\n====== CLIENTE ======")
            print("1. Ver cuentas")
            print("2. Depositar")
            print("3. Retirar")
            print("4. Transferir")
            print("5. Salir")

            op = input("Seleccione: ")

            if op == "1":
                self.ver_cuentas(cliente)

            elif op == "2":
                self.depositar(cliente)

            elif op == "3":
                self.retirar(cliente)

            elif op == "4":
                self.transferir(cliente)

            elif op == "5":
                break
            else:
                print("Opción inválida")

    # =========================
    # VER CUENTAS
    # =========================
    def ver_cuentas(self, cliente):

        cuentas = CuentaService.obtener_cuentas_de_usuario(cliente["id"])

        if not cuentas:
            print("No tiene cuentas")
            return

        for c in cuentas:
            print(f"ID:{c.id} | Tipo:{c.tipo} | Saldo:{c.saldo} | Estado:{c.estado}")

    # =========================
    # DEPOSITAR
    # =========================
    def depositar(self, cliente):

        origen = self.seleccionar_cuenta_origen(cliente)
        if not origen:
            return

        try:
            monto = float(input("Monto: "))
            self.cuenta_service.depositar(origen.id, monto)
            print("Depósito exitoso")
        except Exception as e:
            print(e)

    # =========================
    # RETIRAR
    # =========================
    def retirar(self, cliente):

        origen = self.seleccionar_cuenta_origen(cliente)
        if not origen:
            return

        try:
            monto = float(input("Monto: "))
            self.cuenta_service.retirar(origen.id, monto)
            print("Retiro exitoso")
        except Exception as e:
            print(e)

    # =========================
    # TRANSFERIR
    # =========================
    def transferir(self, cliente):

        origen = self.seleccionar_cuenta_origen(cliente)
        if not origen:
            return

        print(f"\nCuenta origen: {origen.id}")
        print(f"Saldo disponible: {origen.saldo}")

        destino = input("Cuenta destino: ")

        if str(destino) == str(origen.id):
            print("No puedes transferir a tu misma cuenta")
            return

        try:
            monto = float(input("Monto: "))
            self.cuenta_service.transferir(origen.id, destino, monto)
            print("Transferencia exitosa")
        except Exception as e:
            print(e)

    def seleccionar_cuenta_origen(self, cliente):

        cuentas = self.cuenta_service.obtener_cuentas_de_usuario(cliente["id"])

        if not cuentas:
            print("No tienes cuentas registradas")
            return None

        # 👉 solo una cuenta
        if len(cuentas) == 1:
            return cuentas[0]

        # 👉 varias cuentas → mostrar menú
        print("\nSeleccione cuenta origen:")

        for i, c in enumerate(cuentas, start=1):
            print(f"{i}. ID:{c.id} | Tipo:{c.tipo} | Saldo:{c.saldo}")

        try:
            op = int(input("Opción: "))
            if 1 <= op <= len(cuentas):
                return cuentas[op-1]
        except:
            pass

        print("Selección inválida")
        return None                     

# =========================
# WRAPPER PARA LOGIN
# =========================

def mostrarInterfazCliente(cliente):
    interfaz = InterfazCliente()
    interfaz.menu(cliente)