import speech_recognition
import subprocess
import os
import webbrowser as wb
from gtts import gTTS
from playsound import playsound
from ru_word2number import w2n

commands = [
    ("задача", "задачи", "планировщик задач", "диспетчер задач"),
    ("панель", "настройки", "панель управления", "управление"),
    ("поиск в интернете", "поиск", "гуглить", "найди"),
    ("выход", "закончить", "прервать"),
    ("выключение", "выключить", "вырубить", "отключить"),
    ("хост", "хвост", "хосты", "редактировать хосты"),
    ("умножение", "умножить", "произведение")
]
Flag = True
def record_and_recognize_audio(*args: tuple):
    """
    Запись и распознавание аудио
    """
    with microphone:
        recognized_data = ""

        # регулирование уровня окружающего шума
        recognizer.adjust_for_ambient_noise(microphone, duration=2)

        try:
            print("Listening...")
            audio = recognizer.listen(microphone, 5, 5)

        except speech_recognition.WaitTimeoutError:
            print("Can you check if your microphone is on, please?")
            return

        # использование online-распознавания через Google
        try:
            print("Started recognition...")
            recognized_data = recognizer.recognize_google(audio, language="ru").lower()

        except speech_recognition.UnknownValueError:
            pass

        # в случае проблем с доступом в Интернет происходит выброс ошибки
        except speech_recognition.RequestError:
            print("Check your Internet Connection, please")

        return recognized_data

def openTaskManager():
    program = "Taskmgr.exe"
    process = subprocess.Popen(program)

def openPanel():
    os.system('control.exe')

def exitProgram():
    global Flag
    Flag = False

def googleInfo(request):
    wb.open("http://google.com/search?q=" + request)

if __name__ == "__main__":
    # инициализация инструментов распознавания и ввода речи
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()
    while Flag:
        # старт записи речи с последующим выводом распознанной речи
        voice_input = record_and_recognize_audio()
        print(voice_input)
        if voice_input.lower() in commands[0]:
            openTaskManager()
        elif voice_input.lower() in commands[1]:
            openPanel()
        elif voice_input.lower() in commands[3]:
            exitProgram()
        elif "поиск в интернете" in voice_input.lower():
            googleInfo(voice_input.lower()[17:])
        elif voice_input.lower() in commands[5]:
            os.system("start OpenHosts.bat")
        elif voice_input.lower() in commands[4]:
            os.system("start ShutDown.bat")
        elif voice_input.lower().split()[0] in commands[6]:
            mass = voice_input.split()
            number1 = w2n.word_to_num(mass[1])
            number2 = w2n.word_to_num(mass[3])
            text = f"Результат умножения {number1} на {number2} равен {number1*number2}"
            var = gTTS(text=text, lang='ru')
            var.save('res.mp3')
            playsound(os.getcwd() +'\\res.mp3')