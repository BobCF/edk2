import os

class LineStr():
    def __init__(self,linestr, formatstr):
        self.linestr = linestr
        self.formatstr = formatstr

class Viewer():
    def __init__(self):
        self.lines = []
        self.depth = 0

    def addline(self,linestr):
        self.lines.append(LineStr(linestr,self.depth))

    def tab(self):
        self.depth += 1
    def untab(self):
        if self.depth > 0:
            self.depth -= 1
    def display(self):
        for line in self.lines:
            print("%s%s" % ("."*line.formatstr*4, line.linestr))

    def savetofile(self,outputfile):
        ''' save the content as md format to outputfile '''
        if os.path.exists(outputfile):
            with open(outputfile,"w") as fw:
                for line in self.lines:
                    fw.write("%s%s\n" % (" "*line.formatstr, line.linestr))
