class Tool:
  __slots__ = ['attributes', 'cwd']

  def __init__(self, cwd):
    self.cwd = cwd
    self.attributes = {}

  def prepare(self, args):
    pass

  def build(self, args):
    pass

  def report_file(self):
    return None

  def set(self, key, value):
    self.attributes[key] = value
