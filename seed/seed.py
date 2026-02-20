import csv
import os
import numpy as np
from datetime import datetime, timedelta


#seed generado con IA

# =====================================================
# CONFIGURACIÓN GENERAL
# =====================================================

NUM_CLIENTES = 80
MAX_CUENTAS_POR_CLIENTE = 2
NUM_DIAS = 30
TRANSACCIONES_BASE = 8000

np.random.seed(42)

# =====================================================
# RUTA DINÁMICA A /data
# =====================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data")


def ensure_data_folder():
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)


# =====================================================
# UTILIDADES
# =====================================================

def random_dui():
    return f"{np.random.randint(10000000,99999999)}-{np.random.randint(0,9)}"


def random_name():
    nombres = [
        "Carlos","Ana","Luis","Maria","Jorge","Sofia","Ricardo",
        "Valeria","Daniel","Fernanda","Miguel","Camila"
    ]
    apellidos = [
        "Gomez","Lopez","Martinez","Hernandez","Perez",
        "Ramirez","Torres","Flores","Castro","Vargas"
    ]
    return np.random.choice(nombres), np.random.choice(apellidos)


def random_timestamp(start_date, nocturno=False):
    day_offset = np.random.randint(0, NUM_DIAS)
    random_day = start_date + timedelta(days=int(day_offset))

    if nocturno:
        hour = np.random.choice([21,22,23,0,1,2,3])
    else:
        hour = np.random.randint(6, 22)

    minute = np.random.randint(0, 60)
    second = np.random.randint(0, 60)

    return random_day.replace(hour=int(hour), minute=int(minute), second=int(second))


# =====================================================
# GENERAR USUARIOS
# =====================================================

def generate_users():
    users = []

    # Admin fijo
    users.append([1, "ADMIN", "Juan", "Perez", "00000000-0", "1234", "jp1"])

    user_id = 2

    for _ in range(NUM_CLIENTES):
        nombre, apellido = random_name()
        dui = random_dui()
        pin = str(np.random.randint(1000,9999))
        users.append([user_id, "CLIENTE", nombre, apellido, dui, pin, ""])
        user_id += 1

    with open(os.path.join(DATA_PATH, "usuarios.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id","rol","nombres","apellidos","dui","pin","username"])
        writer.writerows(users)

    return users


# =====================================================
# GENERAR CUENTAS
# =====================================================

def generate_accounts(users):
    accounts = []
    account_id = 1

    for user in users:
        if user[1] == "CLIENTE":
            num_cuentas = np.random.randint(1, MAX_CUENTAS_POR_CLIENTE+1)
            for _ in range(num_cuentas):
                tipo = np.random.choice(["AHORRO","CORRIENTE"])
                saldo = round(np.random.uniform(500, 5000), 2)
                estado = "ACTIVA"
                accounts.append([account_id, user[0], tipo, saldo, estado])
                account_id += 1

    with open(os.path.join(DATA_PATH, "cuentas.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["account_id","user_id","tipo","saldo","estado"])
        writer.writerows(accounts)

    return accounts


# =====================================================
# GENERAR TRANSACCIONES Y TRANSFERENCIAS
# =====================================================

def generate_transactions(accounts):
    transactions = []
    transfers = []

    transaction_id = 1
    transfer_id = 1

    start_date = datetime.now() - timedelta(days=NUM_DIAS)

    account_ids = [acc[0] for acc in accounts]

    # ------------------------------
    # TRANSACCIONES BASE
    # ------------------------------

    for _ in range(TRANSACCIONES_BASE):

        account = np.random.choice(account_ids)
        tipo = np.random.choice(["DEPOSITO","RETIRO"])
        monto = round(np.random.uniform(10,500),2)
        timestamp = random_timestamp(start_date)

        transactions.append([
            transaction_id,
            account,
            tipo,
            monto,
            timestamp.strftime("%Y-%m-%d %H:%M:%S")
        ])
        transaction_id += 1

        # Transferencias aleatorias (20%)
        if np.random.rand() < 0.2:
            destino = np.random.choice(account_ids)
            if destino != account:
                monto_t = round(np.random.uniform(10,400),2)
                ts = random_timestamp(start_date)

                transfers.append([
                    transfer_id,
                    account,
                    destino,
                    monto_t,
                    ts.strftime("%Y-%m-%d %H:%M:%S")
                ])

                # Salida
                transactions.append([
                    transaction_id,
                    account,
                    "TRANSFER_OUT",
                    monto_t,
                    ts.strftime("%Y-%m-%d %H:%M:%S")
                ])
                transaction_id += 1

                # Entrada
                transactions.append([
                    transaction_id,
                    destino,
                    "TRANSFER_IN",
                    monto_t,
                    ts.strftime("%Y-%m-%d %H:%M:%S")
                ])
                transaction_id += 1

                transfer_id += 1

    # =====================================================
    # ANOMALÍAS INTENCIONALES
    # =====================================================

    anomalous_account = account_ids[0]

    # 1️⃣ Z-SCORE EXTREMO
    extreme_day = start_date + timedelta(days=NUM_DIAS-1)
    transactions.append([
        transaction_id,
        anomalous_account,
        "DEPOSITO",
        20000,
        extreme_day.strftime("%Y-%m-%d 10:00:00")
    ])
    transaction_id += 1

    # 2️⃣ STRUCTURING (4 depósitos ≤ 50)
    struct_day = start_date + timedelta(days=NUM_DIAS-2)
    for amount in [40, 30, 25, 50]:
        transactions.append([
            transaction_id,
            anomalous_account,
            "DEPOSITO",
            amount,
            struct_day.strftime("%Y-%m-%d 12:00:00")
        ])
        transaction_id += 1

    # 3️⃣ ACTIVIDAD NOCTURNA EXCESIVA
    night_day = start_date + timedelta(days=NUM_DIAS-3)
    for hour in [21,22,23,0,1,2]:
        transactions.append([
            transaction_id,
            anomalous_account,
            "RETIRO",
            60,
            night_day.replace(hour=hour, minute=10, second=0).strftime("%Y-%m-%d %H:%M:%S")
        ])
        transaction_id += 1

    # ------------------------------
    # GUARDAR ARCHIVOS
    # ------------------------------

    with open(os.path.join(DATA_PATH, "transacciones.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["transaction_id","account_id","tipo","monto","timestamp"])
        writer.writerows(transactions)

    with open(os.path.join(DATA_PATH, "transferencias.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["transfer_id","from_account","to_account","monto","timestamp"])
        writer.writerows(transfers)


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":
    print("Generando seed del sistema bancario...")

    ensure_data_folder()
    users = generate_users()
    accounts = generate_accounts(users)
    generate_transactions(accounts)

    print("Seed generado correctamente en la carpeta /data")