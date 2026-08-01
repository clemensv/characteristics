import json
import pathlib
import sys

CLASS_KINDS = {"rdfs-class", "owl-class"}
PROP_KINDS = {"rdf-property", "owl-object-property", "owl-datatype-property", "dcterms-property"}

root = pathlib.Path(__file__).parent
problems = []


def is_type_node(node):
    return node.get("type") in ("object", "tuple") or isinstance(node.get("properties"), dict)


def walk(node, path):
    if not isinstance(node, dict):
        return
    concepts = node.get("concepts")
    if isinstance(concepts, list):
        kinds = {c.get("kind") for c in concepts if isinstance(c, dict)}
        if kinds & CLASS_KINDS and kinds & PROP_KINDS:
            problems.append(f"{path}: mixes class and property kinds {sorted(kinds)}")
        if kinds & CLASS_KINDS and not is_type_node(node):
            problems.append(f"{path}: class kind on a non-type node {sorted(kinds)}")
        op = node.get("observedProperty")
        if isinstance(op, dict):
            refs = {c.get("reference") for c in concepts if isinstance(c, dict)}
            if op.get("reference") in refs:
                problems.append(f"{path}: observedProperty URI repeated in concepts")
    for key in ("properties", "definitions"):
        for name, sub in (node.get(key) or {}).items():
            walk(sub, f"{path}/{key}/{name}")
    for key in ("items", "values", "choices"):
        sub = node.get(key)
        if isinstance(sub, dict):
            walk(sub, f"{path}/{key}")


for schema_file in sorted(root.rglob("schema.struct.json")):
    doc = json.loads(schema_file.read_text(encoding="utf-8"))
    walk(doc, schema_file.relative_to(root).parent.as_posix())

if problems:
    print("\n".join(problems))
    sys.exit(1)
print("kind placement OK")
