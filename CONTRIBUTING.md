# Contributing translations

## Fixing or improving a translation

1. Open the file of your language (for example `fr.json`) and edit the text.
2. Send a pull request. A check runs automatically; please fix any errors it reports.

You can do all of this in the GitHub web editor.

## Adding a new language

1. Copy `en.json` to a new file named with the language code (`nl.json`, `pl.json`, `zh-TW.json`, ...).
2. Translate the texts. You do not have to translate everything at once: keys you leave out are shown in English.
3. Send a pull request.

## The format

Each file is a JSON object of key → text. The keys are the same in all files; only `en.json` defines them.
`context.json` tells you on which screen each text appears.

Some texts change with a number. They are objects of plural forms:

```json
"trips_day_count": {
  "one": "%1$d trip",
  "other": "%1$d trips"
}
```

Use the plural forms of your language (`zero`, `one`, `two`, `few`, `many`, `other`; `other` is required).
Languages without plural forms, such as Japanese and Korean, use only `other`.

## Rules

- **Keep the placeholders** `%1$s`, `%2$d`, ... exactly as they are. You may move them within the sentence.
  `%1$s` is replaced by text (a name, a value with its unit) and `%1$d` by a number.
- **Do not translate** the app name *CarReplotter*, protocol and product names (OBD2, ELM327, BLE, CAN, ISO 15765-4,
  Google Drive, ...) or unit symbols (km/h, mph, °C, kPa, ...).
- `\n` is a line break.
- Keep texts short where they are labels or buttons; the screen of a phone is narrow.
- Use the words that drivers in your language actually use (for example for *RPM*, *throttle*, *coolant temp*).

## Glossary

| English | Meaning in the app |
| --- | --- |
| adapter | An OBD2 (ELM327-compatible) adapter plugged into the car |
| trip | One recording from start to stop |
| meter | The dashboard screen with gauges |
| hard acceleration / hard braking | A sudden change in speed |
| sharp turn | High lateral G while driving fast |
| impact | A shock detected by the phone's accelerometer (a bump, a curb, ...) |
| break | A stop in the middle of a trip (a rest, a traffic jam) |
| mini window | The picture-in-picture window shown while recording |

## Checking locally

```bash
python3 check.py
```
