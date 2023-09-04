import os
import telebot
from runners_list_by_alph import get_pdf as get_alph_list
from runners_list_by_number import get_pdf as get_numb_list

bot = telebot.TeleBot('6653446865:AAEXYUSUM4RPVnxaFGREbhL_gHqB4uM-5Pc')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправьте мне CSV файл(с разделителем ';' с данными участников. Таблица должна содержать следующие поля: Стартовый номер, Фамилия, Имя, Дата рождения (в формате ГГГГ-ММ-ДД).)")


@bot.message_handler(content_types=['document'])
def handle_document(message):
    try:
        # Проверяем, что полученный документ является CSV файлом
        if message.document.mime_type == 'text/csv':
            # Скачиваем файл
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            # Сохраняем файл на сервере
            file_name = message.document.file_name
            with open(file_name, 'wb') as new_file:
                new_file.write(downloaded_file)

            get_alph_list(file_name)

            get_numb_list(file_name)

            # Отправляем файл с алф.списками пользователю
            with open(f'{file_name.split(".")[0]}_by_alph.pdf', 'rb') as alph_list_file:
                bot.send_document(message.chat.id, alph_list_file)

            # Отправляем файл с номерами пользователю
            with open(f'{file_name.split(".")[0]}_by_numbers.pdf', 'rb') as numbers_list_file:
                bot.send_document(message.chat.id, numbers_list_file)

            # Удаляем временный файл
            # os.remove(file_name)
            # os.remove(f'{file_name.split(".")[0]}_by_alph.pdf')
            # os.remove(f'{file_name.split(".")[0]}_by_numbers.pdf')

        else:
            bot.reply_to(message, "Пожалуйста, отправьте файл в формате CSV.")

    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")


if __name__ == "__main__":
    bot.polling()
