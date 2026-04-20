# agent-skills

Multi-runtime agent workflow plugins for Claude Code and Codex.

This repository renders one source set into four self-contained plugins:

| Runtime | Adapter | Plugin path |
|---------|---------|-------------|
| Claude Code | GitHub | `plugins/claude/epic-workflow-github/` |
| Claude Code | tkt | `plugins/claude/epic-workflow-tkt/` |
| Codex | GitHub | `plugins/codex/epic-workflow-github/` |
| Codex | tkt | `plugins/codex/epic-workflow-tkt/` |

Each plugin includes seven skills:

- `adversarial-code-review`
- `adversarial-design-review`
- `epic-brainstorming`
- `epic-decomposition`
- `subtask-planning`
- `team-execution`
- `epic-completion`

Claude plugins also include teammate agent definitions for `implementer-standard`, `implementer-complex`, and `spec-reviewer`.

## Marketplaces

Claude Code marketplace:

```text
.claude-plugin/marketplace.json
```

Codex marketplace:

```text
.agents/plugins/marketplace.json
```

Claude Code:

```bash
/plugin marketplace add wi-adam/agent-skills
/plugin install epic-workflow-github@wi-adam-skills
```

Codex:

```bash
codex marketplace add wi-adam/agent-skills
```

Install Codex plugins through the Codex plugin manager after adding the marketplace.

## Rendering

`tools/ai-sync/` is the source of truth:

- `operations.yaml` defines typed operations, validators, and formatter contracts.
- `adapters/*.yaml` map operations to GitHub or tkt argv recipes and text formatters.
- `runtimes/*.yaml` define Claude and Codex runtime behavior.
- `registry.yaml` defines plugins, skills, and durable workflow rules.
- `templates/` contains the Jinja2 source templates.

Regenerate outputs:

```bash
cd tools/ai-sync
uv sync
uv run python scripts/render.py
uv run python scripts/render.py --check
```

For local Codex skill development without installing a plugin:

```bash
cd tools/ai-sync
uv run python scripts/install_codex.py --adapter github
```

## Cross-Model Review

Verified locally on 2026-04-20:

- Claude Code can invoke Codex through `codex mcp-server`, exposing `codex` and `codex-reply`.
- Codex can invoke Claude through `claude mcp serve`, exposing `Agent`.

Codex plugin-bundled MCP activation is not assumed yet. Generated Codex adversarial review skills include an explicit setup requirement and stop path if `Agent` is unavailable.

## tkt Adapter

Verified locally on 2026-04-20 with `~/go/bin/tkt` reporting `tkt dev`.

The generated adapter expects `tkt` on `PATH`. On this machine, add `~/go/bin` to `PATH` before running generated tkt skills.

The verified workflow maps review publication to:

- create tickets with `tkt create <title> --description <body text>`
- append review bodies with `tkt add-note <id> <body text>`
- mark review-ready work with `tkt edit <id> --status needs_testing`
- close tickets with `tkt edit <id> --status closed`

## Development Notes

Generated files contain a notice near the top. Edit YAML data or templates, then rerender; do not hand-edit generated plugin output.

Consumer projects capture raw workflow notes in `.agent-skills/retro-notes.md`. Promote durable upstream rules by updating `tools/ai-sync/registry.yaml` in this repository and rerendering.
