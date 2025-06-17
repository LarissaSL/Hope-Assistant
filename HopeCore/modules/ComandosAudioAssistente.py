from playsound import playsound
import speech_recognition as sr
import pyttsx3

class AudioAssistente:

    def speak(self, texto, logger=None):
        engine = pyttsx3.init()
        engine.setProperty('rate', 180)
        engine.setProperty('volume', 1)
        engine.say(texto)
        engine.runAndWait()
        self.logger = logger

    def listen_microphone(self, timeout=5, phrase_time_limit=3):
        microfone = sr.Recognizer()

        with sr.Microphone() as source:
            microfone.adjust_for_ambient_noise(source, duration=0.8)
            print('Ouvindo:')
            try:
                audio = microfone.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                with open('HopeCore/recordings/speech.wav', 'wb') as f:
                    f.write(audio.get_wav_data())
            except sr.WaitTimeoutError:
                print('Tempo esgotado - nenhuma fala detectada')
                return ''

        try:
            frase = microfone.recognize_google(audio, language='pt-BR')
            print('Você disse: ' + frase)
        except sr.UnknownValueError:
            frase = ''
            print('Não entendi')
        return frase

    def listen_microphone_extended(self ):
        return self.listen_microphone(timeout=10, phrase_time_limit=8)