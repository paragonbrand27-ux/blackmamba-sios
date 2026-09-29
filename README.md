# BlackMamba SIOS

BlackMamba Special Intelligence Operating System (SIOS) is a benevolence-driven OS with single-host binding, a unified token lifecycle, and security architecture by ABUL SYSTEMS.

## Chooser prototype

The `chooser/` package is a local-first, transparent recommendation engine inspired by the open-source [Microsoft Recommenders](https://github.com/recommenders-team/recommenders) project. It combines content similarity, collaborative signals, diversity re-ranking, and explainable decision records.

This prototype does **not** silently censor content. It exposes configurable policy hooks, records why an item was ranked, and lets the caller decide how to handle safety, legal, or privacy constraints.

```bash
python -m pytest
python examples/chooser_demo.py
```

See [`chooser/README.md`](chooser/README.md) for the design and extension points.
