from IPython.display import Javascript, display
from google.colab import output
from base64 import b64decode
from pydub import AudioSegment
import speech_recognition as sr
import librosa
import numpy as np
import time

AudioSegment.converter = "/usr/bin/ffmpeg"

threshold = 35
max_attempts = 10
attempts = 0

recognizer = sr.Recognizer()

def speak(text):
    print(text)

RECORD = """
async function recordAudio() {
  const stream = await navigator.mediaDevices.getUserMedia({audio:true});
  const recorder = new MediaRecorder(stream);
  const chunks = [];

  recorder.ondataavailable = e => chunks.push(e.data);

  alert("Recording will start now. Speak for 4 seconds.");

  recorder.start();

  await new Promise(resolve => setTimeout(resolve, 4000));

  recorder.stop();

  await new Promise(resolve => recorder.onstop = resolve);

  const blob = new Blob(chunks, {type: 'audio/webm'});
  const buffer = await blob.arrayBuffer();
  const base64 = btoa(String.fromCharCode(...new Uint8Array(buffer)));

  return base64;
}
"""

display(Javascript(RECORD))

def record_audio(filename):
    audio_data = output.eval_js("recordAudio()")
    audio_bytes = b64decode(audio_data)

    webm_filename = filename.replace(".wav", ".webm")

    with open(webm_filename, "wb") as f:
        f.write(audio_bytes)

    audio = AudioSegment.from_file(webm_filename)
    audio.export(filename, format="wav")

def extract_feature(filename):
    audio, sr_rate = librosa.load(filename, sr=16000)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr_rate, n_mfcc=13)
    feature = np.mean(mfcc, axis=1)
    return feature

def speech_to_text(filename):
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except:
        print("Could not recognize speech")
        return ""


print("\n--- User Registration ---")
speak("Hi, my name is Apple")
time.sleep(1)
speak("First, register your voice as password")
time.sleep(1)
speak("Recording will automatically start for 4 seconds")

record_audio("registered_voice.wav")

registered_text = speech_to_text("registered_voice.wav")
registered_feature = extract_feature("registered_voice.wav")

stored_password = input("Create your backup password: ")

speak("Voice registration completed successfully")


while attempts < max_attempts:
    print(f"\n--- Voice Authentication Attempt {attempts + 1} ---")

    speak("Please speak for authentication")
    record_audio("test_voice.wav")

    test_text = speech_to_text("test_voice.wav")
    test_feature = extract_feature("test_voice.wav")

    distance = np.linalg.norm(registered_feature - test_feature)
    print("Voice Distance:", distance)

    if distance < threshold:
        speak("Access Granted. Voice matched successfully")
        print("Access Granted - Voice Matched")
        break
    else:
        attempts += 1
        remaining = max_attempts - attempts

        speak(f"Password did not match. {remaining} attempts remaining")
        print("Voice Not Matched")


if attempts == max_attempts:
    speak("Maximum voice attempts reached")

    entered_password = input("Enter Backup Password: ")

    if entered_password == stored_password:
        speak("Access Granted. Backup password correct")
        print("Access Granted - Password Correct")
    else:
        speak("Access Denied. Wrong backup password")
        print("Access Denied - Wrong Password")
