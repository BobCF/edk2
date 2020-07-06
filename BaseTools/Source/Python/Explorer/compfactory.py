from Explorer.comp_moduletype import CompModuleType
from Explorer.comp_filetype import CompFileType
from Explorer.comp_libclass import CompLibClass
from Explorer.comp_modules import CompModules
from Explorer.explorer_comp import ExplorerComp
class CompFactory():
    def __init__(self):
        pass
    def get(self, opt):
        if opt.etype == "ModuleType":
            return CompModuleType()
        if opt.etype == "FileType":
            return CompFileType()
        if opt.etype == "LibClass":
            return CompLibClass()
        if opt.etype == "ModuleName":
            return CompModules()
        if opt.filetype:
            return CompFileType(opt.filetype)
        if opt.libclass:
            return CompLibClass(opt.libclass)
        if opt.moduletype:
            return CompModuleType(opt.moduletype)
        if opt.modulename:
            return CompModules(opt.modulename)
        else:
            return ExplorerComp()

comp_factory = CompFactory()