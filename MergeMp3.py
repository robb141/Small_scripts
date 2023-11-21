import re
import os
import sys
import getopt


def main(argv):
    indir = ""
    outdir = ""
    opts, args = getopt.getopt(argv, "hi:o:", ["idir=", "odir="])
    for opt, arg in opts:
        if opt == "-h":
            print("test.py -i <inputdir> -o <outputdir>")
            sys.exit()
        elif opt in ("-i", "--idir"):
            indir = arg
        elif opt in ("-o", "--odir"):
            outdir = arg
    print("Input dir is ", indir)
    print("Output dir is ", outdir)
    return indir, outdir


if __name__ == "__main__":
    inputdir, outputdir = main(sys.argv[1:])
    new_name = re.findall("^[^(]*", os.path.basename(inputdir))[0].strip()
    for file in os.listdir(inputdir):
        print(file)
        with open(os.path.join(inputdir, file), "rb") as f:
            if "new_file" in vars():
                new_file += f.read()
            else:
                new_file = f.read()
    with open(os.path.join(outputdir, f"{new_name}.mp3"), "wb") as f:
        f.write(new_file)
    print("Script finished.")
