"""
creattime: 2023/3/23
"""
"""
This tool would dump the hex info from the file
"""

import os
import argparse
import sys

CSIZE =  16
TYPE  = "0x"
INTERVALSYM = ","


def analizefile(data,outputfile):
    try:
        count = len(data)
        log_txt = open(outputfile, "w")
        number = count%CSIZE
        if number == 0:
            maxline = count//CSIZE
        else:
            maxline = count//CSIZE + 1
        line = 1
        linedata  = ""
        csize = 0
        for i in range(0,count):
          word = data[i:i+1].hex()
          xword = TYPE + word + INTERVALSYM
          linedata = linedata + xword
          csize +=1
          if csize == CSIZE:
              line += 1
              csize = 0
              linedata = linedata.strip(INTERVALSYM)
              linedata = linedata + INTERVALSYM
              log_txt.write(f"{linedata}\n")
              linedata = ""
              continue
          if line ==  maxline:
             if csize == number:
                linedata = linedata.strip(INTERVALSYM)
                log_txt.write(f"{linedata}\n")
    

        print("output the hex info to file:",outputfile)

    except RuntimeError as error_messge:
        print(str(error_messge))
        sys.exit(1)

def openfile(filepath,outputfile):
    try:
        with open(filepath, "rb") as f:
            data = f.read()
    except Exception as e:
        raise Exception(f"Error: Cannot read file {filepath} {e}")

    analizefile(data,outputfile)

def get_file_path(args):
    file_path = ''
    input_path = args.file

    try:
        if not input_path:
            error_messge = "{}\n{}".format("[Error] no input","pls use the cmd -f/--file <file path>")
            raise RuntimeError(error_messge)
        #check the input path
        file_path = os.path.abspath(input_path)
        if os.path.exists(file_path):
          return file_path
        error_messge = "{}\n{}\n{}".format("[Error] the input file:",file_path,"was not exists, pls check the path")
        raise RuntimeError(error_messge)
    except RuntimeError as error_messge:
        print(str(error_messge))
        sys.exit(1)


def parse_arguments():
    argparser = argparse.ArgumentParser(description="Dump hex info from the input file",
                                        usage="Dump hex info [-h][--help] [-f][--file] [-o][--ouput]")

    argparser.add_argument('-f', "--file",help="The input file(eg: -f test.bin)")
    argparser.add_argument('-o', "--output",help="The output file(eg: -o certoutput.txt)")
    try:
        args = argparser.parse_args()
    except:
        sys.exit(1)
    return args

if __name__ == "__main__":
    args = parse_arguments()
    ouputfile  = args.output
    if not ouputfile:
        ouputfile = "output.txt"
    file_path = get_file_path(args)
    openfile(file_path,ouputfile)
