import json
from pathlib import Path
from datetime import datetime


def save_result(result, output_path):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    result["timestamp"] = datetime.now().isoformat()

    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(result) + "\n")