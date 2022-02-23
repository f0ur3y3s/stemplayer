import pyaudio, wave, numpy, time, keyboard, os
import tkinter as tk
from tkinter import filedialog
import datetime
import cursor
# setup pyaudio
p = pyaudio.PyAudio()

# get current working directory
cwd = os.path.dirname(os.path.abspath(__file__))

# setting up tkinter dialog box
root = tk.Tk()
root.withdraw()

# initialize modifiers
drumsMod = 1
vocalsMod = 1
bassMod = 1
otherMod = 1
peakingMod = 1
lastCall = datetime.datetime.now()

def incMod(modvar):
    modvar += (0 if modvar >= 1 else 0.05)
    return modvar

def decMod(modvar):
    modvar -= (0 if modvar <= 0 else 0.05)
    return modvar

def toggleMod(modvar):
    global lastCall
    now = datetime.datetime.now()
    if float(str(now - lastCall).split(":")[-1]) > 0.2:
        modvar = 0 if modvar >= 1 else 1
        lastCall = now
    return modvar

def callback(in_data, frame_count, time_info, status):
    global drumsMod, vocalsMod, bassMod, otherMod, keypress, start, peakingMod
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
    if keyboard.is_pressed('z'):
        drumsMod = toggleMod(drumsMod)
    elif keyboard.is_pressed('x'):
        vocalsMod = toggleMod(vocalsMod)
    elif keyboard.is_pressed('c'):
        bassMod = toggleMod(bassMod)
    elif keyboard.is_pressed('v'):
        otherMod = toggleMod(otherMod)
    print("\033[F"*5) # go up 5 lines
    print(
        f'drumMod:   {drumsMod:.2f}',
        f'vocalsMod: {vocalsMod:.2f}',
        f'bassMod:   {bassMod:.2f}',
        f'otherMod:  {otherMod:.2f}',
        sep="\n")
    drums = drumsWF.readframes(frame_count)
    vocals = vocalsWF.readframes(frame_count)
    bass = bassWF.readframes(frame_count)
    other = otherWF.readframes(frame_count)
    decodedDrums = numpy.frombuffer(drums, numpy.int16)
    decodedVocals = numpy.frombuffer(vocals, numpy.int16)
    decodedBass = numpy.frombuffer(bass, numpy.int16)
    decodedOther = numpy.frombuffer(other, numpy.int16)
    
    newdata = ((decodedDrums*drumsMod)*peakingMod + (decodedVocals*vocalsMod)*peakingMod + (decodedBass*bassMod)*peakingMod + (decodedOther*otherMod)*peakingMod).astype(numpy.int16)
    return (newdata.tobytes(), pyaudio.paContinue)

if __name__ == "__main__":
    cursor.hide()

    print("[+] Asking for song directory...")
    targetDir = filedialog.askdirectory(initialdir = cwd)
    songName = targetDir.split('/')[-1]

    try:
        drumsWF = wave.open(os.path.join(targetDir,"drums.wav"), "rb")
        vocalsWF = wave.open(os.path.join(targetDir, "vocals.wav"),"rb")
        bassWF = wave.open(os.path.join(targetDir,"bass.wav"),"rb")
        otherWF = wave.open(os.path.join(targetDir,"other.wav"),"rb")

    except:
        print("[-] Error opening files.")
        cursor.show()
        exit()
    
    try:
        with open(os.path.join(targetDir, "peaking.txt")) as f:
            peakingMod = float(f.read())
            print(f"[+] Peaking modifier set to {peakingMod}")
    except:
        print(f"[-] No peaking modifer found, using 1.")

    stream = p.open(format=p.get_format_from_width(drumsWF.getsampwidth()),
                    channels=drumsWF.getnchannels(),
                    rate=drumsWF.getframerate(),
                    output=True,
                    stream_callback=callback,
                    start=True)

    try:
        print("[+] Starting stream...")
        print(f"[+] Now playing {songName}...")
        print("\n"*4, end="") # create space for mod
        stream.start_stream()
        while True:
            if not stream.is_active():
                stream.stop_stream()
                stream.close()
                p.terminate()
                cursor.show()
                break

    except KeyboardInterrupt:
        print("[+] Keyboard interrupt received... ending stream...")
        stream.stop_stream()
        stream.close()
        p.terminate()
        cursor.show()
        exit()