import os
import json

def extract_ids(filepath):
    ids = set()
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line.strip())
            # Support both _id (CoderEval) and task_id (HumanEval)
            if "_id" in obj:
                ids.add(obj["_id"])
            elif "task_id" in obj:
                ids.add(obj["task_id"])
    return ids

def main(directory):
    jsonl_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".jsonl")]
    file_ids = {f: extract_ids(f) for f in jsonl_files}

    all_ids = set.union(*file_ids.values())

    for f, ids in file_ids.items():
        missing = all_ids - ids
        if missing:
            print(f"Dans {f}, il manque {len(missing)} ids : {missing}")
        else:
            print(f"Tous les ids sont présents dans {f}")

if __name__ == "__main__":
    # Exemple d'utilisation : vérifier tous les fichiers jsonl dans dataset/CoderEval/
    main("./results/rq4-prompt")