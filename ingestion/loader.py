from pathlib import Path

import pandas as pd


SUPPORTED_EXTENSIONS = {
    ".csv",
    ".xlsx",
    ".json",
    ".jsonl",
    ".parquet",
}


def load_dataset(file):
    """
    Load a supported dataset and return it as a Pandas DataFrame.
    """

    filename = file.name

    extension = Path(filename).suffix.lower()

    if extension == ".csv":
        df = pd.read_csv(file)

    elif extension == ".xlsx":
        df = pd.read_excel(file)

    elif extension == ".json":
        df = load_json(file)

    elif extension == ".jsonl":
        df = pd.read_json(file, lines=True)

    elif extension == ".parquet":
        df = pd.read_parquet(file)

    else:
        raise ValueError(
            f"Unsupported file format: {extension}"
        )

    return df


def load_json(file):
    """
    Load a JSON file and convert it into a DataFrame.
    """

    data = file.getvalue()

    import json

    data = json.loads(data)

    if isinstance(data, list):
        return pd.json_normalize(data)

    if isinstance(data, dict):

        for value in data.values():

            if isinstance(value, list):
                return pd.json_normalize(value)

        return pd.json_normalize(data)

    raise ValueError(
        "The JSON structure could not be converted into a table."
    )