import time
import pyttsx3
import numpy as np
import wave
from scipy.io.wavfile import write


# generate the tone
volume = 1.0
fs = 22050
duration = 5.0
f = 440

samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)
scaled = np.int16(samples/np.max(np.abs(samples)) * 2**15)
write('tone.wav',fs,scaled)

# generate the note name
engine = pyttsx3.init()
engine.save_to_file("C 4","note.wav")
engine.runAndWait()
time.sleep(1)

# concatenate the tone and the note name
infiles = ["tone.wav", "note.wav"]
outfile = "c4.wav"

data=[]

for infile in infiles:
    w = wave.open(infile,'rb')
    data.append( [w.getparams(), w.readframes(w.getnframes())] )
    w.close()

# write the tone with name
output = wave.open(outfile,'wb')
output.setparams(data[0][0])
for i in range(len(data)):
    output.writeframes(data[i][1])
output.close