import json

def fetch_ids(results_file):
    ids = set()
    with open(results_file, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line.strip())
            if "_id" in obj:
                ids.add(obj["_id"])
    return ids

def filter_records(input_file, ids):
    filtered = []
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line.strip())
            if obj.get("_id") in ids:
                filtered.append(obj)
    return filtered

def main():
    # Chemin vers le fichier de résultats à utiliser
    results_file = "./results/rq4-prompt/claude-3-5-sonnet-20241022_baseline.jsonl"
    ids = fetch_ids(results_file)

    # Fichiers d'entrée
    test_file = "./dataset/CoderEval/CoderEval_feedback_test.jsonl"
    train_file = "./dataset/CoderEval/CoderEval_feedback.jsonl"

    # Filtrer les records
    test_filtered = filter_records(test_file, ids)
    train_filtered = filter_records(train_file, ids)

    # Sauvegarder les nouveaux fichiers
    with open("./dataset/CoderEval/CoderEval_feedback_test_filtered.jsonl", "w", encoding="utf-8") as f:
        for obj in test_filtered:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")

    with open("./dataset/CoderEval/CoderEval_feedback_filtered.jsonl", "w", encoding="utf-8") as f:
        for obj in train_filtered:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()