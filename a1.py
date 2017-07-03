import speech_recognition as sr
 
AUDIO_FILE = ("t1 (online-audio-converter.com).wav")
 
# use the audio file as the audio source
 
r = sr.Recognizer()
 
with sr.AudioFile(AUDIO_FILE) as source:
    #reads the audio file. Here we use record instead of
    #listen
    audio = r.record(source)  
 
try:
    w=r.recognize_google(audio)
    f=open("nemo.txt","w")
    f.write(w)
    f.close()
 
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
 
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
