import shutil
from pathlib import Path

from git import Repo

from runner.repos import repos
from runner.infer import Infer
from runner.semgrep import Semgrep
from runner.codeql import CodeQL
from runner.reporter import Reporter

from runner.consts import PROJECTS_FOLDER

def prepare_project_git(project):
  dir = PROJECTS_FOLDER / project.name
  if dir.exists():
    return Repo(dir)
  else:
    print(f"[+] Repo not found, cloning {project.url} to {dir}")
    return Repo.clone_from(project.url, dir)

def run_through_projects(tool, report_folder, projects):
  reporter = Reporter(Path(report_folder))
  for project in projects:
    git_repo = prepare_project_git(project)
    root = PROJECTS_FOLDER / project.name

    will_report = reporter.new_group(project.name, tool.name)
    if not will_report:
      print(f"[*] Analysis for {project.name} is skipped")
      print()
      continue
    for commit in project.commits:
      git_repo.git.checkout(commit)
      tool.set_cwd(root, project.sourcefiles)
      # cleanup before the tools are run
      shutil.rmtree(tool.cwd / "infer-out", ignore_errors=True)
      shutil.rmtree(tool.cwd / "semgrep", ignore_errors=True)
      shutil.rmtree(tool.cwd / "codeql", ignore_errors=True)
      shutil.rmtree(tool.cwd / "codeqldb", ignore_errors=True)
      report = tool.run(project)
      if report:
        reporter.add_report(commit, report)
    reporter.finalize_report()

def generate_tool(name):
  if name == "infer":
    print("[+] using infer is unstable after rewriting")
    return Infer()
  elif name == "semgrep":
    return Semgrep()
  elif name == "codeql":
    return CodeQL()
  return None

if __name__ == "__main__":
  import argparse

  parser = argparse.ArgumentParser(description="Run analysis tool on projects")

  subparsers = parser.add_subparsers(
    title="commands", dest="command", help="Available commands")

  analyze = subparsers.add_parser("analyze")

  analyze.add_argument("--tool", choices=["codeql", "semgrep", "infer"],
                       help="Analysis tool to use", required=True)

  analyze.add_argument("--project", help="Comma-separated list of projects to analyze", required=True)

  analyze.add_argument("--report", help="Report output folder", required=True)

  args = parser.parse_args()

  if args.command == 'analyze':
    tool = generate_tool(args.tool)
    projects = args.project.split(",")
    try:
      run_through_projects(tool, args.report, filter(lambda r: r.name in projects, repos))
    except Exception as e:
      print(e)
      pass
