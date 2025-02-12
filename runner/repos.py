import subprocess

from dataclasses import dataclass
from collections.abc import Callable

from runner import utils
from runner.tool import Tool
from runner.consts import BUILD_FOLDER


@dataclass
class Repo:
  name: str
  url: str
  commits: list[str]

  """
  this function describe how to build a project
  we provide Tool as an argument, so that any
  Tool can inject/modify the command
  """
  build: Callable[[Tool], None]

  sourcefiles: str = ''

def cmake_runner(tool):
  """
  The default runner for CMake projects
  """
  tool.invoke(['cmake', '-B', BUILD_FOLDER], cmake=True)
  tool.invoke(['make', '-C', BUILD_FOLDER, '-j16'], make=True)

def make_runner(tool):
  tool.invoke(['make', '-j16'], make=True)

def kbr5_runner(tool):
  subprocess.run(['automake'], cwd=tool.cwd / "src")
  tool.build(['make', '-C', 'src', '-j16'])

krb5 = Repo(
  name = "krb5",
  url = "https://github.com/krb5/krb5.git",
  commits = ['d864d74'],
  build = kbr5_runner,
)

libmpeg2 = Repo(
  name = "libmpeg2",
  url = "https://android.googlesource.com/platform/external/libmpeg2",
  commits = ['9fcdebe'],
  build = cmake_runner,
)

libavc = Repo(
  name = "libavc",
  url = "https://android.googlesource.com/platform/external/libavc",
  commits = ['9783b50', 'b2a61a1', '4900778', '992407f'],
  build = cmake_runner,
)

def gpac_runner(tool):
  tool.invoke(['./configure'], script=True)
  tool.invoke(['make', '-j8'], make=True)

gpac = Repo(
  name = "gpac",
  url = "https://github.com/gpac/gpac.git",
  commits = set([
    "bb9ee4c", "a6b6408", "94cf5b1", "7e2cb01", "6f28c4c", "8f3088b", "cc95b16", "4c77303", "112767e", "a8bc2c8", "50a60b0", "fc9e290", "514a3af", "1b77837", "3ffe59c", "ebedc7a", "78f5269", "7e2e92f", "7edc40f", "89a80ca", "b6b6360", "ca1b48f", "7a6f636", "de7f3a8", "4925c40", "0b29a41", "b1042c3", "8db20cb", "be23476", "4607052", "d2de8b5", "49cb88a",
  ]),
  build = gpac_runner,
)

"https://github.com/nothings/stb.git"

exiv2 = Repo(
  name = "exiv2",
  url = "https://github.com/Exiv2/exiv2.git",
  commits = ["e4adf38", "5ed9fb4"],
  build = cmake_runner,
)

def hostap_runner(tool):
  """
  Some how Infer does not add CONFIG_ECC to its build args
  modify the code to always include the CONFIG_ECC code segment
  """
  utils.modify_file(tool.cwd / "../src/crypto/crypto_openssl.c",
                    "#ifdef CONFIG_ECC", "#if 1")
  # this file inside wpa_supplicant/
  utils.modify_file(tool.cwd / "config_ssid.h",
                    "#ifdef CONFIG_IEEE80211W", "#if 1")
  tool.invoke(['make', '-j16'], make=True)
  # restore project state, should be .. because
  # tool.cwd is either in hostapd/ or wpa_supplicant/
  subprocess.run(['git', 'checkout', '..'], cwd=tool.cwd)

hostap = Repo(
  name = "hostap",
  url = "git://w1.fi/hostap.git",
  commits = ["a6ed414", "703c2b6", "8112131"],
  build = hostap_runner,
  sourcefiles = 'hostapd',
)

wpa_supplicant = Repo(
  name = "wpa",
  url = "git://w1.fi/hostap.git",
  commits = ["a6ed414", "703c2b6", "8112131"],
  build = hostap_runner,
  sourcefiles = 'wpa_supplicant',
)

libxml2 = Repo(
  name = "libxml2",
  url = "https://github.com/GNOME/libxml2.git",
  commits = ["b167c73", "ca2bfec", "5f4ec41", "9ef2a9a", "20f5c73", "7fbd454"],
  build = cmake_runner,
)

wasm_micro_runtime = Repo(
  name = "wasm-micro-runtime",
  url = "https://github.com/bytecodealliance/wasm-micro-runtime.git",
  commits = ["b3f728c", "06df58f"],
  build = cmake_runner,
)

def meson_runner(tool):
  tool.set("integration", "cmake")
  tool.invoke(['meson', 'setup', BUILD_FOLDER], cmake=True)
  tool.set("integration", "make")
  tool.invoke(['ninja', '-C', BUILD_FOLDER, '-j8'], make=True)

p11_kit = Repo(
  name = "p11-kit",
  url = "https://github.com/p11-glue/p11-kit.git",
  commits = ["7fe7e5d"],
  build = meson_runner,
)

def espeak_ng_runner(tool):
  tool.invoke(["./autogen.sh"], script=True)
  tool.invoke(["./configure"], script=True)
  # documentation
  tool.invoke(["make", "-j16", "src/espeak-ng", "src/espeak-ng"], make=True)

espeak_ng = Repo(
  name = "espeak-ng",
  url = "https://github.com/espeak-ng/espeak-ng.git",
  commits = ["0a713d5"],
  build = espeak_ng_runner,
)

def lz4_runner(tool):
  tool.invoke(['cmake', '-B', BUILD_FOLDER, 'build/cmake/'], cmake=True)
  tool.invoke(['make', '-C', BUILD_FOLDER, '-j8'], make=True)

lz4 = Repo(
  name = "lz4",
  url = "https://github.com/lz4/lz4.git",
  commits = ["7654a5a", "9d20cd5"],
  build = make_runner,
)

md4c = Repo(
  name = "md4c",
  url = "https://github.com/mity/md4c.git",
  commits = ["3478ec6"],
  build = cmake_runner,
)

def libplist_runner(tool):
  tool.invoke(["./autogen.sh"], script=True)
  tool.invoke(["./configure"], script=True)
  tool.invoke(["make", "-j16"], make=True)

libplist = Repo(
  name = "libplist",
  url = "https://github.com/libimobiledevice/libplist.git",
  commits = ["491a3ac"],
  build = libplist_runner,
)

libmobi = Repo(
  name = "libmobi",
  url = "https://github.com/bfabiszewski/libmobi.git",
  commits = ["1297ee0"],
  build = cmake_runner,
)

libsndfile = Repo(
  name = "libsndfile",
  url = "https://github.com/libsndfile/libsndfile.git",
  commits = ["2b4cc4b", "fe49327", "932aead", "4819cad", "b706e62"],
  build = cmake_runner,
)

mruby = Repo(
  name = "mruby",
  url = "https://github.com/mruby/mruby.git",
  commits = set(["0ed3fcf", "d1f1b4e", "af5acf3", "55b5261", "8aec568", "4c196db", "bdc244e", "bf5bbf0", "b4168c9", "c30e6eb"]),
  build = make_runner,
)

def selinux_runner(tool):
  tool.invoke(['make', '-j16', 'SUBDIRS=\'libsepol libselinux\''], make=True)

selinux = Repo(
  name = "selinux",
  url = "https://github.com/SELinuxProject/selinux.git",
  commits = ["5e6e516", "e9072e7"],
  build = selinux_runner,
)

def libraw_runner(tool):
  tool.invoke(['./mkdist.sh'], script=True)
  tool.invoke(['./configure'], script=True)
  tool.invoke(['make', '-j16'], make=True)

libraw = Repo(
  name = "LibRaw",
  url = "https://github.com/LibRaw/LibRaw.git",
  commits = set(["eaf63bf", "8382fac", "8382fac", "52b2fc5", "ae2dc58", "adcb898", "5eeffd5", "8382fac", "8382fac", "21f5e5b", "6fbba37"]),
  build = libraw_runner,
)

h3 = Repo(
  name = "h3",
  url = "https://github.com/uber/h3.git",
  commits = ["f581626"],
  build = cmake_runner,
)

htslib = Repo(
  name = "htslib",
  url = "https://github.com/samtools/htslib.git",
  commits = ["dd6f0b7"],
  build = make_runner,
)

hoextdown = Repo(
  name = "hoextdown",
  url = "https://github.com/kjdev/hoextdown.git",
  commits = ["933f9da"],
  build = make_runner,
)

def sleuthkit_runner(tool):
  tool.invoke(['./bootstrap'], script=True)
  tool.invoke(['./configure'], script=True)
  tool.invoke(['make', '-j16'], make=True)

sleuthkit = Repo(
  name = "sleuthkit",
  url = "https://github.com/sleuthkit/sleuthkit.git",
  commits = ["34f995d", "38a13f9", "82d254b", "d9b19e1"],
  build = sleuthkit_runner,
)

assimp = Repo(
  name = "assimp",
  url = "https://github.com/assimp/assimp.git",
  commits = ["0422dff", "565539b", "2d44861"],
  build = cmake_runner,
)

zstd = Repo(
  name = "zstd",
  url = "https://github.com/facebook/zstd.git",
  commits = ["9ad7ea4", "0a96d00", "3cac061", "2fabd37", "6f40571", "d68aa19"],
  build = make_runner,
)

def hunspell_runner(tool):
  tool.invoke(['autoreconf', '-vfi'], script=True)
  tool.invoke(['./configure'], script=True)
  tool.invoke(['make', '-j16'], make=True)

hunspell = Repo(
  name = "hunspell",
  url = "https://github.com/hunspell/hunspell.git",
  commits = set(["6291cac", "74b08bf", "82b9212", "6291cac", "6291cac", "ddec95b", "74b08bf", "1c1f34f", "74b08bf", "473241e", "6291cac"]),
  build = hunspell_runner,
)

def openexr_runner(tool):
  """
  This project has 2 errors when running with Infer,
  1. undefined uintptr_t in src/bin/exrcheck/main.cpp
  2. Wrong define COMP_EXTRA, fix in
    src/test/OpenEXRCoreTest/CMakeLists.txt
  Currently, fix and stash push manually, then the
  following commands will perform the fix each checkout
  """
  subprocess.run(["git", "stash", "pop"], cwd=tool.cwd)
  # just redefine uintptr_t
  utils.modify_file(tool.cwd / "src/bin/exrcheck/main.cpp",
                    "uintptr_t", "unsigned long")
  # do not wrap the string with "", the value inside cmake is still wrapped
  utils.modify_file(tool.cwd / "src/test/OpenEXRCoreTest/CMakeLists.txt",
                    "COMP_EXTRA=\"\\\\\"${OPENEXR_VERSION_RELEASE_TYPE}\\\\\"\"",
                    "COMP_EXTRA=\"\\\\${OPENEXR_VERSION_RELEASE_TYPE}\\\\\"")
  cmake_runner(tool)
  subprocess.run(["git", "checkout", "src/"], cwd=tool.cwd)

openexr = Repo(
  name = "openexr",
  url = "https://github.com/AcademySoftwareFoundation/openexr.git",
  commits = ["115e42e", "672c77d", "4854db9", "7c40603", "e2919b5"],
  build = openexr_runner,
)

def libtpms_runner(tool):
  tool.invoke(['./autogen.sh'], script=True)
  tool.invoke(['./configure'], script=True)
  tool.invoke(['make', '-j16'], make=True)

libtpms = Repo(
  name = "libtpms",
  url = "https://github.com/stefanberger/libtpms.git",
  commits = ["e563166"],
  build = libtpms_runner,
)

irssi = Repo(
  name = "irssi",
  url = "https://github.com/irssi/irssi.git",
  commits = ["afcb483", "b472570"],
  build = meson_runner,
)

harfbuzz = Repo(
  name = "harfbuzz",
  url = "https://github.com/harfbuzz/harfbuzz.git",
  commits = ["3194963", "fb795dc", "918193e"],
  build = cmake_runner,
)

c_blosc = Repo(
  name = "c-blosc",
  url = "https://github.com/Blosc/c-blosc.git",
  commits = ["01df770", "41f3a2e"],
  build = cmake_runner,
)

c_blosc2 = Repo(
  name = "c-blosc2",
  url = "https://github.com/Blosc/c-blocs2.git",
  commits = ["6fc4790", "aebf2b9", "81c2fcd", "4f6d42a", "81c2fcd", "cb15f1b", "38b23d5"],
  build = cmake_runner,
)

json_c = Repo(
  name = "json-c",
  url = "https://github.com/json-c/json-c.git",
  commits = ["da76ee2"],
  build = cmake_runner,
)

"https://github.com/nlohmann/json.git"

wasm3_harness = Repo(
  name = "wasm3-harness",
  url = "https://github.com/wasm3/wasm3.git",
  commits = set(["970849d", "bc32ee0", "4f0b769", "4f0b769", "355285d", "0124fd5", "970849d", "4f0b769", "bc32ee0"]),
  build = cmake_runner,
)

repos = [
  # these are cmake/meson projects
  libavc,
  json_c,
  assimp,
  c_blosc,
  c_blosc2,
  p11_kit,
  gpac,
  libxml2,
  lz4,
  libmpeg2,
  wasm_micro_runtime,
  md4c,
  harfbuzz,
  libmobi,
  libsndfile,
  h3,
  openexr,
  exiv2,

  # cannot build with infer
  irssi,
  krb5,

  # error during analysis
  sleuthkit,

  # undefined uvwasi_* although linked together
  wasm3_harness,

  # takes a long time
  mruby,

  # these are makefile projects
  espeak_ng,
  libplist,
  selinux,
  libraw,
  htslib,
  hoextdown,
  zstd,
  hunspell,
  libtpms,
  hostap,
  wpa_supplicant,

  # these projects are headers only?
  # infer cannot run with headers only?
  # stb,
  # json,
]
