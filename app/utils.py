import json


def prepare_answer(data_from_db: dict):
    answer = {
        "dataset": list(data_from_db.values()),
        "labels": list(data_from_db.keys())
    }
    return json.dumps(answer)
