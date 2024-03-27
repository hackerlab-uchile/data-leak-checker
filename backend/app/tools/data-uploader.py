import json
import os
import sys
from datetime import datetime
from hashlib import sha256

from core.database import get_db
from repositories.breach_repository import create_breach
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
        display_data(upload_data)
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
        date = datetime.strptime("2024-03-22", "%Y-%m-%d")
        breach_data = {
            "name": upload_data["breach"],
            "description": upload_data["description"],
            "breach_date": date,
            "confirmed": True,
            "is_sensitive": True,
        }
        breach_to_create = BreachCreate(**breach_data)
        print("breach_schema:", breach_to_create)
        # created_breach = create_breach(**breach_to_create.model_dump())
        session = get_db().__next__()
        created_breach = create_breach(db=session, breach=breach_to_create)
        print(created_breach)
    return 0


if __name__ == "__main__":
    main()
