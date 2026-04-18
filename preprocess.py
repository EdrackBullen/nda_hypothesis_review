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

# Generate raw_manifest.json — list of filenames present in raw/ that also
# exist in the dataset.  Re-run this script whenever raw/ changes.
raw_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
raw_files = []
if os.path.isdir(raw_dir):
    raw_files = sorted(
        f for f in os.listdir(raw_dir)
        if not f.startswith(".") and f in output["documents"]
    )

manifest_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw_manifest.json")
with open(manifest_path, "w") as f:
    json.dump(raw_files, f)

print(f"Wrote {len(raw_files)} entries to raw_manifest.json")
