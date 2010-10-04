import fnmatch
import os
import shutil

baseDir = os.path.join(os.path.expanduser("~") , 'Desktop', '100CANON')
group = {}
# could use glob.glob instead of listdir + fnmatch
for fileName in os.listdir(baseDir):
    if fnmatch.fnmatch(fileName, 'ST*.JPG'):    # STA_8288.JPG, STB_8289.JPG, STC_8290.JPG, and etc
        alphabet = fileName[2]
        group.setdefault(alphabet, [])
        group[alphabet].append(fileName)
for alphabet, fileNames in group.items():
    folder = os.path.join(baseDir, alphabet)
    if not os.path.exists(folder):
        os.mkdir(folder)
    for file in fileNames:
        shutil.copy(os.path.join(baseDir, file), folder)
