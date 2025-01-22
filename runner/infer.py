import subprocess
from enum import Enum

from runner.tool import Tool

class InferMode(Enum):
  COMPILE = 1
  RUN = 2

class Infer(Tool):
  integration = None

  def run(self, mode, rest):
    base = ['infer']

    if mode == InferMode.COMPILE:
      base += ['compile']
    elif mode == InferMode.RUN:
      base += ['run', '--sarif', '--bufferoverrun', '--pulse']

    if "integration" in self.attributes:
      base += ['--force-integration', self.attributes["integration"]]

    subprocess.run([*base, '--', *rest], cwd=self.cwd)

  def prepare(self, command):
    self.run(InferMode.COMPILE, command)

  def build(self, command):
    self.run(InferMode.RUN, command)

  def report_file(self):
    report = self.cwd / "infer-out" / "report.sarif"
    if not report.exists():
      return None
    return report
