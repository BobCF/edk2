
from Explorer.explorer_comp import ExplorerComp
import os

class CompFileType(ExplorerComp):
    def __init__(self, filetype=None):
        super(CompFileType,self).__init__()
        self.file_type_set = dict()
        self.filetype = filetype
        self.file_set = dict()

    def handle(self,module_set):
        for ma in module_set:
            for source in ma.SourceFileList:
                self.file_type_set.setdefault(os.path.splitext(source.File)[-1][1:],[]).append(ma)
                self.file_set.setdefault(os.path.splitext(source.File)[-1][1:],[]).append(source.File)

    def format(self):
        myview = self.getViewer()
        filecount = 0
        if not self.filetype: 
            for f_type in self.file_type_set:
                myview.addline(f_type)
            myview.addline("---------------------")
            myview.addline(str(len(self.file_type_set)))
        else:
            if self.filetype in self.file_type_set:
                myview.addline(self.filetype)
                myview.tab()
                for filepath in self.file_type_set[self.filetype]:
                    myview.addline(filepath)
            elif self.filetype == "all":
                for filetype in self.file_type_set:
                    myview.addline(filetype)
                    myview.tab()
                    filecount += len(self.file_set[filetype])
                    for filepath in self.file_set[filetype]:
                        myview.addline(filepath)
                    myview.untab()
                myview.addline("---------------------")
                myview.addline(str(filecount))

