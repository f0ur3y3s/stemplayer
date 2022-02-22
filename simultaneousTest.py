import pyaudio
import wave
import numpy
import time
import keyboard  # using module keyboard

p = pyaudio.PyAudio()


drumsWF = wave.open("drums.wav", "rb")
vocalsWF = wave.open("vocals.wav","rb")
bassWF = wave.open("bass.wav","rb")
otherWF = wave.open("other.wav","rb")
drumsMod = 1
vocalsMod = 1
bassMod = 1
otherMod = 1
# def incMod(modvar):
#     modvar += 0.1
# def decMod(modvar):
#     modvar -= 0.1
def callback(in_data, frame_count, time_info, status):
    global drumsMod, vocalsMod, bassMod, otherMod
    # control = keyboard.read_key()
    # match control:
    if keyboard.is_pressed('q'):
        if drumsMod >= 1:
            drumsMod = 1
        else:
            drumsMod += 0.1
    elif keyboard.is_pressed('a'):
        if drumsMod <= 0:
            drumsMod = 0
        else:
            drumsMod -= 0.1
    elif keyboard.is_pressed('w'):
        if vocalsMod >= 1:
            vocalsMod = 1
        else:
            vocalsMod += 0.1
    elif keyboard.is_pressed('s'):
        if vocalsMod <= 0:
            vocalsMod = 0
        else:
            vocalsMod -= 0.1
    elif keyboard.is_pressed('e'):
        if bassMod >= 1:
            bassMod = 1
        else:
            bassMod += 0.1
    elif keyboard.is_pressed('d'):
        if bassMod <= 0:
            bassMod = 0
        else:
            bassMod -= 0.1
    elif keyboard.is_pressed('r'):
        if otherMod >= 1:
            otherMod = 1
        else:
            otherMod += 0.1
    elif keyboard.is_pressed('f'):
        if otherMod <= 0:
            otherMod = 0
        else:
            otherMod -= 0.1
        # case _:
        #     pass
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

stream.start_stream()

while stream.is_active():
    time.sleep(100)
    stream.stop_stream()
stream.close()

p.terminate()