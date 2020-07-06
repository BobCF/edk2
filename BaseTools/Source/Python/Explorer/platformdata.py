from Explorer.logger import logger
from AutoGen.DataPipe import MemoryDataPipe
import Common.GlobalData as GlobalData
from Common.MultipleWorkspace import MultipleWorkspace as mws
from AutoGen.ModuleAutoGen import ModuleAutoGen
from AutoGen.ModuleAutoGenHelper import WorkSpaceInfo
from Common.Misc import PathClass
import os

class PlatformData():
    def __init__(self,pdata):
        self.PlatformMetaFileSet = {}
        self.pdata = [self.readdata(item) for item in pdata]
        
    def readdata(self,globalvar):
        MaSet = set()
        try:
            data_pipe = MemoryDataPipe()
            data_pipe.load(globalvar)
        except:
            logger.error("Load global variable failed.")
            exit(-1)
            
        target = data_pipe.Get("P_Info").get("Target")
        toolchain = data_pipe.Get("P_Info").get("ToolChain")
        archlist = data_pipe.Get("P_Info").get("ArchList")

        active_p = data_pipe.Get("P_Info").get("ActivePlatform")
        workspacedir = data_pipe.Get("P_Info").get("WorkspaceDir")
        PackagesPath = os.getenv("PACKAGES_PATH")
        mws.setWs(workspacedir, PackagesPath)
        Wa = WorkSpaceInfo(
            workspacedir,active_p,target,toolchain,archlist
            )
        Wa._SrcTimeStamp = data_pipe.Get("Workspace_timestamp")
        GlobalData.gGlobalDefines = data_pipe.Get("G_defines")
        GlobalData.gCommandLineDefines = data_pipe.Get("CL_defines")
        os.environ._data = data_pipe.Get("Env_Var")
        GlobalData.gWorkspace = workspacedir
        GlobalData.gDisableIncludePathCheck = False
        GlobalData.gFdfParser = data_pipe.Get("FdfParser")
        GlobalData.gDatabasePath = data_pipe.Get("DatabasePath")

        GlobalData.gEnableGenfdsMultiThread = data_pipe.Get("EnableGenfdsMultiThread")

        pcd_from_build_option = []
        for pcd_tuple in data_pipe.Get("BuildOptPcd"):
            pcd_id = ".".join((pcd_tuple[0],pcd_tuple[1]))
            if pcd_tuple[2].strip():
                pcd_id = ".".join((pcd_id,pcd_tuple[2]))
            pcd_from_build_option.append("=".join((pcd_id,pcd_tuple[3])))
        GlobalData.BuildOptionPcd = pcd_from_build_option

        FfsCmd = data_pipe.Get("FfsCommand")
        if FfsCmd is None:
            FfsCmd = {}
        GlobalData.FfsCmd = FfsCmd
        PlatformMetaFile = self.GetPlatformMetaFile(data_pipe.Get("P_Info").get("ActivePlatform"),
                                         data_pipe.Get("P_Info").get("WorkspaceDir"))
        
        ModuleLibs = data_pipe.Get("DEPS")
        libModules = data_pipe.Get("REFS")
        
        for module_file,module_root,module_arch,module_path in ModuleLibs: 
            module_metafile = PathClass(os.path.normpath(module_file),os.path.normpath(module_root))
            module_metafile.Arch = module_arch
            if module_path:
                module_metafile.Path = os.path.normpath(module_path)
            arch = module_arch
            target = data_pipe.Get("P_Info").get("Target")
            toolchain = data_pipe.Get("P_Info").get("ToolChain")
            Ma = ModuleAutoGen(Wa,module_metafile,target,toolchain,arch,PlatformMetaFile,data_pipe)
            deps = ModuleLibs[(module_file,module_root,module_arch,module_path)]
            for l in deps:
                l_module_file,l_module_root,l_module_arch,l_module_path = l 
                l_module_metafile = PathClass(l_module_file,l_module_root)
                if l_module_path:
                    l_module_metafile.Path = l_module_path 
                Ma.Module.LibInstances.append(ModuleAutoGen(Wa,l_module_metafile,target,toolchain,arch,PlatformMetaFile,data_pipe))
            if Ma:
                Ma.IsLibrary = False
                MaSet.add(Ma)
            else:
                logger.error(module_metafile)
        for module_file,module_root,module_arch,module_path in libModules: 
            module_metafile = PathClass(module_file,module_root)
            if module_path:
                module_metafile.Path = module_path
            arch = module_arch
            target = data_pipe.Get("P_Info").get("Target")
            toolchain = data_pipe.Get("P_Info").get("ToolChain")
            Ma = ModuleAutoGen(Wa,module_metafile,target,toolchain,arch,PlatformMetaFile,data_pipe)
            ref_ms = libModules[(module_file,module_root,module_arch,module_path)]
            for m in ref_ms:
                m_module_file,m_module_root,m_module_arch,m_module_path = m
                m_module_metafile = PathClass(m_module_file,m_module_root)
                if m_module_path:
                    m_module_metafile.Path = m_module_path 
                Ma.ReferenceModules.append(ModuleAutoGen(Wa,m_module_metafile,target,toolchain,arch,PlatformMetaFile,data_pipe))
            if Ma:
                Ma.IsLibrary = True
                MaSet.add(Ma)
            else:
                logger.error(module_metafile)
        return MaSet
    
    def GetPlatformMetaFile(self,filepath,root):
        try:
            return self.PlatformMetaFileSet[(filepath,root)]
        except:
            self.PlatformMetaFileSet[(filepath,root)]  = filepath
            return self.PlatformMetaFileSet[(filepath,root)]
    
    @property
    def MaSet(self):
        rt = set()
        for maset in self.pdata:
            rt |= maset
        return rt