from pydub import AudioSegment
from os import listdir
from os.path import isfile, join
import os

cwd = os.path.dirname(os.path.abspath(__file__))

onlyFiles = [f for f in listdir(cwd) if isfile(join(cwd, f))]
for file in onlyFiles:
    if ".mp3" in file or ".flac" in file:
        fileName = file.split(".")[0]
        openedFile = AudioSegment.from_file(os.path.join(cwd, file))
        openedFile.export(os.path.join(cwd, fileName + ".wav"), format='wav') 
