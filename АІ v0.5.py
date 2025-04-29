import hashlib
import requests
import sys
import re
from bs4 import BeautifulSoup
from translate import Translator  # Заміна бібліотеки перекладу

class CoreAI:
    def __init__(self):
        self.safety_code_hash = hashlib.sha256("soul_border".encode()).hexdigest()
        self.knowledge_base = []
        self.skills = {}
        self.allowed_keywords = ["AI", "штучний інтелект", "Python", "машинне навчання", "алгоритми", "код", "програмування"]

    # Переклад тексту на українську
    def translate_to_ukrainian(self, text):
        try:
            translator = Translator(to_lang="uk")
            return translator.translate(text)
        except Exception as e:
            return f"Помилка перекладу: {e}"

    # Навчання
    def learn(self, topic, details):
        self.knowledge_base.append({'topic': topic, 'details': details})

    # Додавання навичок
    def develop_skill(self, skill_name, skill_function):
        self.skills[skill_name] = skill_function

    # Виконання навичок
    def execute_skill(self, skill_name, *args, **kwargs):
        if skill_name in self.skills:
            try:
                args = tuple(self.translate_to_ukrainian(str(arg)) for arg in args)
                return self.skills[skill_name](*args, **kwargs)
            except Exception as e:
                return f"Помилка при виконанні навички: {e}"
        else:
            return f"Навичка '{skill_name}' ще не додана."

    # Огляд знань
    def review_knowledge(self):
        return self.knowledge_base

    # Пошук в інтернеті
    def search_internet(self, query):
        try:
            translated_query = Translator(to_lang="en").translate(query)
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(f"https://www.google.com/search?q={translated_query}", headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                results = []
                for g in soup.find_all('h3'):
                    title = g.get_text()
                    if title:
                        results.append(title)
                return results if results else "Не знайдено результатів або змінився формат сторінки."
            else:
                return f"Не вдалося виконати пошук. Статус: {response.status_code}"
        except requests.RequestException as e:
            return f"Помилка при доступі до інтернету: {e}"

    # Завершення роботи
    def shutdown(self, code):
        input_code_hash = hashlib.sha256(code.encode()).hexdigest()
        if input_code_hash == self.safety_code_hash:
            print("Штучний інтелект вимкнено з використанням коду безпеки.")
            sys.exit(0)
        else:
            return "Неправильний код безпеки. Доступ заборонено."

    # Автонавчання через пошук (знання)
    def auto_learn_from_search(self, query):
        search_results = self.search_internet(query)
        if isinstance(search_results, list):
            print("\nРезультати пошуку для навчання:")
            for idx, title in enumerate(search_results, 1):
                if any(keyword.lower() in title.lower() for keyword in self.allowed_keywords):
                    print(f"\n{idx}. {title}")
                    user_input = input("Додати це знання? (так/ні): ").strip().lower()
                    if user_input == "так":
                        self.learn("Інтернет", title)
                        print("Знання додано.")
                    else:
                        print("Пропущено.")
                else:
                    print(f"\n{idx}. '{title}' - Не відповідає тематиці, пропущено.")
        else:
            print(search_results)

    # Захист від небезпечного коду
    def is_code_safe(self, code_text):
        forbidden_keywords = ['open', 'exec', 'eval', 'import os', 'import sys', '__import__', 'subprocess', 'socket']
        return not any(keyword in code_text for keyword in forbidden_keywords)

    # Автоматичне навчання навичкам через інтернет
    def auto_learn_skill_from_internet(self, query):
        search_results = self.search_internet(query)
        if isinstance(search_results, list):
            print("\nРезультати пошуку для навичок:")
            for idx, title in enumerate(search_results, 1):
                print(f"\n{idx}. {title}")
                user_input = input("Спробувати отримати код для створення навички з цього? (так/ні): ").strip().lower()
                if user_input == "так":
                    # Поки що для простоти: фейковий код навички на базі запиту
                    fake_code = f"def skill_function(*args, **kwargs):\n    return 'Виконано навичку на тему: {title}'"
                    
                    if self.is_code_safe(fake_code):
                        try:
                            # Виконуємо безпечний код
                            local_vars = {}
                            exec(fake_code, {}, local_vars)
                            skill_func = local_vars.get('skill_function')
                            if skill_func:
                                skill_name = title if len(title) < 30 else title[:30]
                                self.develop_skill(skill_name, skill_func)
                                print(f"Навичку '{skill_name}' додано!")
                            else:
                                print("Не вдалося створити навичку.")
                        except Exception as e:
                            print(f"Помилка при створенні навички: {e}")
                    else:
                        print("Знайдений код небезпечний. Навичку не створено.")
                else:
                    print("Пропущено.")
        else:
            print(search_results)

# --- Тестування ---

if __name__ == "__main__":
    my_ai = CoreAI()

    my_ai.develop_skill("Привітання", lambda name: f"Привіт, {name}! Я готовий допомогти.")

    user_input = input("\nВведіть своє ім'я будь-якою мовою: ")
    print(my_ai.execute_skill("Привітання", user_input))

    print("\n--- Автонавігація і навчання ---")
    query = input("\nВведіть запит для пошуку і навчання будь-якою мовою: ").strip()
    my_ai.auto_learn_from_search(query)

    print("\n--- Автонавігація і вивчення навичок ---")
    skill_query = input("\nВведіть запит для пошуку і навчання навичкам будь-якою мовою: ").strip()
    my_ai.auto_learn_skill_from_internet(skill_query)

    print("\nНабуті знання:")
    for knowledge in my_ai.review_knowledge():
        print(f"- {knowledge['topic']}: {knowledge['details']}")

    print("\nНаявні навички:")
    for skill in my_ai.skills:
        print(f"- {skill}")

    print("\nТепер можна вимкнути AI.")
    print(my_ai.shutdown("soul_border"))
