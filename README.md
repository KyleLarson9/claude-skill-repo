# larson-claude-plugins

A [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin **marketplace** for
data reading, quality, validation, and verification workflows.

## Install

Add the marketplace, then install a plugin from it:

```
/plugin marketplace add KyleLarson9/claude-skill-repo
/plugin install read_data@larson-claude-plugins
```

## Repo layout

```
.
├── pyproject.toml        # uv project (package = false) + ruff/pytest config
├── Makefile              # install / lint / format / test / validate
├── .claude-plugin/
│   └── marketplace.json  # marketplace manifest (added in a later change)
├── plugins/
│   └── <name>/           # one directory per plugin
└── tests/                # scaffold + plugin tests
```

## Contributing a plugin

1. Create `plugins/<name>/` with the plugin's skills and a `.claude-plugin/plugin.json`.
2. Register it in `.claude-plugin/marketplace.json`.
3. Run `make lint test validate` and open a PR — CI runs lint + test on every PR to `main`.

## Local development

```
make install    # uv sync --dev
make lint       # ruff check + ruff format --check
make format     # ruff check --fix + ruff format
make test       # uv run pytest
make validate   # claude plugin validate .
make help       # list targets
```
