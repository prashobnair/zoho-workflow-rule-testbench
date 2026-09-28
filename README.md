# zoho-workflow-rule-testbench (moved)

This project moved to [zoho-implementation-toolkit](https://github.com/prashobnair/zoho-implementation-toolkit) as the `workflow` module. Its full commit history was preserved there.

It simulates workflow rules against a record before anyone configures the real CRM — decisions traced, cycles and missing owners flagged.

## Use it now

```sh
pip install https://github.com/prashobnair/zoho-implementation-toolkit/releases/download/v0.1.0/zohokit-0.1.0-py3-none-any.whl
```

or

```sh
uv tool install git+https://github.com/prashobnair/zoho-implementation-toolkit@v0.1.0
```

The old `python cli.py rules.json` is now:

```sh
zohokit workflow simulate rules.json [--strict]
```

`--strict` exits 2 when the rules are not ready. Reports render with `--format json|table|markdown|html` and `--out`.

## Links

- Module guide: https://prashobnair.github.io/zoho-implementation-toolkit/modules/workflow/
- What changed versus this repo: https://prashobnair.github.io/zoho-implementation-toolkit/legacy-parity/
- Source: https://github.com/prashobnair/zoho-implementation-toolkit/tree/main/src/zohokit/modules/workflow

This repository is archived and read-only.
