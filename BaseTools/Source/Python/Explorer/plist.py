import argparse
from Explorer.compfactory import comp_factory
from Explorer.platformdata import PlatformData
import os
from Explorer.logger import logger

optparser = argparse.ArgumentParser()
optparser.add_argument("-t", dest="etype", help="What type of data.")
optparser.add_argument("-o", dest="outputfile", help="Write the result to a output file")
optparser.add_argument("-f", dest="filetype", help="list files of file type")
optparser.add_argument("-m", dest="moduletype", help="list modules of module type")
optparser.add_argument("-l", dest="libclass", help="list modules refere to a Lib")
optparser.add_argument("-ml", dest="modulename", help="list libraries used in a module")
opt = optparser.parse_args()

def getplatform():
    build_folder = os.environ.get('BuildRoot')
    rt = []
    if not build_folder:
        logger.error("Please Set BuildRoot environment variable.")
        exit(-1)
    for buildfile in os.listdir(build_folder):
        _,fileext = os.path.splitext(buildfile)
        filename = os.path.basename(buildfile)
        if fileext == ".bin" and filename.startswith("GlobalVar"):
            rt.append(os.path.join(build_folder,buildfile))
    return rt

def main():
    component = comp_factory.get(opt)
    pdata = PlatformData(getplatform())
    component.handle(pdata.MaSet)
    component.list(opt.outputfile)

if __name__ == "__main__":
    main()