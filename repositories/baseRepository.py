import csv
import os

class BaseRepository:

    def __init__(self, file_path, fieldnames):
        self.file_path = file_path
        self.fieldnames = fieldnames
        self.datos = []
        self.cargar_datos()
    
    def cargar_datos(self):
        """
        Carga los datos desde archivo TXT.
        Si no existe, lo crea con encabezado.
        """

        try:
            if not os.path.exists(self.file_path):
                with open(self.file_path, "w", newline="") as file:
                    writer = csv.DictWriter(
                        file,
                        fieldnames=self.fieldnames,
                        delimiter="|"
                    )
                    writer.writeheader()
                self.datos = []
                return

            with open(self.file_path, "r") as file:
                reader = csv.DictReader(file, delimiter="|")

                # Validar estructura clara de columnas
                if reader.fieldnames != self.fieldnames:
                    raise ValueError("Estructura de columnas incorrecta")

                self.datos = list(reader)

        except Exception as e:
            print(f"Error al cargar datos: {e}")
            self.datos = []

    def guardar_datos(self):
        """
        Guarda inmediatamente en archivo TXT.
        Garantiza persistencia inmediata.
        """

        try:
            with open(self.file_path, "w", newline="") as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=self.fieldnames,
                    delimiter="|"
                )
                writer.writeheader()
                writer.writerows(self.datos)

        except Exception as e:
            print(f"Error al guardar datos: {e}")

    def agregar(self, nuevo_registro):
        """
        Agrega registro y guarda inmediatamente.
        """

        try:
            if set(nuevo_registro.keys()) != set(self.fieldnames):
                raise ValueError("Estructura inválida")

            self.datos.append(nuevo_registro)
            self.guardar_datos()  # Persistencia inmediata

        except Exception as e:
            print(f"Error al agregar: {e}")
            
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
            print(f"Error al actualizar: {e}")