import os
import datetime
import psutil
import glob
import tkinter as tk
from tkinter import simpledialog
from gtts import gTTS
import pygame
import tempfile
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Ініціалізація pygame для звуку
pygame.init()
pygame.mixer.init()

# Шлях до файлу для збереження пам'яті
memory_file = "memory.json"

# Завантаження пам'яті з файлу
def load_memory():
    if os.path.exists(memory_file):
        with open(memory_file, "r") as f:
            return json.load(f)
    return {}

# Збереження пам'яті в файл
def save_memory(memory):
    with open(memory_file, "w") as f:
        json.dump(memory, f)

# Пам'ять Джарвіса
memory = load_memory()

# Приклад додавання інформації до пам'яті
def add_to_memory(key, value):
    memory[key] = value
    save_memory(memory)

# Використання пам'яті
def recall_from_memory(key):
    return memory.get(key, "Я не пам'ятаю.")

# Голосовий ввід
def speak(text):
    print(f"Jarvis: {text}")
    tts = gTTS(text=text, lang='uk')
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as fp:
        tts.save(fp.name)
        pygame.mixer.music.load(fp.name)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

# Пошук встановлених програм
def find_installed_programs():
    search_dirs = ["C:\\Program Files", "C:\\Program Files (x86)", "C:\\Users", "D:\\"]
    programs = {}
    for dir_path in search_dirs:
        for path in glob.glob(dir_path + "/**/*.exe", recursive=True):
            name = os.path.splitext(os.path.basename(path))[0].lower()
            programs[name] = path
    return programs

installed_programs = find_installed_programs()

# Класифікація команд за допомогою машинного навчання
training_data = [
    ("Привіт", "greeting"),
    ("Як справи?", "question"),
    ("Погода сьогодні", "question"),
    ("До побачення", "goodbye"),
    ("Вийти", "exit"),
    ("Час", "time"),
    ("Батарея", "battery")
]

texts, labels = zip(*training_data)
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)
y = labels

# Навчальна модель
model = MultinomialNB()
model.fit(X, y)

# Функція для класифікації команди
def classify_command(command):
    command_vector = vectorizer.transform([command])
    prediction = model.predict(command_vector)
    return prediction[0]

# Команди користувача
def process_command(command):
    command = command.lower()
    category = classify_command(command)

    if category == "greeting":
        speak("Привіт! Як я можу допомогти?")
    elif category == "question":
        speak("Цікаве питання!")
    elif category == "goodbye":
        speak("До побачення!")
    elif category == "exit":
        speak("До зустрічі!")
        root.quit()
    elif category == "time":
        speak("Зараз " + datetime.datetime.now().strftime("%H:%M"))
    elif category == "battery":
        battery = psutil.sensors_battery()
        if battery:
            speak(f"Заряд {int(battery.percent)} відсотків")
        else:
            speak("Не вдалося дізнатися заряд.")
    elif "запам'ятай" in command:
        memory_data = command.replace("запам'ятай", "").strip()
        add_to_memory("user_data", memory_data)
        speak(f"Я запам'ятав: {memory_data}")
    elif "що я запам'ятав" in command:
        remembered_data = recall_from_memory("user_data")
        speak(f"Ти запам'ятав: {remembered_data}")
    else:
        speak("Я поки не знаю, як це зробити.")

# Голосовий ввід
def handle_voice():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        speak("Говори команду")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio, language="uk-UA")
        process_command(command)
    except:
        speak("Не зрозумів команду.")

# Текстовий ввід
def handle_text():
    command = simpledialog.askstring("Введи команду", "Що бажаєш?")
    if command:
        process_command(command.lower())

# GUI
root = tk.Tk()
root.title("Jarvis Assistant")
root.geometry("300x250")

tk.Label(root, text="Jarvis", font=("Arial", 24)).pack(pady=10)
tk.Button(root, text="🎙 Голосова команда", font=("Arial", 14), command=handle_voice).pack(pady=10)
tk.Button(root, text="💬 Текстова команда", font=("Arial", 14), command=handle_text).pack(pady=10)
tk.Button(root, text="❌ Вихід", font=("Arial", 14), command=root.quit).pack(pady=10)

speak("Вітаю. Я Ніро.")
root.mainloop()
