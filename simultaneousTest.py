import pyaudio
import wave
import numpy
import time

p = pyaudio.PyAudio()

drumsWF = wave.open("drums.wav", "rb")
vocalsWF = wave.open("vocals.wav","rb")
bassWF = wave.open("bass.wav","rb")
otherWF = wave.open("other.wav","rb")

def callback(in_data, frame_count, time_info, status):
    drums = drumsWF.readframes(frame_count)
    vocals = vocalsWF.readframes(frame_count)
    bass = bassWF.readframes(frame_count)
    other = otherWF.readframes(frame_count)
    decodedDrums = numpy.frombuffer(drums, numpy.int16)
    decodedVocals = numpy.frombuffer(vocals, numpy.int16)
    decodedBass = numpy.frombuffer(bass, numpy.int16)
    decodedOther = numpy.frombuffer(other, numpy.int16)
    
    newdata = (decodedDrums + decodedVocals + decodedBass + decodedOther).astype(numpy.int16)
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