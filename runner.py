import shutil
from pathlib import Path

from git import Repo

from runner.repos import repos
from runner.infer import Infer
from runner.reporter import Reporter

reporter = Reporter(Path('reports'))

root = Path('projects')
for repo in repos:
  dir = root / repo.name

  if dir.exists():
    git = Repo(dir)
  else:
    print(f"Repo not found, cloning {repo.url} to {dir}")
    git = Repo.clone_from(repo.url, dir)

  tool = Infer(dir)
  reporter.new_group(repo.name, "infer")

  for commit in repo.commits:
    # force fresh build
    if (dir / "build").exists():
      shutil.rmtree(dir / "build")

    git.git.checkout(commit)
    repo.run(tool)
    report = tool.report_file()
    if report:
      reporter.add_report(commit, report)
  reporter.finalize_report()
