
from Explorer.explorer_comp import ExplorerComp
import os

class CompModules(ExplorerComp):
    def __init__(self, modulename=None):
        super(CompModules,self).__init__()
        self.module_lib_set = dict()
        self.module_name_set = dict()
        self.modulename = modulename

    def handle(self,module_set):
        for ma in module_set:
            if ma.IsLibrary:
                continue
            self.module_name_set.setdefault(ma.Name,[]).append(ma.MetaFile.Path)
            for lib in ma.Module.LibInstances:
                self.module_lib_set.setdefault(ma.MetaFile.Path,[]).append(lib.MetaFile.Path)

    def format(self):
        myview = self.getViewer()
        if not self.modulename: 
            for modulename in sorted(self.module_name_set.keys()):
                myview.addline(modulename)
        else:
            if self.modulename in self.module_name_set:
               myview.addline(self.modulename)
               myview.tab()
               for filepath in self.module_name_set[self.modulename]:
                   myview.addline(filepath)
                   myview.tab()
                   for libpath in self.module_lib_set[filepath]:
                       myview.addline(libpath)
                   myview.untab()