import speech_recognition as sr
import pyttsx3

# pip install SpeechRecognition pyttsx3
# pip install setuptools
# pip install pipwin
# pip install pyaudio
# pip install looseversion

# Inicializar el motor de síntesis de voz
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

# Función para que el asistente hable
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Inicializar el reconocimiento de voz
recognizer = sr.Recognizer()

# Función para escuchar y reconocer la voz
def listen():
    with sr.Microphone() as source:
        print("Escuchando...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            print("Reconociendo...")
            command = recognizer.recognize_google(audio, language='es-ES')
            print(f"Tú dijiste: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Lo siento, no te entendí. ¿Podrías repetirlo?")
            return None
        except sr.RequestError as e:
            speak("Lo siento, hubo un error con el servicio de reconocimiento de voz.")
            return None

# Función principal para manejar los comandos
def handle_command(command):
    if command is None:
        return True  # Continúa escuchando

    if 'hola' in command:
        speak("Hola, ¿cómo estás?")
    elif 'cómo te llamas' in command:
        speak("Soy tu asistente virtual.")
    elif 'adiós' in command:
        speak("Adiós, ¡que tengas un buen día!")
        return False  # Detiene el bucle principal
    else:
        speak("Lo siento, no entiendo ese comando.")
    
    return True  # Continúa escuchando

# Bucle principal del asistente
def main():
    speak("Hola, soy tu asistente virtual. ¿En qué puedo ayudarte?")
    while True:
        command = listen()
        if command is None:
            continue  # Si no se entendió el comando, seguir escuchando
        if not handle_command(command):
            break

if __name__ == "__main__":
    main()