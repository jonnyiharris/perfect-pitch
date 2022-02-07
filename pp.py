import time
import pyttsx3
import numpy as np
import wave
from scipy.io.wavfile import write

all_notes=["C", "C sharp", "D", "E flat", "E", "F", "F sharp", "G", "A flat", "A", "B flat", "B" ]

A4=440
A0=A4/(2**4)
C0=A0/(2**(9/12))

def get_note_frequency(note,number):
    note_index=all_notes.index(note)
    
    freq0=C0*(2**(note_index/12))

    return freq0*(2**number)

def generate_tone_file(note,number):
# generate the tone
    volume = 1.0
    fs = 22050
    duration = 5.0
    f = get_note_frequency(note,number)
    print(f)

    samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)
    scaled = np.int16(samples/np.max(np.abs(samples)) * 2**15)
    write('tone.wav',fs,scaled)

# generate the note name
    note_name = f'{note} {number}'
    engine = pyttsx3.init()
    engine.save_to_file(note_name,"note.wav")
    engine.runAndWait()
    time.sleep(1)

# concatenate the tone and the note name
    infiles = ["tone.wav", "note.wav"]
    outfile = note_name.replace(' ','-')+".wav"

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

for note in all_notes:
    for octave in range(1,8):
        generate_tone_file(note, octave)
