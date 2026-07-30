#!/usr/bin/env python3
"""Check JSON Structure Characteristics annotations against the extension meta-schema.

The JSON Structure SDK validators check a schema document against Core and the
extensions they know about, but they ignore annotation keywords contributed by an
add-in they do not implement. This script closes that gap for the Characteristics
extension: it reads ``characteristics-v0.json``, derives the keyword set and the
value types from the add-ins listed under ``$offers``, and validates every
annotation found in a sample schema against those definitions.

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


def walk(meta, node, path, in_property, errors):
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

    for name, child in node.get("properties", {}).items():
        walk(meta, child, f"{path}/properties/{name}", True, errors)
    for name, child in node.get("choices", {}).items():
        walk(meta, child, f"{path}/choices/{name}", True, errors)
    for keyword in ("items", "values"):
        walk(meta, node.get(keyword), f"{path}/{keyword}", False, errors)
    for name, child in node.get("definitions", {}).items():
        walk(meta, child, f"{path}/definitions/{name}", False, errors)


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
        errors = []
        walk(meta, document, "#", False, errors)
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
