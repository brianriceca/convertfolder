#!/usr/local/bin/python3

import sys
import getopt
import os
import re
from subprocess import run

def main(argv):
    try:
        opts, dirs_to_walk = getopt.getopt(argv,"nv")
    except getopt.GetoptError:
        print('convertfolder.py -v|-n dirs_to_walk')
        sys.exit(2)

    basedir=os.getcwd()
    print("basedir is {}".format(basedir))
    for d in dirs_to_walk:
        print("d is {}".format(d))
        for root, dirs, files in os.walk(d):
            if (".AppleDouble" in dirs):
                dirs.remove(".AppleDouble")
            print("root is {}".format(root))
            for f in files:
                if (f == ".DS_Store"):
                    continue
                if (re.match('deleteme-',f)):
                    continue
                ftype=re.sub(r'^.*\.(.*)$',r'\1',f)
                if (ftype.lower() == 'mp4'):
                    print("skipping {} because no point in messing with mp4s".format(f))
                    continue
                nname=re.sub(r'\s','_',f)
                nname=re.sub(r'\'','',nname)
                nname=re.sub(r'[\[\]~]','-',nname)
                nname=re.sub(r'^(.*)\..*$',r'\1.mp4',nname)
                print("{} --> {}".format(f,nname))
                if os.path.isfile(os.path.join(basedir,d,nname)): 
                    print("skipping {} because {} already exists".format(f,nname))
                    continue
                if ftype.lower() not in 'mov|mpeg|mpg|avi|wmv|rm|3g2|divx':
                    print("skipping {} because type {} not recognized".format(f,ftype))
                    continue
                cp = run(['/usr/local/bin/ffmpeg','-i',os.path.join(basedir,d,f),os.path.join(basedir,d,nname)])
                if cp.returncode:
                    print("ffmpeg seems to have failed on {}".format(f))
                else:
                    new_atime = os.path.getatime(os.path.join(basedir,d,f))
                    new_mtime = os.path.getmtime(os.path.join(basedir,d,f))
                    os.utime(os.path.join(basedir,d,nname),(new_atime,new_mtime))
                    os.rename(os.path.join(basedir,d,f),os.path.join(basedir,d,"deleteme-" + f))
                    print("SUCCESS {}".format(f))

if __name__ == "__main__":
    main(sys.argv[1:])
