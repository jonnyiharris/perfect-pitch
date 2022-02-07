import os
import random
import time
import pyttsx3
import numpy as np
import wave
from scipy.io.wavfile import write

NUM_NOTES_IN_RANDOM_SEQ=500

DURATION=10.0 # seconds
FIRST_OCTAVE=3
LAST_OCTAVE=5

all_notes=["C", "C sharp", "D", "E flat", "E", "F", "F sharp", "G", "A flat", "A", "B flat", "B" ]
generate_notes=["C", "D", "E", "F", "G", "A", "B" ]

A4=440
A0=A4/(2**4)
C0=A0/(2**(9/12))

def get_note_frequency(note,number):
    note_index=all_notes.index(note)
    
    freq0=C0*(2**(note_index/12))

    return freq0*(2**number)

def get_filename(note,number):
    return f'{note} {number}.wav'.replace(" ","-")

def generate_tone_file(note,number):
    if os.path.exists(get_filename(note,number)):
        return
# generate the tone
    volume = 1.0
    fs = 22050
    f = get_note_frequency(note,number)
    print(f)

    samples = (np.sin(2*np.pi*np.arange(fs*DURATION)*f/fs)).astype(np.float32)
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
    outfile = get_filename(note,number)

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




# MAIN

# generate all of the note files
for note in all_notes:
    for octave in range(FIRST_OCTAVE,LAST_OCTAVE+1):
        generate_tone_file(note, octave)

sequence=[]
for i in range(NUM_NOTES_IN_RANDOM_SEQ):
    note=random.choice(generate_notes)
    octave=random.randrange(FIRST_OCTAVE,LAST_OCTAVE+1)
    w = wave.open(get_filename(note,octave),'rb')
    sequence.append( [w.getparams(), w.readframes(w.getnframes())] )
    w.close()

output = wave.open("sequence.wav",'wb')
output.setparams(sequence[0][0])
for i in range(len(sequence)):
    output.writeframes(sequence[i][1])
output.close
