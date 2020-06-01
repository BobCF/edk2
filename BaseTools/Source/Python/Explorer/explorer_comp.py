from Explorer.viewer import Viewer

class ExplorerComp():
    def __init__(self):
        self.viewer = None

    def list(self, outputfile = None):
        self.format()
        if not self.viewer:
            print("no view init")
            return
        self.viewer.display()
        if outputfile:
            self.viewer.savetofile(outputfile)

    def getViewer(self):
        self.viewer = Viewer()
        return self.viewer

    def format(self):
        pass

    def handle(self,*args):
        pass
