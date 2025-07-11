import speech_recognition as sr

def get_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak now...")
        audio = r.listen(source)
    try:
        print("🧠 Recognizing...")
        query = r.recognize_google(audio, language='hi-IN')  # Hindi + English
        return query
    except sr.UnknownValueError:
        return "Sorry, I could not understand the voice clearly."
    except sr.RequestError as e:
        return f"Speech recognition failed: {e}"
