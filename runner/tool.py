class Tool:
  __slots__ = ['attributes', 'cwd', 'name']

  def __init__(self):
    self.cwd = None
    self.attributes = {}

  def set_cwd(self, root, sourcefiles):
    """
    root is the whole path to project
    sourcefiles is the folder inside project
    where every build commands is executed
    """
    self.cwd = root / sourcefiles

  def invoke(self, command, **kargs):
    subprocess.run(command, cwd=self.cwd)

  def set(self, key, value):
    self.attributes[key] = value
