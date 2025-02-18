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
  # commits = set([
  #   "bb9ee4c", "a6b6408", "94cf5b1", "7e2cb01", "6f28c4c", "8f3088b", "cc95b16", "4c77303", "112767e", "a8bc2c8", "50a60b0", "fc9e290", "514a3af", "1b77837", "3ffe59c", "ebedc7a", "78f5269", "7e2e92f", "7edc40f", "89a80ca", "b6b6360", "ca1b48f", "7a6f636", "de7f3a8", "4925c40", "0b29a41", "b1042c3", "8db20cb", "be23476", "4607052", "d2de8b5", "49cb88a",
  # ]),

  # customized for CodeQL
  commits = ["895ac12", "a8bc2c8", "13dad7d"],
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

def libxml2_runner(tool):
  """
  The default runner for CMake projects
  """
  tool.invoke(['cmake', '-B', BUILD_FOLDER], cmake=True)
  tool.invoke(['make', '-C', BUILD_FOLDER, '-j16', 'LibXml2'], make=True)

libxml2 = Repo(
  name = "libxml2",
  url = "https://github.com/GNOME/libxml2.git",
  # commits = ["b167c73", "ca2bfec", "5f4ec41", "9ef2a9a", "20f5c73", "7fbd454"],

  # confirmed vuln commits
  commits = set([
    "14c62e0dd337208c6a5de45a90312eab0a6cf4e4",
    "14c62e0dd337208c6a5de45a90312eab0a6cf4e4",
    "14c62e0dd337208c6a5de45a90312eab0a6cf4e4",
    "14c62e0dd337208c6a5de45a90312eab0a6cf4e4",
    "14c62e0dd337208c6a5de45a90312eab0a6cf4e4",
    "14c62e0dd337208c6a5de45a90312eab0a6cf4e4",
    "14c62e0dd337208c6a5de45a90312eab0a6cf4e4",
    "14c62e0dd337208c6a5de45a90312eab0a6cf4e4",
    "f0a703dac85ad9398f208d3237ca19c483368834",
    "42322eba820022eaebb9b6e7c083a8aadddea286",
    "e115194e6fc7f86e2e47224b758653f43501e6fe",
    "0e4a11bb30e85d21bce665b1df42f29529d1e0cd",
    "0e4a11bb30e85d21bce665b1df42f29529d1e0cd",
    "7fbd454d9f70f0f0c0a0c27a7d541fed4d038c2a", # already have
    "00c2f549e483b4669d51b44d9af2bb1b26f58472",
    "0533daf5d2747860a2aa636466bcf02972c2dfba", # huh?
    "5f664ab2cfcf5b817924e303ca9e6699487b2af9",
    "7f04e297318b1b908cec20711f74f75625afed7f",
    "05c147c3ef2029019f4bca856a1319b14e2a0fa8",
    "05c147c3ef2029019f4bca856a1319b14e2a0fa8",
    "c63900fbc1a7c20eb872996ae700f264ba6d75ef",
    "8afd321abd2f75cf795f679b54333237b364d4d9",
    "9ef2a9abf357f747c2fb03841b7f479cc0dfd3ef", # already have
    # "9ef2a9abf357f747c2fb03841b7f479cc0dfd3ef",
    # "9ef2a9abf357f747c2fb03841b7f479cc0dfd3ef",
    "36ea881b9d92166568b1d107181a05f673fd4ab1",
    "b167c7314497b6cb0d9a587a31874ae0d273ffaa", # already have
    "f0fd1b67fc883a24cdd039abb3d4fe4696104d72", # huh?
    # "00ed736eecf93aeab49089abb06e0e5fc0e7e091", # libxml2class.py not found
    "f6a9541fb85c1ffdee1399ad2c0a54faaebf9f38",
    "f6a9541fb85c1ffdee1399ad2c0a54faaebf9f38",
    "d025cfbb4bf05785d970e268e46d674580a8a686",
    "0e201722e497f278f028c5c3916e293e2f77b5a4", # huh?
    # "0e201722e497f278f028c5c3916e293e2f77b5a4",
    "20f5c73457df065df21bf25aa081a0a4cd028046", # already have
    "b76d81dab3869f16a5c3506d9902526dff583b3e",
    "5cb4b05c57b945ed524da51d271f2209b2190a31", # huh?
    # "5cb4b05c57b945ed524da51d271f2209b2190a31",
    # "5cb4b05c57b945ed524da51d271f2209b2190a31",
    "ecfbcc8a52b4376de0653ba4138493faeb6c7fa4",
    "6c128fd58a0e4641c23a345d413672494622db1b", # huh?
    "fa48187304039f8792d8e19129df7d64422e7f69",
    "ec7be50662ec17104355e7357f5067d43c47b207", # huh?
    # "84bab955fe01c50e64382481de67259047d917a9", # cannot build
  ]),
  build = libxml2_runner,
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

def c_blosc2_runner(tool):
  """
  The default runner for CMake projects
  """
  tool.invoke(['cmake', '-B', BUILD_FOLDER, '-DCMAKE_C_CFLAGS=-lz', '-DCMAKE_EXE_LINKER_FLAGS=-lz -lm'], cmake=True)
  tool.invoke(['make', '-C', BUILD_FOLDER, '-j16'], make=True)


c_blosc2 = Repo(
  name = "c-blosc2",
  url = "https://github.com/Blosc/c-blocs2.git",
  # commits = ["6fc4790", "aebf2b9", "81c2fcd", "4f6d42a", "81c2fcd", "cb15f1b", "38b23d5"],

  # confirmed vuln commits
  commits = set([
    "79e921d904d46fc9edc292e02a48f1aa54567a7d", # cannot build
    "603cd3d160c28b807c2ca50113fda00bafa51be7",
    "5a222cc79dc67ce01477da3a3ee10edf1076c655",
    "4e231e35d1a72ccb6025e0f4a45327f0f5a3e28b",
    "5005516135da3b11762bd9b7dc8fea7b1bef631b",
    "5005516135da3b11762bd9b7dc8fea7b1bef631b",
    "5005516135da3b11762bd9b7dc8fea7b1bef631b",
    "5005516135da3b11762bd9b7dc8fea7b1bef631b",
    "5005516135da3b11762bd9b7dc8fea7b1bef631b",
    "5005516135da3b11762bd9b7dc8fea7b1bef631b",
    "5005516135da3b11762bd9b7dc8fea7b1bef631b",
    "5005516135da3b11762bd9b7dc8fea7b1bef631b",
    "5005516135da3b11762bd9b7dc8fea7b1bef631b",
    "5005516135da3b11762bd9b7dc8fea7b1bef631b",
    "5005516135da3b11762bd9b7dc8fea7b1bef631b",
    "5005516135da3b11762bd9b7dc8fea7b1bef631b",
    "5005516135da3b11762bd9b7dc8fea7b1bef631b",
    "5005516135da3b11762bd9b7dc8fea7b1bef631b",
    "5005516135da3b11762bd9b7dc8fea7b1bef631b",
    "5005516135da3b11762bd9b7dc8fea7b1bef631b",
    "5005516135da3b11762bd9b7dc8fea7b1bef631b",
    "5005516135da3b11762bd9b7dc8fea7b1bef631b",
    "5005516135da3b11762bd9b7dc8fea7b1bef631b",
    "5005516135da3b11762bd9b7dc8fea7b1bef631b",
    "5005516135da3b11762bd9b7dc8fea7b1bef631b",
    "5005516135da3b11762bd9b7dc8fea7b1bef631b",
    "6ab571f1ee7cdd4dcf94a8919e71c6685bbd34ba",
    "6ab571f1ee7cdd4dcf94a8919e71c6685bbd34ba",
    "6ab571f1ee7cdd4dcf94a8919e71c6685bbd34ba",
    "6ab571f1ee7cdd4dcf94a8919e71c6685bbd34ba",
    "6ab571f1ee7cdd4dcf94a8919e71c6685bbd34ba",
    "6ab571f1ee7cdd4dcf94a8919e71c6685bbd34ba",
    "6ab571f1ee7cdd4dcf94a8919e71c6685bbd34ba",
    "6ab571f1ee7cdd4dcf94a8919e71c6685bbd34ba",
    "6ab571f1ee7cdd4dcf94a8919e71c6685bbd34ba",
    "250ca709b73000fe9c96fcc26109f233103b1636",
    "57fca38a4f51687d71e451ae29df6b353764fb72",
    "cb15f1b2904c0c4087bb5422cf18a7091fc5ac82",
    "ea4bf5d8341c4a861cd92eea0fb8331819a48f65",
    "4d78953db484839708091c610951678ab4b2b555",
    "1c9795f2e3e04a79f13d9e7658e6d6e47dfe1cc4",
    "d1ea514286c47433dabcf47b11cf81d2248ca5bf",
    "5d06b75a46ebc8ced68b2c5c11cd771aac0a4270",
    "3294fdf03973e5c7d968f4de49f2354d2cabd921",
    "3294fdf03973e5c7d968f4de49f2354d2cabd921",
    "3294fdf03973e5c7d968f4de49f2354d2cabd921",
    "3294fdf03973e5c7d968f4de49f2354d2cabd921",
    "3294fdf03973e5c7d968f4de49f2354d2cabd921",
    "c473b21cff5e1a459b4467f18bf7414114f848fd",
    "861ba79f31393dec0a0782ca11cf32cebb6f6610",
    "7be72a8f72330c13eb51c0eb992bcb0f2a027038",
    "64fd6b78baf939ef32c3bfe118f718242d0e3f4c",
  ]),
  build = c_blosc2_runner,
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

def faad2_runner(tool):
  tool.invoke(['./bootstrap'], script=True, check=True)
  tool.invoke(['make', '-j8'], make=True)
  subprocess.run(['git', 'checkout', '.'], cwd=tool.cwd)

faad2 = Repo(
  name = "faad2",
  url = "https://github.com/knik0/faad2",
  commits = ["bfab0b0", "1073aee"],
  build = faad2_runner,
  # build = bazel_runner,
)

libyang = Repo(
  name = "libyang",
  url = "https://github.com/CESNET/libyang",
  commits = ["f6d684a"],
  build = cmake_runner,
)

hiredis = Repo(
  name = "hiredis",
  url = "https://github.com/redis/hiredis",
  commits = ["d5b4c69"],
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

  faad2,
  libyang,
  hiredis,
]
