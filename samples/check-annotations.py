#!/usr/bin/env python3
"""Check JSON Structure Characteristics annotations against the extension meta-schema.

The JSON Structure SDK validators check a schema document against Core and the
extensions they know about, but they ignore annotation keywords contributed by an
add-in they do not implement. This script closes that gap for the Characteristics
extension: it reads ``characteristics-v0.json``, derives the keyword set and the
value types from the add-ins listed under ``$offers``, and validates every
annotation found in a sample schema against those definitions.

The same gap exists for ``altenums`` from the Alternate Names extension, which
the samples use to carry per-symbol display labels and descriptions, so this
script checks the shape of that keyword too.

Usage:
    python check-annotations.py <meta-schema> <schema> [<schema> ...]
"""

import json
import re
import sys

ABSOLUTE_URI = re.compile(r"^[A-Za-z][A-Za-z0-9+.\-]*:")

# Maps the $extends target of an add-in to the schema nodes it applies to.
ANY_NODE = "*"
PROPERTY_NODE = "property"
EXTENDS_TARGETS = {
    "#/definitions/NoType": ANY_NODE,
    "#/definitions/Property": PROPERTY_NODE,
    "#/definitions/ObjectType": "object",
    "#/definitions/TupleType": "tuple",
    "#/definitions/ArrayType": "array",
    "#/definitions/MapType": "map",
    "#/definitions/SetType": "set",
    "#/definitions/ChoiceType": "choice",
}

# Section "The concepts Keyword" of the draft partitions the documented kind
# values into terms that denote a class and terms that denote a property.
CLASS_KINDS = {"rdfs-class", "owl-class"}
PROPERTY_KINDS = {
    "rdf-property",
    "owl-object-property",
    "owl-datatype-property",
    "dcterms-property",
}


class MetaSchema:
    """The Characteristics add-ins and value types, read from the meta-schema."""

    def __init__(self, doc):
        self.doc = doc
        self.keywords = {}
        offers = doc.get("$offers", {}).get("JSONStructureCharacteristics", [])
        if isinstance(offers, str):
            offers = [offers]
        for pointer in offers:
            addin = self.resolve(pointer)
            target = EXTENDS_TARGETS.get(addin.get("$extends"))
            if target is None:
                raise ValueError("unknown $extends target in " + pointer)
            for keyword, schema in addin.get("properties", {}).items():
                self.keywords.setdefault(keyword, {"targets": set(), "schema": schema})
                self.keywords[keyword]["targets"].add(target)

    def resolve(self, pointer):
        node = self.doc
        for token in pointer.lstrip("#").strip("/").split("/"):
            node = node[token.replace("~1", "/").replace("~0", "~")]
        return node

    def check(self, schema, value, path, errors):
        """Validate ``value`` against a value type drawn from the meta-schema."""
        declared = schema.get("type")

        if isinstance(declared, dict):
            self.check(self.resolve(declared["$ref"]), value, path, errors)
            return
        if isinstance(declared, list):
            branches = []
            for alternative in declared:
                collected = []
                if isinstance(alternative, str):
                    self.check({"type": alternative}, value, path, collected)
                else:
                    self.check(self.resolve(alternative["$ref"]), value, path, collected)
                if not collected:
                    return
                branches.append(collected)
            errors.append(f"{path}: matches none of the permitted forms")
            for branch in branches:
                errors.extend("    " + message for message in branch)
            return

        if declared == "object":
            if not isinstance(value, dict):
                errors.append(f"{path}: expected an object")
                return
            properties = schema.get("properties", {})
            for member in schema.get("required", []):
                if member not in value:
                    errors.append(f"{path}: missing required member '{member}'")
            if schema.get("additionalProperties") is False:
                for member in value:
                    if member not in properties:
                        errors.append(f"{path}: member '{member}' is not permitted")
            for member, member_schema in properties.items():
                if member in value:
                    self.check(member_schema, value[member], f"{path}/{member}", errors)
            if "if" in schema:
                condition = []
                self.check(schema["if"], value, path, condition)
                branch = schema.get("then") if not condition else schema.get("else")
                if branch is not None:
                    self.check(branch, value, path, errors)
            return

        if declared == "array":
            if not isinstance(value, list):
                errors.append(f"{path}: expected an array")
                return
            if len(value) < schema.get("minItems", 0):
                errors.append(f"{path}: expected at least {schema['minItems']} item(s)")
            if schema.get("uniqueItems") and len(value) != len({json.dumps(i) for i in value}):
                errors.append(f"{path}: items must be distinct")
            for index, item in enumerate(value):
                self.check(schema.get("items", {}), item, f"{path}[{index}]", errors)
            return

        if declared == "any":
            return

        if declared in ("string", "uri", "jsonpointer"):
            if not isinstance(value, str):
                errors.append(f"{path}: expected a string")
                return
            if declared == "uri" and not ABSOLUTE_URI.match(value):
                errors.append(f"{path}: expected an absolute URI, got '{value}'")
            if declared == "jsonpointer" and not value.startswith(("#/", "/")):
                errors.append(f"{path}: expected a JSON Pointer, got '{value}'")
        elif declared in ("int32", "int64", "integer"):
            if isinstance(value, bool) or not isinstance(value, int):
                errors.append(f"{path}: expected an integer")
                return
            if "minimum" in schema and value < schema["minimum"]:
                errors.append(f"{path}: expected at least {schema['minimum']}, got {value}")
        elif declared is not None:
            errors.append(f"{path}: unsupported meta-schema type '{declared}'")
            return

        if "const" in schema and value != schema["const"]:
            errors.append(f"{path}: expected '{schema['const']}', got '{value}'")
        if "enum" in schema and value not in schema["enum"]:
            errors.append(
                f"{path}: '{value}' is not one of "
                + ", ".join(repr(v) for v in schema["enum"])
            )


def check_concepts(node, path, errors):
    """Enforce the placement rules the meta-schema cannot express."""
    concepts = node.get("concepts")
    if not isinstance(concepts, list):
        return
    kinds = {entry.get("kind") for entry in concepts if isinstance(entry, dict)}
    if kinds & CLASS_KINDS and kinds & PROPERTY_KINDS:
        errors.append(
            f"{path}/concepts: an array must not combine a class kind with a property kind"
        )
    is_type_node = node.get("type") in ("object", "tuple") or isinstance(
        node.get("properties"), dict
    )
    if kinds & CLASS_KINDS and not is_type_node:
        errors.append(
            f"{path}/concepts: a class kind is only permitted on a type definition"
        )
    observed = node.get("observedProperty")
    if isinstance(observed, dict):
        references = {
            entry.get("reference") for entry in concepts if isinstance(entry, dict)
        }
        if observed.get("reference") in references:
            errors.append(
                f"{path}/concepts: repeats the URI already carried by observedProperty"
            )


def check_altenums(node, path, uses, errors):
    """Enforce the shape the Alternate Names extension requires of altenums."""
    altenums = node.get("altenums")
    if altenums is None:
        return
    if "JSONStructureAlternateNames" not in uses:
        errors.append(
            f"{path}/altenums: the document does not list "
            "'JSONStructureAlternateNames' in $uses"
        )
    if not isinstance(node.get("enum"), list):
        errors.append(f"{path}/altenums: only permitted on a schema that has an enum")
        return
    if not isinstance(altenums, dict):
        errors.append(f"{path}/altenums: expected an object")
        return
    symbols = [str(value) for value in node["enum"]]
    for purpose, mapping in altenums.items():
        where = f"{path}/altenums/{purpose}"
        if not isinstance(mapping, dict):
            errors.append(f"{where}: expected an object")
            continue
        missing = [symbol for symbol in symbols if symbol not in mapping]
        if missing:
            errors.append(f"{where}: no entry for " + ", ".join(repr(s) for s in missing))
        extra = [key for key in mapping if key not in symbols]
        if extra:
            errors.append(
                f"{where}: " + ", ".join(repr(k) for k in extra) + " is not an enum value"
            )
        for key, value in mapping.items():
            if not isinstance(value, str) or not value:
                errors.append(f"{where}/{key}: expected a non-empty string")


def walk(meta, node, path, in_property, uses, errors):
    if not isinstance(node, dict):
        return

    kinds = {ANY_NODE}
    if in_property:
        kinds.add(PROPERTY_NODE)
    if isinstance(node.get("type"), str):
        kinds.add(node["type"])

    for keyword, entry in meta.keywords.items():
        if keyword not in node:
            continue
        if not entry["targets"] & kinds:
            targets = ", ".join(sorted(entry["targets"]))
            errors.append(f"{path}/{keyword}: not permitted here, only on {targets}")
            continue
        meta.check(entry["schema"], node[keyword], f"{path}/{keyword}", errors)

    check_concepts(node, path, errors)
    check_altenums(node, path, uses, errors)

    for name, child in node.get("properties", {}).items():
        walk(meta, child, f"{path}/properties/{name}", True, uses, errors)
    for name, child in node.get("choices", {}).items():
        walk(meta, child, f"{path}/choices/{name}", True, uses, errors)
    for keyword in ("items", "values"):
        walk(meta, node.get(keyword), f"{path}/{keyword}", False, uses, errors)
    for name, child in node.get("definitions", {}).items():
        walk(meta, child, f"{path}/definitions/{name}", False, uses, errors)


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    with open(argv[1], encoding="utf-8") as handle:
        meta = MetaSchema(json.load(handle))

    failed = False
    for filename in argv[2:]:
        with open(filename, encoding="utf-8") as handle:
            document = json.load(handle)
        uses = document.get("$uses", [])
        if not isinstance(uses, list):
            uses = []
        errors = []
        walk(meta, document, "#", False, uses, errors)
        if errors:
            failed = True
            print(f"{filename}: annotations are invalid")
            for message in errors:
                print(f" - {message}")
        else:
            print(f"{filename}: annotations are valid")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
