import tarfile

class Reporter:
  def __init__(self, storage):
    self.storage = storage

  def new_group(self, name, tag):
    self.tag = tag
    self.name = name
    filename = f"{name}_{tag}.tar.gz"
    filepath = self.storage / filename

    if filepath.exists():
      print(f"Found existing report file {filepath}")
      print(">> Overwrite (y/n)", end=' ')
      answer = input()
      if answer != "y":
        return False
    self.tar = tarfile.open(filepath, 'w:gz')
    return True

  def add_report(self, commit, path):
    if path.is_dir():
      for f in path.glob("*.sarif"):
        name = f"{self.name}_{commit}_{f.stem}_{self.tag}.json"
        self.tar.add(file, arcname=name)
        print(f">> added report {name}")
    else:
      name = f"{self.name}_{commit}_{self.tag}.json"
      self.tar.add(file, arcname=name)
      print(f">> added report {name}")

  def finalize_report(self):
    self.tar.close()
