from Explorer.explorer_comp import ExplorerComp
import os

class CompLibClass(ExplorerComp):
    def __init__(self, libclass=None):
        super(CompLibClass,self).__init__()
        self.lib_module_set = dict()
        self.lib_instance_set = dict()
        self.libclass = libclass

    def handle(self,module_set):
        for ma in module_set:
            if ma.IsLibrary:
                for libc in ma.Module.LibraryClass:
                    self.lib_instance_set.setdefault(libc.LibraryClass,[]).append(ma.MetaFile.Path)
                self.lib_module_set.setdefault(ma.MetaFile.Path,[]).extend(ma.ReferenceModules)

    def format(self):
        myview = self.getViewer()
        libcount = 0
        if not self.libclass: 
            for libclass in sorted(self.lib_instance_set.keys()):
                myview.addline(libclass)
        else:
            if self.libclass in self.lib_instance_set:
               myview.addline(self.libclass)
               myview.tab()
               for filepath in self.lib_instance_set[self.libclass]:
                   myview.addline(filepath)
                   myview.tab()
                   for module in self.lib_module_set[filepath]:
                       myview.addline(module.MetaFile.Path)
                   myview.untab()
            elif self.libclass == "all":
                for libc in self.lib_instance_set:
                    myview.addline(libc)
                    myview.tab()
                    for filepath in self.lib_instance_set[libc]:
                        myview.addline(filepath)
                        myview.tab()
                        for module in self.lib_module_set[filepath]:
                            myview.addline(module.MetaFile.Path)
                        myview.untab()
                    myview.untab()
            elif self.libclass == "alllibs":
                for libc in self.lib_instance_set:
                    myview.addline(libc)
                    myview.tab()
                    for filepath in self.lib_instance_set[libc]:
                        myview.addline(filepath)
                    libcount += len(self.lib_instance_set[libc])
                    myview.untab()
                myview.addline("---------------------------")
                myview.addline(str(libcount))