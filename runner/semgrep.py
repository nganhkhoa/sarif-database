import subprocess
from pathlib import Path

from runner.tool import Tool

# can be opengrep or semgrep
# depends on the tool installed
SEMGREP_CMD = 'opengrep'

SEMGREP_RULES = [
    Path('semgrep-rules/c/')
]

class Semgrep(Tool):
  name = "semgrep"

  def run(self, project):
    """
    Iterate through a list of rules, output multiple reports
    TODO: Rework to output multiple reports
    """
    for rule in SEMGREP_RULES:
      base = [SEMGREP_CMD]
      base += ['scan', '--sarif', '-o', 'semgrep/report.sarif', '-f', rule.absolute()]
      subprocess.run([*base, '.'], cwd=self.cwd)

      report = self.cwd / 'semgrep/report.sarif'
      print(report)
      if not report.exists():
        return None
      return report
