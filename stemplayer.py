import pyaudio, wave, numpy, time, keyboard, os
import serial
import string
import time

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

ser = serial.Serial('/dev/ttyUSB2', 9600)
potVal = [0.0,0.0,0.0,0.0]

def callback(in_data, frame_count, time_info, status):
    global drumsMod, vocalsMod, bassMod, otherMod, potVal
    serialData=ser.readline()
    if serialData == "Start":
        for i in range(0,4):
            potVal[i] = ser.readline()
    drumsMod = potVal[0]
    vocalsMod = potVal[1]
    bassMod = potVal[2]
    otherMod = potVal[3]

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