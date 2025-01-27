# SARIF Dataset Generator

Generates C/C++ SARIF reports from static analyzers.

Supports Infer, and Opengrep.

Projects should be automatically cloned using git.

Opengrep rules should be manually downloaded, and modify the list of rules inside `runner/semgrep.py`.

This project uses `uv` for python management.

```
uv run runner.py analyze --tool infer --project a,b,c
uv run runner.py analyze --tool semgrep --project a,b,c
```

## Infer

Infer requires the project to be built using Infer's clang compiler.

> A few of the projects not compatible with Infer, so there are a few setup performed manually (at this stage). Check the source code.

## Semgrep/Opengrep

Opengrep is an open-source fork of Semgrep, these terms can be used interchangably. This tool only needs the path to the project and a path to list of rules applied.
