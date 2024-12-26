import speech_recognition as sr
from gtts import gTTS
import os
from datetime import datetime
from playsound import playsound
import google.generativeai as genai
from django.http import JsonResponse
import threading
from django.shortcuts import render
from datetime import datetime

class SpeechRecognitionSystem:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.is_active = False
        self.conversation_history = []
        self.commands = {
            "hallo": self.say_hello,
            "wie heißt du": self.tell_name,
            "auf wiedersehen": self.say_goodbye,
            "danke": self.say_welcome,
            "was ist Literatur": self.say_about_literature,
            "aufsatz": self.generate_essay
        }
        
        genai.configure(api_key='AIzaSyAHcj6-yuym_aFmj10WVIZdNH9VTYWBCAY')
        self.model = genai.GenerativeModel('gemini-pro')

    def speak(self, text):
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.conversation_history.append({
            'speaker': 'System',
            'message': text,
            'timestamp': timestamp
        })
        tts = gTTS(text=text, lang='de')
        audio_file = "temp_audio.mp3"
        tts.save(audio_file)
        playsound(audio_file)
        os.remove(audio_file)
    
    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            
        try:
            text = self.recognizer.recognize_google(audio, language="fr-FR")
            timestamp = datetime.now().strftime('%H:%M:%S')
            self.conversation_history.append({
                'speaker': 'User',
                'message': text,
                'timestamp': timestamp
            })
            return text.lower()
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            self.speak("Haben Problemen mit dem Server.")
            return None

    def say_hello(self):
        self.speak("Guten Tag") 
        
    def say_goodbye(self):
        self.speak("Auf Wiedersehen!") 
        
    def tell_name(self):
        self.speak(f"Ich hab kein Name, aber du kannst mich Gepanzertekriegsschildkröte nennen") 

    def say_welcome(self):
        self.speak("Ich habe dir gern geholfen!")

    def say_about_literature(self):
        self.speak("Literatur ist eine Sammlung schriftlicher Werke, in denen wir einen ästhetischen Zweck sehen..")

    def generate_essay_async(self, topic):
        try:
            prompt = f"""Schreiben Sie einen gut strukturierten Aufsatz auf Deutsch zum Thema: {topic}
            Der Aufsatz muss enthalten:
            - Eine Einführung
            - 2-3 Hauptargumente
            - Eine Schlussfolgerung
            Länge: ca. 250 Wörter"""
            
            response = self.model.generate_content(prompt)
            essay = response.text

            self.conversation_history.append({
                'speaker': 'System',
                'message': essay,
                'timestamp': datetime.now().strftime('%H:%M:%S')
            })
           
            print('essay', essay)
        except Exception as e:
            self.speak("Es gibt ein Fehler, du bekommst nicht dein Aufsatz.") 
            print(f"Fehler: {e}")

    def generate_essay(self):
        self.speak("Über welches Thema soll ich einen Aufsatz schreiben?")
        topic = self.listen()
        if topic:
            self.speak("Bitte warte ein paar Minuten...")
            thread = threading.Thread(target=self.generate_essay_async, args=(topic,))
            thread.start()
        else:
            self.speak("Bitte wiederhole das Thema")

    def run(self):
        self.speak("Ich bin bereit zu unterhalten") 
        self.is_active = True
        while self.is_active:
            text = self.listen()
            
            if text:
                for command, action in self.commands.items():
                    if command in text:
                        result = action()
                        if result == "exit":
                            return

speech_system = SpeechRecognitionSystem()

def speech_recognition(request):
    return render(request, 'speech_recognition.html')

def start_recognition(request):
    if not speech_system.is_active:
        thread = threading.Thread(target=speech_system.run)
        thread.start()
        return JsonResponse({'status': 'started'})
    return JsonResponse({'status': 'already running'})

def stop_recognition(request):
    speech_system.is_active = False
    return JsonResponse({'status': 'stopped'})

def get_conversations(request):
    return JsonResponse({'conversations': speech_system.conversation_history})