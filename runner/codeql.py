import shutil
import subprocess
from pathlib import Path

from runner.tool import Tool
from runner.consts import BUILD_FOLDER, CODEQL_PACKS

class CodeQL(Tool):
  name = "codeql"

  def run(self, project):
    # we only need the project built for infer
    project.build(self)

    report = self.cwd / "codeql"
    if not report.exists():
      return None
    return report

  def invoke(self, command, **kargs):
    cmake = kargs.get("cmake", False)
    make = kargs.get("make", False)
    script = kargs.get("script", False)

    base = ['codeql']

    if script:
      subprocess.run(command, cwd=self.cwd)
    if make:
      # do a clean first
      subprocess.run([*command, 'clean'], cwd=self.cwd)
      if not (self.cwd / "codeqldb").exists():
        # init codeql database if not generated from cmake
        subprocess.run([*base, 'database', 'create', 'codeqldb',
                        '--language=cpp', '--source-root=.'],
                        # f'command="{' '.join(command)}"'],
                       cwd=self.cwd, check=True)
      else:
        # run make
        subprocess.run([*command], cwd=self.cwd)
        # subprocess.run([*base, 'database', 'finalize', 'codeqldb'],
        #                cwd=self.cwd, check=True)

      (self.cwd / "codeql").mkdir(exist_ok=True)
      for pack in CODEQL_PACKS:
        subprocess.run([*base,
                        'database', 'analyze', 'codeqldb',
                        str((Path('CodeQL-Queries') / pack).absolute()),
                        '--format=sarifv2.1.0',
                        '--no-sarif-minify',
                        f'--output=codeql/{pack}.sarif'],
                       cwd=self.cwd, check=True)
    if cmake:
      # we delete the build folder first
      shutil.rmtree(self.cwd / BUILD_FOLDER, ignore_errors=True)
      shutil.rmtree(self.cwd / "_codeql", ignore_errors=True)
      shutil.rmtree(self.cwd / "_codeql_build_dir", ignore_errors=True)
      subprocess.run(command, cwd=self.cwd, check=True)
      # base += ['database', 'create', 'codeqldb', '--language=cpp', '--source-root=.']
      # subprocess.run([*base], cwd=self.cwd, check=True)
