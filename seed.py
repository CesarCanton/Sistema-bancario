import os
import numpy as np
from datetime import datetime, timedelta

# =====================================================
# MODELOS DE DATOS
# =====================================================

class Usuario:
    def __init__(self, id, nombres, apellidos, dui, pin, rol, username):
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos
        self.dui = dui
        self.pin = pin
        self.rol = rol
        self.username = username

    def __str__(self):
        return f"{self.id}|{self.rol}|{self.nombres}|{self.apellidos}|{self.dui}|{self.pin}|{self.username}"

class Cuenta:
    def __init__(self, id, propietarioId, tipo, saldo, estado):
        self.id = id
        self.propietarioId = propietarioId
        self.tipo = tipo
        self.saldo = saldo
        self.estado = estado

    def __str__(self):
        return f"{self.id}|{self.propietarioId}|{self.tipo}|{self.saldo}|{self.estado}"

class Transaccion:
    def __init__(self, id, cuentaId, tipo, monto, fecha):
        self.id = id
        self.cuentaId = cuentaId
        self.tipo = tipo
        self.monto = monto
        self.fecha = fecha

    def __str__(self):
        return f"{self.id}|{self.cuentaId}|{self.tipo}|{self.monto}|{self.fecha}"

class Transferencia:
    def __init__(self, id, cuentaOrigen, cuentaDestino, monto, fecha):
        self.id = id
        self.cuentaOrigen = cuentaOrigen
        self.cuentaDestino = cuentaDestino
        self.monto = monto
        self.fecha = fecha

    def __str__(self):
        return f"{self.id}|{self.cuentaOrigen}|{self.cuentaDestino}|{self.monto}|{self.fecha}"

# =====================================================
# CONFIGURACIÓN Y UTILIDADES
# =====================================================

NUM_CLIENTES = 80
MAX_CUENTAS_POR_CLIENTE = 2
NUM_DIAS = 30
TRANSACCIONES_BASE = 8000

np.random.seed(42)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data")

def ensure_data_folder():
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)

def random_timestamp(start_date):
    day_offset = np.random.randint(0, NUM_DIAS)
    hour = np.random.randint(0, 24)
    minute = np.random.randint(0, 60)
    return (start_date + timedelta(days=int(day_offset))).replace(hour=hour, minute=minute)

# =====================================================
# GENERACIÓN DE OBJETOS
# =====================================================

def generate_data():
    usuarios = []
    cuentas = []
    transacciones = []
    transferencias = []

    # 1. Usuarios
    nombres_pool = ["Carlos","Ana","Luis","Maria","Jorge","Sofia","Ricardo","Valeria"]
    apellidos_pool = ["Gomez","Lopez","Martinez","Hernandez","Perez","Torres"]
    
    # Admin
    usuarios.append(Usuario(1, "Juan", "Perez", "00000000-0", "1234", "ADMIN", "jp1"))

    for i in range(2, NUM_CLIENTES + 2):
        u = Usuario(
            id=i,
            nombres=np.random.choice(nombres_pool),
            apellidos=np.random.choice(apellidos_pool),
            dui=f"{np.random.randint(10000000,99999999)}-{np.random.randint(0,9)}",
            pin=str(np.random.randint(1000,9999)),
            rol="CLIENTE",
            username=""
        )
        usuarios.append(u)

        # 2. Cuentas para cada usuario
        for _ in range(np.random.randint(1, MAX_CUENTAS_POR_CLIENTE + 1)):
            c = Cuenta(
                id=len(cuentas) + 1,
                propietarioId=u.id,
                tipo=np.random.choice(["AHORRO", "CORRIENTE"]),
                saldo=round(np.random.uniform(500, 5000), 2),
                estado="ACTIVA"
            )
            cuentas.append(c)

    # 3. Transacciones y Transferencias
    start_date = datetime.now() - timedelta(days=NUM_DIAS)
    acc_ids = [c.id for c in cuentas]

    for i in range(1, TRANSACCIONES_BASE + 1):
        acc_id = np.random.choice(acc_ids)
        tipo = np.random.choice(["DEPOSITO", "RETIRO"])
        monto = round(np.random.uniform(10, 500), 2)
        fecha = random_timestamp(start_date).strftime("%Y-%m-%d %H:%M:%S")
        
        transacciones.append(Transaccion(len(transacciones)+1, acc_id, tipo, monto, fecha))

        # Transferencia (20% probabilidad)
        if np.random.rand() < 0.2:
            destino = np.random.choice(acc_ids)
            if destino != acc_id:
                m_t = round(np.random.uniform(10, 400), 2)
                t_f = random_timestamp(start_date).strftime("%Y-%m-%d %H:%M:%S")
                
                transferencias.append(Transferencia(len(transferencias)+1, acc_id, destino, m_t, t_f))
                # Registramos los movimientos de la transferencia
                transacciones.append(Transaccion(len(transacciones)+1, acc_id, "TRANSFER_OUT", m_t, t_f))
                transacciones.append(Transaccion(len(transacciones)+1, destino, "TRANSFER_IN", m_t, t_f))

    return usuarios, cuentas, transacciones, transferencias

# =====================================================
# PERSISTENCIA EN TXT
# =====================================================

def save_to_txt(filename, data_list, header):
    path = os.path.join(DATA_PATH, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(header + "\n")
        for item in data_list:
            f.write(str(item) + "\n")

if __name__ == "__main__":
    ensure_data_folder()
    print("Generando objetos del sistema...")
    u, c, t, tr = generate_data()

    print("Guardando archivos TXT...")
    save_to_txt("usuarios.txt", u, "id|rol|nombres|apellidos|dui|pin|username")
    save_to_txt("cuentas.txt", c, "id|propietarioId|tipo|saldo|estado")
    save_to_txt("transacciones.txt", t, "id|cuentaId|tipo|monto|fecha")
    save_to_txt("transferencias.txt", tr, "id|cuentaOrigen|cuentaDestino|monto|fecha")

    print(f"Éxito. Se generaron {len(t)} transacciones en la carpeta /data.")