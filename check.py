#!/usr/bin/env python3
"""Checks the translation files: the app (*.json) and the website (site/*.json).

- every file is a JSON object of key -> text (or key -> {"one": ..., "other": ...} for plurals, app only)
- no keys that are not in en.json
- placeholders match en.json exactly: %1$s, %2$d, ... in the app; {privacy}, {email}, ... on the website
- website: the number of links (<a ...>) matches en.json (emphasis such as <strong> may differ)
- plurals have "other" (and use only zero/one/two/few/many/other)

Missing keys are allowed (the app shows English for them) and are listed as coverage.
Exit code 1 if there is an error.
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP_PLACEHOLDER = re.compile(r"%\d\$[sd]")
SITE_PLACEHOLDER = re.compile(r"\{[a-z_]+\}")
TAG = re.compile(r"<a[ >]")
QUANTITIES = {"zero", "one", "two", "few", "many", "other"}


PLACEHOLDER = APP_PLACEHOLDER


def placeholders(text):
    return sorted(PLACEHOLDER.findall(text))


def tags(text):
    return sorted(TAG.findall(text))


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def check(folder, site, errors):
    global PLACEHOLDER
    PLACEHOLDER = SITE_PLACEHOLDER if site else APP_PLACEHOLDER
    prefix = "site/" if site else ""
    en = load(os.path.join(folder, "en.json"))
    for path in sorted(glob.glob(os.path.join(folder, "*.json"))):
        name = prefix + os.path.basename(path)
        if os.path.basename(path) in ("en.json", "context.json"):
            continue
        try:
            data = load(path)
        except json.JSONDecodeError as e:
            errors.append(f"{name}: invalid JSON: {e}")
            continue
        if not isinstance(data, dict):
            errors.append(f"{name}: must be a JSON object")
            continue
        for key, value in data.items():
            where = f"{name}: {key}"
            if key not in en:
                errors.append(f"{where}: not in en.json")
                continue
            source = en[key]
            if isinstance(source, dict):
                if not isinstance(value, dict) or "other" not in value:
                    errors.append(f'{where}: must be an object with at least "other"')
                    continue
                for quantity, text in value.items():
                    if quantity not in QUANTITIES:
                        errors.append(f"{where}: unknown quantity {quantity!r}")
                    elif not isinstance(text, str) or not text.strip():
                        errors.append(f"{where}.{quantity}: must be non-empty text")
                    elif placeholders(text) != placeholders(source["other"]):
                        errors.append(f"{where}.{quantity}: placeholders {placeholders(text)} must match {placeholders(source['other'])}")
            else:
                if not isinstance(value, str) or (not value.strip() and source.strip()):
                    errors.append(f"{where}: must be non-empty text")
                elif placeholders(value) != placeholders(source):
                    errors.append(f"{where}: placeholders {placeholders(value)} must match {placeholders(source)}")
                elif site and tags(value) != tags(source):
                    errors.append(f"{where}: links ({len(tags(value))}) must match en.json ({len(tags(source))})")
        missing = [k for k in en if k not in data]
        print(f"{name}: {len(en) - len(missing)}/{len(en)} translated" + (f" (missing: {', '.join(missing[:5])}{' ...' if len(missing) > 5 else ''})" if missing else ""))


def main():
    errors = []
    check(HERE, False, errors)
    check(os.path.join(HERE, "site"), True, errors)
    for e in errors:
        print("ERROR " + e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
