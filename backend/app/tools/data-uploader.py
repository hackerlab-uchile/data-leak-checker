import enum
import json
import os
import sys
from datetime import datetime
from hashlib import sha256

from core.database import get_db
from models.email_leaks import EmailLeak
from models.emails import Email
from models.phone_leaks import PhoneLeak
from models.phones import Phone
from models.rut_leaks import RutLeak
from models.ruts import Rut
from repositories.breach_repository import create_breach
from repositories.data_type_repository import get_data_type_by_name, save_breach_data
from repositories.email_repository import get_or_create
from schemas.breach_data import BreachDataCreate
from schemas.breaches import BreachCreate


def valid_file_type() -> bool:
    if len(sys.argv) < 2 or sys.argv[1].lower() not in ["upload", "json", "csv"]:
        return False
    return True


def valid_file_path() -> bool:
    if len(sys.argv) < 3 or not os.path.isfile(sys.argv[2]):
        return False
    return True


def valid_params() -> bool:
    if len(sys.argv) != 3:
        print("Usage:\npython data-uploader.py <file-type> <file-path>")
        return False
    if not valid_file_type() or not valid_file_path():
        return False
    return True


def display_data(data: dict):
    for c in data.keys():
        print(f"{c}: {data[c][:5]}")


def handle_csv_file(f_path: str):
    sep = input("Please enter columns separator: ")
    with open(f_path, "r") as file:
        all_rows = file.read().strip().split("\n")
    sample = all_rows[0].split(sep, maxsplit=1)
    n_cols = len(sample)
    print(f"{n_cols} columns have been detected.")
    print("Please enter the names of the columns in order:")
    columns: list[str] = []
    data = {}
    for i in range(n_cols):
        col_name = input(f"Column number {i+1}: ")
        columns.append(col_name)
        data[col_name] = []
    for row in all_rows:
        values = row.split(sep)
        for i, c in enumerate(columns):
            value = sha256(values[i].encode("UTF-8")).hexdigest()
            data[c].append(value)
    display_data(data)
    return data


def handle_json_file(f_path: str): ...


def valid_upload_file(data: dict) -> bool:
    breach = data.get("breach")
    error_msg = ""
    if breach is None:
        error_msg += "Invalid Upload File: Must have a 'breach' key\n"

    description = data.get("breach")
    if description is None:
        data["description"] = ""

    data_path = data.get("data_path")
    if data_path is None:
        error_msg += "Invalid Upload File: Must have a 'data_path' key\n"

    file_type = data.get("file_type")
    if file_type is None or file_type not in ["json", "csv"]:
        error_msg += "Invalid Upload File: Must have a 'file_type' key\n"

    if error_msg:
        print(error_msg)
    return error_msg == ""


def handle_upload_file(f_path: str):
    with open(f_path, "r") as file:
        upload_data = json.load(file)

    if valid_upload_file(upload_data):
        data_leak = handle_csv_file(upload_data["data_path"])
        # display_data(upload_data)
        display_data(data_leak)
        return upload_data, data_leak
    return None, None


def main() -> int:
    if not valid_params():
        return 1
    f_type = sys.argv[1].lower()
    f_path = sys.argv[2].lower()
    if f_type == "csv":
        handle_csv_file(f_path)
    elif f_type == "json":
        handle_json_file(f_path)
    elif f_type == "upload":
        upload_data, data_leak = handle_upload_file(f_path)
        if upload_data is None or data_leak is None:
            return 1
        # Obtenemos acceso a la db
        session = get_db().__next__()
        breach = upload_data["breach"]
        breach["date"] = datetime.strptime(breach["breach_date"], "%Y-%m-%d")
        breach_to_create = BreachCreate(**breach)
        print("breach_schema:", breach_to_create)
        # En estos momentos, tengo guardada la filtración así:
        # data_leak = { "column" : [...], "column" : [....] }
        # En total se deben guardar datos en estas tablas:
        # 1. Breach
        # 2. Breach Data (relaciona un Breach con la data filtrada)
        # 3. {Dato} (Email, Phone, Rut)
        # 4. {Dato Leak} (Relaciona un Dato con un breach y INFO ADICIONAL que lo acompaña)
        # 5. Password (hash: sha256)
        # ------
        # 1. Guardamos el Breach
        created_breach = create_breach(db=session, breach=breach_to_create)
        for col, items in data_leak.items():
            # 2. Guardamos la info encontrada con el breach (nombre de columnas)
            column_data_type = get_data_type_by_name(db=session, name=col)
            if column_data_type is None:
                print(f"Error: Column with name {col} is not a valid data type!")
                continue
            breach_data_to_create = {
                "breach_id": created_breach.id,
                "data_type_id": column_data_type.id,
            }
            created_breach_data = save_breach_data(db=session, **breach_data_to_create)
            # 3. Guardar {Dato}. Revisar si ya existe o no
            model = Email
            model_leak = EmailLeak
            leak_data_name = "email_id"
            match column_data_type.dtype:
                case "email":
                    pass
                case "phone":
                    model = Phone
                    model_leak = PhoneLeak
                    leak_data_name = "phone_id"
                case "rut":
                    model = Rut
                    model_leak = RutLeak
                    leak_data_name = "rut_id"
                case _:
                    continue
            for i, item in enumerate(items):
                if item == "":  # or no tiene forma de Email
                    continue
                # a. Check if already exists
                # a2. If doesnt exist -> save it
                # a3. else -> get it
                data = get_or_create(session, model, value=item)
                for other_data in data_leak.keys():
                    if other_data == col:
                        continue
                    column_data_type = get_data_type_by_name(
                        db=session, name=other_data
                    )
                    if column_data_type is None:
                        print(
                            f"Error: Column with name {other_data} is not a valid data type!"
                        )
                        continue
                    data_leak_created = get_or_create(
                        db=session,
                        model=model_leak,
                        breach_id=created_breach.id,
                        data_type_id=column_data_type.id,
                        **{leak_data_name: data.id},
                    )

        # TODO: Guardamos los nuevos datos en su tabla (ej. Email), (si es que no existen ya)
        # TODO: Guardamos la relación de los datos con el breaach (ej. EmailLeak)
        # TODO: Guardamos la relación de los datos con el breaach y con los datos que se encontró (ej. EmailLeak)
        # TODO: Guardamos el hash en contraseñas
        print(created_breach)
    return 0


if __name__ == "__main__":
    main()
