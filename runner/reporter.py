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
      print("Found existing report file", filepath)
      print("Please manually keep the file or move")
      print("append to tar.gz is unsupported by Python")
      print("Ctrl+C to exit")
      print("Press any key to continue, overwrite")
      input()
    self.tar = tarfile.open(filepath, 'w:gz')

  def add_report(self, commit, file):
    name = f"{self.name}_{commit}_{self.tag}.json"
    self.tar.add(file, arcname=name)
    print("add report", name)

  def finalize_report(self):
    self.tar.close()
