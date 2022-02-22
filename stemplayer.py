import pyaudio, wave, numpy, time, keyboard, os
p = pyaudio.PyAudio()

cwd = os.path.dirname(os.path.abspath(__file__))
songFolder = "OffTheGrid"
targetDir = os.path.join(cwd, songFolder)

drumsWF = wave.open(os.path.join(targetDir,"drums.wav"), "rb")
vocalsWF = wave.open(os.path.join(targetDir, "vocals.wav"),"rb")
bassWF = wave.open(os.path.join(targetDir,"bass.wav"),"rb")
otherWF = wave.open(os.path.join(targetDir,"other.wav"),"rb")

drumsMod = 1
vocalsMod = 1
bassMod = 1
otherMod = 1

def incMod(modvar):
    if modvar >= 1:
        modvar = 1
    else:
        modvar += 0.1
    return modvar
def decMod(modvar):
    if modvar <= 0:
        modvar = 0
    else:
        modvar -= 0.1
    return modvar

def callback(in_data, frame_count, time_info, status):
    global drumsMod, vocalsMod, bassMod, otherMod
    if keyboard.is_pressed('q'):
        drumsMod = incMod(drumsMod)
    elif keyboard.is_pressed('a'):
        drumsMod = decMod(drumsMod)
    elif keyboard.is_pressed('w'):
        vocalsMod = incMod(vocalsMod)
    elif keyboard.is_pressed('s'):
        vocalsMod = decMod(vocalsMod)
    elif keyboard.is_pressed('e'):
        bassMod = incMod(bassMod)
    elif keyboard.is_pressed('d'):
        bassMod = decMod(bassMod)
    elif keyboard.is_pressed('r'):
        otherMod = incMod(otherMod)
    elif keyboard.is_pressed('f'):
        otherMod = decMod(otherMod)
    drums = drumsWF.readframes(frame_count)
    vocals = vocalsWF.readframes(frame_count)
    bass = bassWF.readframes(frame_count)
    other = otherWF.readframes(frame_count)
    decodedDrums = numpy.frombuffer(drums, numpy.int16)
    decodedVocals = numpy.frombuffer(vocals, numpy.int16)
    decodedBass = numpy.frombuffer(bass, numpy.int16)
    decodedOther = numpy.frombuffer(other, numpy.int16)
    
    newdata = (decodedDrums*drumsMod + decodedVocals*vocalsMod + decodedBass*bassMod + decodedOther*otherMod).astype(numpy.int16)
    return (newdata.tobytes(), pyaudio.paContinue)

stream = p.open(format=p.get_format_from_width(drumsWF.getsampwidth()),
                channels=drumsWF.getnchannels(),
                rate=drumsWF.getframerate(),
                output=True,
                stream_callback=callback,
                start=True)

try:
    print("[+] Starting stream...")
    stream.start_stream()
    while True:
        if not stream.is_active():
            stream.stop_stream()
            stream.close()
            p.terminate()
            break

except KeyboardInterrupt:
    print("[+] Keyboard interrupt received... ending stream")
    stream.stop_stream()
    stream.close()
    p.terminate()
    exit()