import subprocess
import shutil
from enum import Enum

from runner.tool import Tool

class Infer(Tool):
  name = "infer"

  def run(self, project):
    # we only need the project built for infer
    project.build()

    report = self.cwd / "infer-out" / "report.sarif"
    if not report.exists():
      return None
    return report

  def invoke(self, command, **kargs):
    kargs['cmake']
    kargs['make']
    kargs['script']

    base = ['infer']

    if "integration" in self.attributes:
      base += ['--force-integration', self.attributes["integration"]]

    if script:
      subprocess.run(command, cwd=self.cwd)
    if make:
      base += ['run', '--sarif', '--bufferoverrun', '--pulse']
      # do a clean first
      subprocess.run([*command, 'clean'], cwd=self.cwd)
      subprocess.run(command, cwd=self.cwd)
    if cmake:
      # we delete the build folder first
      # this would delete lz4 build folder
      shutil.rmtree(self.cwd / "_build", ignore_errors=True)
      base += ['compile']
      subprocess.run([*base, '--', *command], cwd=self.cwd)
