import subprocess
from time import sleep

def speak(msg, t=0.1):
    subprocess.call(espeak_command(msg), shell=True)
    speak_break(t)

def speak_break(t=0.1):
    sleep(t)

def espeak_command(msg):
    return "espeak -ven+f2 -s130 --stdout '" + msg + "' | aplay"
