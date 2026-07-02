import json
from pathlib import Path

CATALOG_PATH = Path(__file__).parent / "catalog_data.json"


def load_catalog():
    """
    Load SHL catalog JSON file
    """
    with open(CATALOG_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


if __name__ == "__main__":
    catalog = load_catalog()
    print(f"Loaded {len(catalog)} assessments")