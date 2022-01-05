import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["8.45"]:
            self.targets[ver] = f"https://downloads.sourceforge.net/sourceforge/pcre/pcre-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"pcre-{ver}"
        self.patchToApply["8.45"] = [("pcre-8.10-20101125.diff", 1)]
        self.targetDigests['8.45'] = (
            ['4dae6fdcd2bb0bb6c37b5f97c33c2be954da743985369cddac3546e3218bffb8'], CraftHash.HashAlgorithm.SHA256)

        self.description = "Perl-Compatible Regular Expressions"
        self.defaultTarget = "8.45"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libbzip2"] = None
        self.runtimeDependencies["libs/zlib"] = None


class Package(CMakePackageBase):
    def fixLibraryID(self, packageName):
        root = str(CraftCore.standardDirs.craftRoot())
        craftLibDir = os.path.join(root,  'lib')
        utils.system("install_name_tool -add_rpath " + craftLibDir + " " + craftLibDir +"/" + packageName + ".dylib")
        utils.system("install_name_tool -id @rpath/" + packageName + ".dylib " + craftLibDir +"/" + packageName + ".dylib")

    def __init__(self, **args):
        CMakePackageBase.__init__(self)

        defines = "-DBUILD_SHARED_LIBS=ON "
        defines += "-DPCRE_SUPPORT_UNICODE_PROPERTIES=ON "
        defines += "-DPCRE_SUPPORT_UTF8=ON "
        defines += "-DPCRE_EBCDIC=OFF "
        if CraftCore.compiler.isAndroid:
            defines += "-DHAVE_STRTOQ=FALSE -DPCRE_BUILD_PCREGREP=FALSE -DPCRE_BUILD_TEST=FALSE"
        self.subinfo.options.configure.args = defines

    def postQmerge(self):
        self.fixLibraryID("libpcre")
        self.fixLibraryID("libpcrecpp")
        self.fixLibraryID("libpcreposix")
        root = str(CraftCore.standardDirs.craftRoot())
        craftLibDir = os.path.join(root,  'lib')
        utils.system("install_name_tool -change libpcre.dylib @rpath/libpcre.dylib " + craftLibDir +  "/" + "libpcrecpp.dylib")
        utils.system("install_name_tool -change libpcre.dylib @rpath/libpcre.dylib " + craftLibDir +  "/" + "libpcreposix.dylib")
        return True

