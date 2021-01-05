import speech_recognition as sr
import time

r = sr.Recognizer()
keywords = [("jarvis",1),("hey jarvis",1)]
source = sr.Microphone()
def callback(recognizer, audio):  # this is called from the background thread
	try:
		speech_as_text = r.recognize_sphinx(audio, keyword_entries=keywords)
		print(speech_as_text)
		# Look for your "Ok Google" keyword in speech_as_text
		if "jarvis" in speech_as_text or "hey jarvis":
			recognize_main()
			pass

	except sr.UnknownValueError:
		pass

def recognize_main():
	print("Recognizing Main...")
	audio_data = r.listen(source)
	response = r.recognize_google(audio_data)

    # interpret the user's words however you normally interpret them

def start_recognizer():
	r.listen_in_background(source,callback)

start_recognizer()
