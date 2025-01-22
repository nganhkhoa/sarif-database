import subprocess

from dataclasses import dataclass
from collections.abc import Callable

from runner.tool import Tool

@dataclass
class Repo:
  name: str
  url: str
  commits: list[str]
  runner: Callable[[Tool], None]

  def run(self, tool):
    self.runner(tool)

def cmake_runner(tool):
  """
  The default runner for CMake projects
  """
  tool.prepare(['cmake', '-B', 'build'])
  tool.build(['make', '-C', 'build', '-j8'])

def kbr5_runner(tool):
  tool.prepare([])

kbr5 = Repo(
  name = "kbr5",
  url = "https://github.com/krb5/krb5.git",
  commits = ['d864d74'],
  runner = kbr5_runner,
)

def libmpeg2_runner(tool):
  tool.prepare([])

libmpeg2 = Repo(
  name = "libmpeg2",
  url = "https://android.googlesource.com/platform/external/libmpeg2",
  commits = ['9fcdebe'],
  runner = libmpeg2_runner,
)

libavc = Repo(
  name = "libavc",
  url = "https://android.googlesource.com/platform/external/libavc",
  commits = ['9783b50', 'b2a61a1', '4900778', '992407f'],
  runner = cmake_runner,
)

def gpac_runner(tool):
  subprocess.run(['./configure'], cwd=tool.cwd)
  tool.build(['make', 'clean', '-j8'])
  tool.build(['make', '-j8'])

gpac = Repo(
  name = "gpac",
  url = "https://github.com/gpac/gpac.git",
  commits = set([
    "bb9ee4c", "a6b6408", "94cf5b1", "7e2cb01", "6f28c4c", "8f3088b", "cc95b16", "4c77303", "112767e", "a8bc2c8", "50a60b0", "fc9e290", "514a3af", "1b77837", "3ffe59c", "ebedc7a", "78f5269", "7e2e92f", "7edc40f", "89a80ca", "b6b6360", "ca1b48f", "7a6f636", "de7f3a8", "4925c40", "0b29a41", "b1042c3", "8db20cb", "be23476", "4607052", "d2de8b5", "49cb88a",
  ]),
  runner = gpac_runner,
)

"https://github.com/nothings/stb.git"
"https://github.com/Exiv2/exiv2.git"
"git://w1.fi/hostap.git"
"https://github.com/GNOME/libxml2.git"
"https://github.com/bytecodealliance/wasm-micro-runtime.git"

def p11_kit_runner(tool):
  tool.set("integration", "cmake")
  tool.prepare(['meson', 'setup', 'build'])
  tool.set("integration", "make")
  tool.build(['ninja', '-C', 'build', '-j8'])

p11_kit = Repo(
  name = "p11-kit",
  url = "https://github.com/p11-glue/p11-kit.git",
  commits = ["7fe7e5d"],
  runner = p11_kit_runner,
)

"https://github.com/espeak-ng/espeak-ng.git"
"https://github.com/lz4/lz4.git"
"https://github.com/mity/md4c.git"
"https://github.com/libimobiledevice/libplist.git"
"https://github.com/bfabiszewski/libmobi.git"
"https://github.com/libsndfile/libsndfile.git"
"https://github.com/mruby/mruby.git"
"https://github.com/SELinuxProject/selinux.git"
"https://github.com/LibRaw/LibRaw.git"
"https://github.com/uber/h3.git"
"https://github.com/samtools/htslib.git"
"https://github.com/kjdev/hoextdown.git"
"https://github.com/sleuthkit/sleuthkit.git"

assimp = Repo(
  name = "assimp",
  url = "https://github.com/assimp/assimp.git",
  commits = ["0422dff", "565539b", "2d44861"],
  runner = cmake_runner,
)

"https://github.com/facebook/zstd.git"
"https://github.com/hunspell/hunspell.git"
"https://github.com/AcademySoftwareFoundation/openexr.git"
"https://github.com/stefanberger/libtpms.git"
"https://github.com/irssi/irssi.git"
"https://github.com/harfbuzz/harfbuzz.git"


c_blosc = Repo(
  name = "c-blosc",
  url = "https://github.com/Blosc/c-blosc.git",
  commits = ["01df770", "41f3a2e"],
  runner = cmake_runner,
)

c_blosc2 = Repo(
  name = "c-blosc2",
  url = "https://github.com/Blosc/c-blocs2.git",
  commits = ["6fc4790", "aebf2b9", "81c2fcd", "4f6d42a", "81c2fcd", "cb15f1b", "38b23d5"],
  runner = cmake_runner,
)

json_c = Repo(
  name = "json-c",
  url = "https://github.com/json-c/json-c.git",
  commits = ["da76ee2"],
  runner = cmake_runner,
)

"https://github.com/nlohmann/json.git"

repos = [
  # libavc,
  # json_c,
  # assimp,
  # c_blosc,
  # c_blosc2,
  # p11_kit
  gpac,
]
