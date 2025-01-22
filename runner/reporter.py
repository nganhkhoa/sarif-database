import tarfile

class Reporter:
  def __init__(self, storage):
    self.storage = storage

  def new_group(self, name, tag):
    self.tag = tag
    self.name = name
    filename = f"{name}_{tag}.tar.gz"
    filepath = self.storage / filename
    self.tar = tarfile.open(filepath, 'w:gz')

  def add_report(self, commit, file):
    name = f"{self.name}_{commit}_{self.tag}.json"
    self.tar.add(file, arcname=name)

  def finalize_report(self):
    self.tar.close()
