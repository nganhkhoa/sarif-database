from pathlib import Path

PROJECTS_FOLDER = Path("projects")

BUILD_FOLDER = '_build'

# can be opengrep or semgrep
# depends on the tool installed
SEMGREP_CMD = 'opengrep'

SEMGREP_RULES = [
    ("0xdea", Path('semgrep-rules/c/')),
]

CODEQL_PACKS = [
    'oob', 'uaf'
]
