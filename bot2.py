import telebot
import csv
from telebot import types
import os
from dotenv import load_dotenv
import re

load_dotenv()

# Ваш токен от BotFather
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN не найден. Убедитесь, что он установлен в переменных окружения.")

bot = telebot.TeleBot(TOKEN)

# Файл для сохранения данных
DATA_FILE = "sections.csv"

# Максимальная вместимость секций
sections = {
    "Актерское мастерство": {
        "дни": "пн/ср/пт",
        "возраст": "3-4-5 классы",
        "количество": 24,
        "ссылка": "https://chat.whatsapp.com/LEUOjMN2E8dIvBsxX2Nb11"
    },
    "Хореография": {
        "дни": "вт/чт",
        "возраст": "0-1-2 классы",
        "количество": 24,
        "ссылка": "https://chat.whatsapp.com/If9BAqB4CgY8AsflR57kmX"
    },
    "Борьба": {
        "дни": "пн/ср/пт",
        "возраст": "микс",
        "количество": 24,
        "ссылка": "https://chat.whatsapp.com/C1Vot2BJo6I5eS57r1Y2du"
    },
    "Китайский": {
        "дни": "пн",
        "возраст": "3-4-5 классы",
        "количество": 14,
        "ссылка": "https://chat.whatsapp.com/BW9gLYX1Qzs35jPV670mdW"
    },
    "Изо младшая": {
        "дни": "вт/чт",
        "возраст": "0-1-2 классы",
        "количество": 14,
        "ссылка": "https://chat.whatsapp.com/KQkCZzoRbliGldnG0MgMgv"
    },
    "Изо старшая": {
        "дни": "ср/пт",
        "возраст": "3-4-5 классы",
        "количество": 14,
        "ссылка": "https://chat.whatsapp.com/CKdG9JvO7XgJD4xAFtSxtw"
    },
    "Шахматы": {
        "дни": "пн/ср/пт",
        "возраст": "микс",
        "количество": 18,
        "ссылка": "https://chat.whatsapp.com/KHOVvvtSt8FJtFguwvZD1L"
    },
    "Нейрогимнастика": {
        "дни": "вт/чт",
        "возраст": "микс",
        "количество": 18,
        "ссылка": "https://chat.whatsapp.com/Fl8fS9LeGMl10cTNRqrfEu"
    },
    "Ораторское искусство": {
        "дни": "пн/ср/пт",
        "возраст": "3-4 классы",
        "количество": 18,
        "ссылка": "https://chat.whatsapp.com/HD7WxhGVTLbLaMXjmyGkyM"
    },
    "Ораторское искусство мл": {
        "дни": "вт/чт",
        "возраст": "0-1-2 классы",
        "количество": 18,
        "ссылка": "https://chat.whatsapp.com/LaUFheTcnVV1toiczmnmKn"
    },
    "Арабский продвинутый": {
        "дни": "пн",
        "возраст": "3-4-5 классы",
        "количество": 14,
        "ссылка": "https://chat.whatsapp.com/KNT40biy9vWK3AyNH1FIl4"
    },
    "Арабский начинающий": {
        "дни": "ср",
        "возраст": "0-1-2 классы",
        "количество": 14,
        "ссылка": "https://chat.whatsapp.com/KkTvLX3WUKS5sbLaUkZsuw"
    },
    "Ментальная": {
        "дни": "вт/чт",
        "возраст": "микс",
        "количество": 14,
        "ссылка": "https://chat.whatsapp.com/CK6u8lrFBi9Jz2p5K3Ov1t"
    },
    "Китайский младшая": {
        "дни": "пт",
        "возраст": "0-1-2 классы",
        "количество": 14,
        "ссылка": "https://chat.whatsapp.com/FxKhEGUJp8qItjxhFQ1RQe"
    },
    "Разговорный английский про": {
        "дни": "пн/ср/пт",
        "возраст": "3-4-5 классы",
        "количество": 18,
        "ссылка": "https://chat.whatsapp.com/LXRksvRprSN5UlR1PaE2Do"
    },
    "Разговорный английский": {
        "дни": "вт/чт",
        "возраст": "0-1-2 классы",
        "количество": 18,
        "ссылка": "https://chat.whatsapp.com/J0XLBz5aQ1P56AnzBO7Q6W"
    },
    "Тхэквандо": {
        "дни": "вт/чт",
        "возраст": "микс",
        "количество": 20,
        "ссылка": "https://chat.whatsapp.com/CaSuP7PusQL8CAVJjdheW0"
    }
}


def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            data = [row for row in reader if len(row) == 3]
        return data
    except FileNotFoundError:
        return []


def save_data(full_name, school_class, section):
    with open(DATA_FILE, "a", encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([full_name, school_class, section])


def count_section(section):
    data = load_data()
    return sum(1 for row in data if row[2] == section)


def get_user_sections(full_name):
    data = load_data()
    return [row[2] for row in data if row[0] == full_name]


def extract_class_level(school_class):
    # Извлекаем первую цифру класса
    match = re.search(r'^(\d+)', school_class)
    return match.group(1) if match else None


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id,
                     "Добро пожаловать! Введите ФИО и класс через запятую (например: Иванов Иван Иванович, 7Б).")
    bot.register_next_step_handler(message, get_user_data)
    print(message.chat.id)


def validate_full_name(full_name):
    # Проверка, что ФИО содержит как минимум один пробел (минимум 2 слова)
    if len(full_name.split()) < 2:
        return False

    # Проверка, что ФИО содержит только буквы и пробелы
    if not re.match(r'^[А-Яа-яЁё\s]+$', full_name):
        return False

    return True


def validate_school_class(school_class):
    # Проверка, что класс содержит только цифры
    if not re.match(r'^\d+[А-Яа-яЁё]?$', school_class):
        return False

    # Проверка диапазона классов (обычно 1-11)
    try:
        class_number = int(re.search(r'^\d+', school_class).group())
        if class_number < 0 or class_number > 11:
            return False
    except:
        return False

    return True


def is_section_available_for_class(section_details, class_level):
    # Если возраст указан как "микс", секция доступна для любых классов
    if section_details['возраст'] == 'микс':
        return True
    # Если возраст указан списком классов (как в предыдущей версии)
    if isinstance(section_details['возраст'], list):
        return class_level in section_details['возраст']
    # Если возраст указан диапазоном строкой (например, "0-1-2 классы")
    if isinstance(section_details['возраст'], str):
        # Извлекаем числа из строки возраста
        age_range = re.findall(r'\d+', section_details['возраст'])
        return class_level in age_range
    return False


def get_user_data(message):
    if not message or not message.text:
        bot.send_message(message.chat.id, "Произошла ошибка. Пожалуйста, введите данные в формате: ФИО, класс.")
        bot.register_next_step_handler(message, get_user_data)
        return

    user_data = message.text.strip()
    if "," not in user_data:
        bot.send_message(message.chat.id,
                         "Пожалуйста, убедитесь что вы поставили запятую после ФИО. Введите данные в формате: ФИО, класс.")
        bot.register_next_step_handler(message, get_user_data)
        return

    full_name, school_class = map(str.strip, user_data.split(",", 1))

    # Валидация ФИО
    if not validate_full_name(full_name):
        bot.send_message(message.chat.id,
                         "Пожалуйста, введите полное ФИО (минимум 2 слова). Используйте только русские буквы.")
        bot.register_next_step_handler(message, get_user_data)
        return

    # Валидация класса
    if not validate_school_class(school_class):
        bot.send_message(message.chat.id, "Пожалуйста, введите корректный класс (например, 7А или 11).")
        bot.register_next_step_handler(message, get_user_data)
        return

    # Извлекаем уровень класса
    class_level = extract_class_level(school_class)

    if not class_level:
        bot.send_message(message.chat.id, "Не удалось определить класс. Убедитесь, что указан корректный класс.")
        bot.register_next_step_handler(message, get_user_data)
        return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    # Фильтруем секции по возрасту
    available_sections = [
        section for section, details in sections.items()
        if is_section_available_for_class(details, class_level)
    ]

    for section in available_sections:
        filled = count_section(section)
        days = sections[section]['дни']
        max_capacity = sections[section]['количество']
        keyboard.add(f"{section}, {days} ({filled}/{max_capacity})")

    if not available_sections:
        bot.send_message(message.chat.id, "Для вашего класса нет доступных секций.\n/start")
        return

    bot.send_message(message.chat.id, "Выберите секцию:", reply_markup=keyboard)
    bot.register_next_step_handler(message, lambda msg: register_user(msg, full_name, school_class))

    # Дальнейший код без изменений...


def register_user(message, full_name, school_class):
    if not message or not message.text:
        bot.send_message(message.chat.id, "Произошла ошибка. Пожалуйста, выберите секцию.")
        return

    # Разбиваем текст на название секции и дни
    selected_section_info = message.text.split(", ")

    if len(selected_section_info) < 2:
        bot.send_message(message.chat.id, "Неверный формат выбора секции.")
        return

    # Извлекаем название секции (первая часть до запятой)
    selected_section = selected_section_info[0]

    # Проверяем наличие секции в списке
    if selected_section not in sections:
        bot.send_message(message.chat.id, "Неверный выбор. Пожалуйста, выберите секцию из списка.")
        return

    user_sections = get_user_sections(full_name)

    # Проверка на повторную запись в секцию
    if selected_section in user_sections:
        bot.send_message(message.chat.id, f"Вы уже записаны в секцию {selected_section}.\n/start",
                         reply_markup=types.ReplyKeyboardRemove())
        return

    # Проверка количества секций
    if len(user_sections) >= 3:
        bot.send_message(message.chat.id, "Вы уже записаны в 3 секции.\n/start",
                         reply_markup=types.ReplyKeyboardRemove())
        return

    # Проверка заполненности секции
    if count_section(selected_section) >= sections[selected_section]['количество']:
        bot.send_message(message.chat.id, "Извините, эта секция уже заполнена.\n/start")
        return

    # Сохраняем данные
    save_data(full_name, school_class, selected_section)

    # Получаем ссылку для секции
    section_link = sections[selected_section].get('ссылка', 'Ссылка не указана')

    # Формируем подробное сообщение
    response_message = (
        f"Вы успешно записаны в {selected_section}!\n\n"
        f"Дни занятий: {sections[selected_section]['дни']}\n"
        f"Ссылка: {section_link}\n\n"
        "/start"
    )

    bot.send_message(message.chat.id, response_message,
                     reply_markup=types.ReplyKeyboardRemove())

ADMIN_IDS = [515202835, 1159140776]


# Команда /export_data для выгрузки данных
@bot.message_handler(commands=["export_data"])
def export_data(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")
        return

    # Выгрузка данных из файла
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as file:
            bot.send_document(message.chat.id, file)
    else:
        bot.send_message(message.chat.id, "Файл с данными не найден.")

    # Удаление данных
@bot.message_handler(commands=["delete_data"])
def delete_data(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")
        return

    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
        bot.send_message(message.chat.id, "Данные успешно удалены.")
    else:
        bot.send_message(message.chat.id, "Файл с данными не найден.")


if __name__ == "__main__":
    bot.polling()