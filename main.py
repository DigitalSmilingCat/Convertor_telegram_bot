import telebot
from extensions import APIException, Convertor
from config import TOKEN, abbreviations
import traceback
from re import sub

bot = telebot.TeleBot(TOKEN)  # Создаем телеграм-бота по токену


@bot.message_handler(commands=['start', 'help'])  # Выводим инструкцию для команд /start и /help
def start(message: telebot.types.Message):
    text = "Для указания валют можно использовать наименования на русском языке или трехбуквенные коды на латинице. " \
           "Для перевода валюты укажите через запятую:\n<Из какой валюты нужно перевести>, " \
           "<В какую валюту нужно перевести>, <Количество переводимой валюты>\n\n" \
           "Для вывода списка доступных валют используйте команду /values"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])  # Выводим доступные валюты по команде /values
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for k, v in abbreviations.items():
        text = '\n'.join((text, f'{k} ({v})'))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])  # Обрабатываем текст на корректность введенных данных
def convert(message: telebot.types.Message):
    # Убираем пробелы и прочие лишние символы, если пользователь неправильно понял формат ввода
    values = sub("""<|>| |'|"|""", '', message.text).split(',', 2)  # Разбиваем на слова по двум ',', не трогая в числе
    try:
        if len(values) != 3:  # Вызываем ошибку, если количество слов не равно 3
            raise APIException('Неверное количество параметров! Используйте запятые!')
        answer = Convertor.get_price(*values)  # Вызываем метод, который должен вернуть результат конвертации
    except APIException as e:  # Выводим текст ошибки для введенного текста
        bot.reply_to(message, f'Ошибка в команде:\n{e}')
    except Exception as e:  # Выводим текст ошибки, если она связанна с внешними факторами
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f'Неизвестная ошибка:\n{e}')
    else:
        bot.reply_to(message, answer)  # Выводим пользователю результат конвертации


bot.polling()  # После запуска программы бот будет постоянно проверять новые запросы от телеграма
