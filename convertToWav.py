from pydub import AudioSegment
from pydub.playback import play
import os

cwd = os.path.dirname(os.path.abspath(__file__))
vocals = AudioSegment.from_file(os.path.join(cwd, "vocals.mp3"))
drums = AudioSegment.from_file(os.path.join(cwd, "drums.mp3"))
bass = AudioSegment.from_file(os.path.join(cwd,"bass.mp3"))
other = AudioSegment.from_file(os.path.join(cwd,"other.mp3"))

vocals.export(os.path.join(cwd,"vocals.wav"), format='wav') 
drums.export(os.path.join(cwd,"drums.wav"), format='wav') 
bass.export(os.path.join(cwd,"bass.wav"), format='wav') 
other.export(os.path.join(cwd,"other.wav"),format='wav')

