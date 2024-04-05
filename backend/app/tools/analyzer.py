import re
import sys
from enum import Enum

import pandas as pd


class DataType(Enum):
    EMAIL = "email"
    PHONE = "phone"
    RUT = "rut"
    HASH = "hash"
    STRING = "string"


def is_email(value: str) -> bool:
    regex = re.compile(r"^[\w\-\.]+\@([\w\-]+\.)+[\w\-]{2,4}$")
    if regex.match(value):
        return True
    return False


def is_phone(value: str) -> bool:
    cell_regex = re.compile(r"(\+?56)?(\s*)9(\s*)?[98765432](\d{3})(\s*)?(\d{4})")
    landline_regex = re.compile(
        r"(\+?56)?(\s*)?(2|\d{2})(\s*)?[98765432](\d{3})(\s*)(\d{4})"
    )
    if cell_regex.match(value) or landline_regex.match(value):
        return True
    return False


def is_rut(value: str) -> bool:
    regex = re.compile(r"([1-9]{1,3})(\.?\d{3})*[\-\s]?([\dkK])")
    if regex.match(value):
        return True
    return False


def is_hash(value: str) -> bool:
    # SHA512, SHA251, SHA1 & MD5
    regex = re.compile(
        r"([0-9a-f]{128})|([0-9a-f]{64})|([0-9a-f]{40})|([0-9a-f]{32})", re.IGNORECASE
    )
    if regex.match(value):
        return True
    return False


def identify_data_type(sample: pd.DataFrame) -> tuple[DataType, dict[DataType, list]]:
    sorted_data: dict[DataType, list[str]] = {
        DataType.EMAIL: [],
        DataType.PHONE: [],
        DataType.RUT: [],
        DataType.HASH: [],
        DataType.STRING: [],
    }
    results = {
        DataType.EMAIL: 0,
        DataType.PHONE: 0,
        DataType.RUT: 0,
        DataType.HASH: 0,
        DataType.STRING: 0,
    }

    for value in sample:
        try:
            if is_email(value):
                sorted_data[DataType.EMAIL].append(value)
                results[DataType.EMAIL] += 1
            elif is_phone(value):
                sorted_data[DataType.PHONE].append(value)
                results[DataType.PHONE] += 1
            elif is_rut(value):
                sorted_data[DataType.RUT].append(value)
                results[DataType.RUT] += 1
            elif is_hash(value):
                sorted_data[DataType.HASH].append(value)
                results[DataType.HASH] += 1
            else:
                sorted_data[DataType.STRING].append(value)
                results[DataType.STRING] += 1
        except TypeError:  # nan values
            continue
            # print(f"ERROR: {value} of type: {type(value)} is not string")

    return max(results, key=results.get), sorted_data  # type: ignore


def main():
    # 0. Separarlo por mi cuenta y dps pasarselo a Pandas
    # 1. Pasar datos a un DataFrame de Pandas
    df = pd.read_table(
        sys.argv[1],
        engine="python",
        dtype=str,
        header=None,
        names=["col1", "col2", "col3"],
        delimiter=r"\:{1}",
        usecols=range(2),
    )
    # print(df.head())
    # print(df.iloc[1])
    # print(df.columns)
    # 2. Analizar cada columna (ver los 1eros 100 o 1000)
    # sample = df.sample(frac=0.1)
    sample = df
    total_rows = len(sample)
    for col in range(len(df.columns)):
        #   2a. Identificar más o menos que tipo de dato contiene
        #   2b. La mayoría gana
        data_type, results = identify_data_type(sample.iloc[:, col])
        print(f"Column {col} -> {data_type}")
        for dtype in DataType:
            n_r = len(results[dtype])
            print(f"{dtype} : {n_r} ({'{:.2f}'.format(100 * n_r / total_rows)}%)")
        if col == 0:
            print(f"{DataType.STRING}: {results[DataType.STRING]}")
        if col == 1:
            # print(f"{DataType.PHONE}: {results[DataType.PHONE][:15]}")
            print(f"{DataType.HASH}: {results[DataType.HASH][:15]}")
    print("----------")
    ids = df.iloc[:, 1]
    ids.name = "col2"
    print(type(ids))
    # df[ids.isin(ids[ids.duplicated()])].sort_values('0')
    print(ids.head())
    # print(df.groupby("col2").nunique().head())
    print(df.groupby("col2").nunique().sort_values(by=["col1"]))
    # pd.concat(g for _, g in ids.groupby("col2") if len(g) > 1).head()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage:\n\tpython analyzer.py <data-file>")
    else:
        main()
