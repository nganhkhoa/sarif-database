import subprocess
from pathlib import Path

from runner.tool import Tool
from runner.consts import SEMGREP_CMD, SEMGREP_RULES

class Semgrep(Tool):
  name = "semgrep"

  def run(self, project):
    """
    Iterate through a list of rules, output multiple reports
    TODO: Rework to output multiple reports
    """
    for (rule_name, rule) in SEMGREP_RULES:
      base = [SEMGREP_CMD]
      base += ['scan', '--sarif',
               '-o', f'semgrep/{rule_name}.sarif',
               '-f', rule.absolute(),
               ]
      subprocess.run([*base, '.'], cwd=self.cwd)

      report = self.cwd / 'semgrep'
      if not report.exists():
        return None
      return report
