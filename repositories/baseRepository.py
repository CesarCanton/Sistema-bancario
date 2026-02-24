import csv
import os


class BaseRepository:

    def __init__(self, file_path, fieldnames):
        self.file_path = file_path
        self.fieldnames = fieldnames
        self.datos = []

        # Crear carpeta si no existe
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        self.cargar_datos()

    # ==========================================
    # CARGA DE ARCHIVO
    # ==========================================

    def cargar_datos(self):

        try:
            if not os.path.exists(self.file_path):

                with open(self.file_path, "w", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(
                        file,
                        fieldnames=self.fieldnames,
                        delimiter="|"
                    )
                    writer.writeheader()

                self.datos = []
                return

            with open(self.file_path, "r", encoding="utf-8") as file:

                reader = csv.DictReader(file, delimiter="|")

                # Validación REAL de estructura
                if reader.fieldnames != self.fieldnames:
                    raise ValueError(
                        f"Estructura incorrecta en {self.file_path}\n"
                        f"Esperado: {self.fieldnames}\n"
                        f"Encontrado: {reader.fieldnames}"
                    )

                self.datos = list(reader)

        except Exception as e:
            print(f"[ERROR] cargar_datos -> {e}")
            self.datos = []

    # ==========================================
    # GUARDADO
    # ==========================================

    def guardar_datos(self):

        try:
            with open(self.file_path, "w", newline="", encoding="utf-8") as file:

                writer = csv.DictWriter(
                    file,
                    fieldnames=self.fieldnames,
                    delimiter="|"
                )

                writer.writeheader()
                writer.writerows(self.datos)

        except Exception as e:
            print(f"[ERROR] guardar_datos -> {e}")

    # ==========================================
    # AGREGAR
    # ==========================================

    def agregar(self, nuevo_registro):

        try:
            # Validar orden exacto de columnas
            if list(nuevo_registro.keys()) != self.fieldnames:
                raise ValueError("Estructura inválida del registro")

            self.datos.append(nuevo_registro)
            self.guardar_datos()

        except Exception as e:
            print(f"[ERROR] agregar -> {e}")

    # ==========================================
    # ACTUALIZAR
    # ==========================================

    def actualizar(self, campo_id, valor_id, nuevos_datos):

        actualizado = False

        try:
            for registro in self.datos:
                if registro[campo_id] == str(valor_id):
                    registro.update(nuevos_datos)
                    actualizado = True
                    break

            if actualizado:
                self.guardar_datos()
            else:
                print("Registro no encontrado")

        except Exception as e:
            print(f"[ERROR] actualizar -> {e}")

    # ==========================================
    # ELIMINAR
    # ==========================================

    def eliminar(self, campo_id, valor_id):

        try:
            self.datos = [
                r for r in self.datos
                if r[campo_id] != str(valor_id)
            ]

            self.guardar_datos()

        except Exception as e:
            print(f"[ERROR] eliminar -> {e}")

    # ==========================================
    # UTILIDADES
    # ==========================================

    def buscar(self, campo, valor):
        return next((r for r in self.datos if r[campo] == str(valor)), None)

    def filtrar(self, campo, valor):
        return [r for r in self.datos if r[campo] == str(valor)]

    def obtener_todos(self):
        return self.datos