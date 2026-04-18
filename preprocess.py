"""
Generate app_data.json, raw_manifest.json, and spans_data.json for the
hypothesis viewer app.  Re-run whenever raw/ changes or source splits change.
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))

output = {"labels": None, "documents": {}}
# doc_text_spans[filename] = (text, spans_list) — kept in memory for spans_data
doc_raw = {}

for split in ["train.json", "dev.json", "test.json"]:
    with open(os.path.join(BASE, split)) as f:
        data = json.load(f)

    if output["labels"] is None:
        output["labels"] = data["labels"]

    for doc in data["documents"]:
        annotations = doc["annotation_sets"][0]["annotations"]
        output["documents"][doc["file_name"]] = {
            nda_id: ann["choice"] for nda_id, ann in annotations.items()
        }
        doc_raw[doc["file_name"]] = (doc["text"], doc["spans"])

with open(os.path.join(BASE, "app_data.json"), "w") as f:
    json.dump(output, f, separators=(",", ":"))
print(f"Wrote {len(output['documents'])} documents to app_data.json")

# raw_manifest.json — files present in raw/ that exist in the dataset
raw_dir = os.path.join(BASE, "raw")
raw_files = []
if os.path.isdir(raw_dir):
    raw_files = sorted(
        f for f in os.listdir(raw_dir)
        if not f.startswith(".") and f in output["documents"]
    )

with open(os.path.join(BASE, "raw_manifest.json"), "w") as f:
    json.dump(raw_files, f)
print(f"Wrote {len(raw_files)} entries to raw_manifest.json")

# spans_data.json — resolved span texts for manifest docs only (keeps payload small)
# Format: { filename: { nda_id: ["span text", ...] } }
spans_data = {}
for fname in raw_files:
    if fname not in doc_raw:
        continue
    text, doc_spans = doc_raw[fname]
    annotations = output["documents"][fname]
    # We need original span indices — reload from the split data
    # (output["documents"] only has choices; re-derive from doc_raw is not possible
    #  without the original span index list, so we re-read from splits below)

# Re-read splits to get span indices for manifest docs
manifest_set = set(raw_files)
for split in ["train.json", "dev.json", "test.json"]:
    with open(os.path.join(BASE, split)) as f:
        data = json.load(f)
    for doc in data["documents"]:
        if doc["file_name"] not in manifest_set:
            continue
        text = doc["text"]
        doc_spans = doc["spans"]
        entry = {}
        for nda_id, ann in doc["annotation_sets"][0]["annotations"].items():
            resolved = [text[doc_spans[si][0]:doc_spans[si][1]] for si in ann["spans"]]
            if resolved:
                entry[nda_id] = resolved
        spans_data[doc["file_name"]] = entry

with open(os.path.join(BASE, "spans_data.json"), "w") as f:
    json.dump(spans_data, f, separators=(",", ":"))
print(f"Wrote spans_data.json for {len(spans_data)} manifest documents")
