#!/usr/local/bin/python3

import sys
import os
import time
import getopt
import re
import subprocess

for a in sys.argv:
  for dirName, subdirList, fileList in os.walk(a, topdown=False):
    if '.AppleDouble' in dirName:
      continue
    if '@SynoEAStream' in dirName:
      continue
    if '@SynoResource' in dirName:
      continue
    if '@eaDir' in dirName:
      continue
    for f in fileList:
      if f.lower().endswith('.mp4'):
        print("Skipping {} because no point in messing with mp4's".format(f))
        continue
      if not ( f.lower().endswith('.mpg') or
               f.lower().endswith('.mpeg') or
               f.lower().endswith('.wmv') or
               f.lower().endswith('.rm') or
               f.lower().endswith('.avi') or
               f.lower().endswith('.rm') or
               f.lower().endswith('.3g2') or
               f.lower().endswith('.divx') or
               f.lower().endswith('.flv')):
        print("Skipping {} because not obviously a video file".format(f))
        continue
      if not os.access(os.path.join(dirName,f),os.R_OK):
        print("Skipping {} because not readable".format(f))
        continue
      if os.stat(os.path.join(dirName,f)).st_size == 0:
        print("Skipping {} because zero length".format(f))
        continue
      nf = f.encode('utf-8').decode('unicode_escape')
      nf = re.sub(r'\\x..', r'', nf, count=0, flags=re.IGNORECASE)
      nf = re.sub(r'\\x..', r'', nf, count=0, flags=re.IGNORECASE)
      nf = re.sub(r' \[~of\d+\]', r'', nf, count=0, flags=re.IGNORECASE)
      nf = re.sub(r' - File ~ of \d+', r'', nf, count=0, flags=re.IGNORECASE)
      nf = re.sub(r' yEnc  ~ bytes  -', r'', nf, count=0, flags=re.IGNORECASE)
      nf = re.sub(r'~', r'', nf, count=0, flags=re.IGNORECASE)
      nf = re.sub(r'\(\)', r'', nf, count=0, flags=re.IGNORECASE)
      nf = re.sub(r'\s', r'_', nf, count=0, flags=re.IGNORECASE)
      nf = re.sub(r'&', r'_and_', nf, count=0, flags=re.IGNORECASE)
      nf = re.sub(r'(.*)\..*',r'\1',nf) + ".mp4"
      if (os.access(os.path.join(dirName,nf),os.F_OK) and
         os.stat(os.path.join(dirName,nf)).st_size > 0):
        print("Skipping {} because {} exists with nonzero length".format(f,nf))
        continue
      stat = os.stat(os.path.join(dirName,f))
      print("gonna do ffmpeg -i {} {}".format(f,nf))
      result = subprocess.run([ '/usr/local/bin/ffmpeg',
                       '-i',
                       os.path.join(dirName,f),
                       os.path.join(dirName,nf) ])
      if result.returncode:
        print("ffmpeg -i {} {} appears to have failed".format(f,nf))
      else:
        os.rename(os.path.join(dirName,f),os.path.join(dirName,"deleteme-" + f))
        os.utime(os.path.join(dirName,nf), times=(stat.st_mtime, stat.st_mtime))

