"""
Generate app_data.json for the hypothesis viewer app.
Extracts only the fields needed: file_name, labels, and per-document choices.
"""
import json
import os

output = {"labels": None, "documents": {}}

for split in ["train.json", "dev.json", "test.json"]:
    path = os.path.join(os.path.dirname(__file__), split)
    with open(path) as f:
        data = json.load(f)

    if output["labels"] is None:
        output["labels"] = data["labels"]

    for doc in data["documents"]:
        annotations = doc["annotation_sets"][0]["annotations"]
        output["documents"][doc["file_name"]] = {
            nda_id: ann["choice"] for nda_id, ann in annotations.items()
        }

out_path = os.path.join(os.path.dirname(__file__), "app_data.json")
with open(out_path, "w") as f:
    json.dump(output, f, separators=(",", ":"))

print(f"Wrote {len(output['documents'])} documents to app_data.json")
