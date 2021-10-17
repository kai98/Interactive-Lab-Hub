import sys
import os
import wave
import subprocess
from time import sleep
from vosk import Model, KaldiRecognizer
import json

if not os.path.exists("model"):
    print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
    exit (1)

model = Model("model")

def vosk(wordlist, filename='recorded_mono.wav'):
    record(filename)
    return wav_to_text(filename, wordlist)

def record(filename):
    command = "arecord -D hw:3,0 -f cd -c1 -r 48000 -d 5 -t wav " + filename
    subprocess.call(command, shell=True)

def wav_to_text(filename, word_list):
    wf = wave.open("./"+filename)
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        exit (1)

    word_list = ' '.join(word_list)
    word_list += "[unk]"
    rec = KaldiRecognizer(model, wf.getframerate(), word_list)
    keywords = set()

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            print(rec.Result())
        else:
            thisword = json.loads(rec.PartialResult())['partial']
            # temp = rec.PartialResult()
            words = thisword.split(' ')
            for w in words:
                keywords.add(w)
    return keywords