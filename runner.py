import shutil
from pathlib import Path

from git import Repo

from runner.repos import repos
from runner.infer import Infer
from runner.semgrep import Semgrep
from runner.reporter import Reporter

def prepare_project_git(project):
  dir = Path("projects") / project.name
  if dir.exists():
    return Repo(dir)
  else:
    print(f"Repo not found, cloning {repo.url} to {dir}")
    return Repo.clone_from(repo.url, dir)

def run_through_projects(tool, projects):
  reporter = Reporter(Path('reports'))
  for project in projects:
    git_repo = prepare_project_git(project)
    root = Path('projects') / project.name

    reporter.new_group(project.name, tool.name)
    for commit in project.commits:
      git_repo.git.checkout(commit)
      tool.set_cwd(root, project.sourcefiles)
      report = tool.run(project)
      print('we have report at', report)
      if report:
        reporter.add_report(commit, report)
    reporter.finalize_report()

def generate_tool(name):
  if name == "infer":
    return Infer()
  elif name == "semgrep":
    return Semgrep()
  return None

if __name__ == "__main__":
  import argparse

  parser = argparse.ArgumentParser(description="Run analysis tool on projects")

  subparsers = parser.add_subparsers(
    title="commands", dest="command", help="Available commands")

  analyze = subparsers.add_parser("analyze")

  analyze.add_argument("--tool", choices=["semgrep", "infer"], help="Analysis tool to use", required=True)

  analyze.add_argument("--project", help="Comma-separated list of projects to analyze", required=True)

  args = parser.parse_args()

  if args.command == 'analyze':
    tool = generate_tool(args.tool)
    projects = args.project.split(",")
    run_through_projects(tool, filter(lambda r: r.name in projects, repos))
