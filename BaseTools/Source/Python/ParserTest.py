from Library.MetaFileParser import DscParser,InfParser,DecParser
from Library.MetaFileTable import MetaFileStorage
from Common.Misc import PathClass
from CommonDataClass.DataClass import *


import Common.GlobalData as GlobalData
from Common.MultipleWorkspace import MultipleWorkspace as mws
import os


def TestDscParser(dsc_path):
    dsc_parser = DscParser(PathClass(dsc_path,r"D:\BobEdk2\edk2"),MODEL_FILE_DSC,"IA32",
                                MetaFileStorage(PathClass(dsc_path,r"D:\BobEdk2\edk2"), MODEL_FILE_DSC))
    for item in dsc_parser[MODEL_META_DATA_COMPONENT,"IA32"]:
        print(item)

    for item in dsc_parser[MODEL_PCD_FIXED_AT_BUILD]:
        print (item)

    for item in dsc_parser[MODEL_META_DATA_HEADER]:
        print(item)

    for item in dsc_parser[MODEL_EFI_SKU_ID]:
        print(item)

    for item in dsc_parser[MODEL_EFI_DEFAULT_STORES]:
        print(item)

    for item in dsc_parser[MODEL_META_DATA_PACKAGE]:
        print(item)

    for item in dsc_parser[MODEL_EFI_LIBRARY_CLASS]:
        print(item)

    for item in dsc_parser[MODEL_META_DATA_BUILD_OPTION]:
        print(item)

def TestInfParser(inf_path):
    inf_parser = InfParser(PathClass(inf_path,r"D:\BobEdk2\edk2"),MODEL_FILE_INF,"IA32",
                                MetaFileStorage(PathClass(inf_path,r"D:\BobEdk2\edk2"), MODEL_FILE_INF))
    for item in inf_parser[MODEL_META_DATA_HEADER]:
        print(item)

    for item in inf_parser[MODEL_EFI_SOURCE_FILE]:
        print (item)

    for item in inf_parser[MODEL_EFI_LIBRARY_CLASS]:
        print(item)

    for item in inf_parser[MODEL_EFI_LIBRARY_INSTANCE]:
        print(item)

    for item in inf_parser[MODEL_EFI_PROTOCOL]:
        print(item)

    for item in inf_parser[MODEL_EFI_PPI]:
        print(item)

    for item in inf_parser[MODEL_EFI_GUID]:
        print(item)

    for item in inf_parser[MODEL_EFI_INCLUDE]:
        print(item)

    for item in inf_parser[MODEL_META_DATA_PACKAGE]:
        print(item)

    for item in inf_parser[MODEL_PCD_DYNAMIC]:
        print(item)

    for item in inf_parser[MODEL_META_DATA_BUILD_OPTION]:
        print(item)

    for item in inf_parser[MODEL_EFI_DEPEX]:
        print(item)

def TestDecParser(dec_path):
    inf_parser = DecParser(PathClass(dec_path,r"D:\BobEdk2\edk2"),MODEL_FILE_INF,"IA32",
                                MetaFileStorage(PathClass(dec_path,r"D:\BobEdk2\edk2"), MODEL_FILE_INF))
    for item in inf_parser[MODEL_META_DATA_HEADER]:
        print(item)

    for item in inf_parser[MODEL_EFI_PROTOCOL]:
        print (item)

    for item in inf_parser[MODEL_EFI_PPI]:
        print(item)

    for item in inf_parser[MODEL_EFI_GUID]:
        print(item)

    for item in inf_parser[MODEL_EFI_INCLUDE]:
        print(item)

    for item in inf_parser[MODEL_EFI_LIBRARY_CLASS]:
        print(item)

    for item in inf_parser[MODEL_PCD_DYNAMIC]:
        print(item)

if __name__ == "__main__":
    WorkspaceDir = r"D:\BobEdk2\edk2"
    GlobalData.gGlobalDefines['WORKSPACE'] = WorkspaceDir
    GlobalData.gWorkspace = WorkspaceDir
    PackagesPath = os.getenv("PACKAGES_PATH")
    mws.setWs(WorkspaceDir, PackagesPath)
    dsc_path = r"OvmfPkg\OvmfPkgIa32.dsc"
    inf_path = r"OvmfPkg\Sec\SecMain.inf"
    dec_path = r"OvmfPkg\OvmfPkg.dec"
    TestDecParser(dec_path)
    TestInfParser(inf_path)
    TestDscParser(dsc_path)
