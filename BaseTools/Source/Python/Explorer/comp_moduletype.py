from Explorer.explorer_comp import ExplorerComp

class CompModuleType(ExplorerComp):
    def __init__(self,moduletype=None):
        super(CompModuleType,self).__init__()
        self.module_type_set = dict()
        self.moduletype = moduletype

    def handle(self,module_set):
        for ma in module_set:
            self.module_type_set.setdefault(ma.ModuleType,[]).append(ma.MetaFile)

    def format(self):
        myview = self.getViewer()
        if not self.moduletype:
            for m_type in self.module_type_set:
                myview.addline(m_type)
            myview.addline("-----------------")
            myview.addline(str(len(self.module_type_set)))
        else:
            if self.moduletype in self.module_type_set:
                myview.addline(self.moduletype)
                myview.tab()
                for m in self.module_type_set[self.moduletype]:
                    myview.addline(m)
