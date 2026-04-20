# Contributing

## Source Files

Edit the source data and templates under `tools/ai-sync/`:

- `registry.yaml` for plugin metadata, skill descriptions, and durable workflow rules
- `operations.yaml` for typed operation contracts
- `adapters/*.yaml` for backend-specific commands and formatter strings
- `runtimes/*.yaml` for runtime-specific setup and delegation behavior
- `templates/` for generated skill, agent, and manifest text

Do not hand-edit generated files under `plugins/`, `.claude-plugin/`, `.agents/plugins/`, or `docs/process/improvements.md`.

## Regenerate

```bash
cd tools/ai-sync
uv sync
uv run python scripts/render.py
uv run python scripts/render.py --check
```

`render.py` validates adapter coverage, argv placeholders, list iteration, formatter placeholders, JSON manifests, and built-in golden cases before writing output.

## Promoting Retro Notes

Consumer projects should write execution notes to `.agent-skills/retro-notes.md`.

To promote a durable rule:

1. Convert the note into a generic rule that is not tied to one codebase.
2. Add or update an entry in `tools/ai-sync/registry.yaml`.
3. Keep `source_retro` empty in the public registry unless the evidence is intended to be published.
4. Rerender and review the generated skills plus `docs/process/improvements.md`.

## Adapter Changes

Commands must stay as argv arrays. Do not introduce `sh -c`, shell escaping recipes, or single interpolated shell strings. If an operation cannot be expressed as direct argv, add a helper script with tests instead of hiding shell behavior in generated prose.

Every adapter must implement every operation in `operations.yaml`, and adapter-specific ticket IDs must be declared as `validators.ticket_id`.
