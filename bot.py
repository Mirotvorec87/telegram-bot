from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# Ссылки на каталоги
catalog_links = {
    "Врач": "https://disk.yandex.ru/i/Lsx2dtEb33HpYw",
    "Минэнерго": "https://disk.yandex.ru/i/sv1IAHkXLO1ebg",
    "Космос корпоративный 2021-2022": "https://disk.yandex.ru/i/4RTw-idaNhVsCw",
    "Курчатовский": "https://disk.yandex.ru/i/PcBvuxYqMImPRA",
    "Новый год": "https://disk.yandex.ru/i/SDixCEPemz8vMQ",
    "Арктика": "https://disk.yandex.ru/i/kV5WqFTXZOGEZg",
    "Военный полный": "https://disk.yandex.ru/i/NNqRtx-TbjpbfA",
    "Каталог Газпром": "https://disk.yandex.ru/i/Hdr1CxDtMWNhng",
    "МИД": "https://disk.yandex.ru/i/0bTkAmfvbgciMg",
    "Смешанный (литье+ филигрань)": "https://disk.yandex.ru/i/OhAf0HQX8te1vA"
}

# Путь к папке с новинками
new_items_dir = "C:/telegram_project/Nowinki/27.05.2024"

# Ссылки на видео
video_links = {
    "Новогодние подарки 2023": "https://youtube.com/shorts/4slNO1n6iSY",
    "Русское народное творчество Филигрань": "https://youtu.be/H2c64OZWT8c",
    "Военные наборы": "https://youtu.be/2mPZx08gOqY",
    "Новинка лопата и термос": "https://youtu.be/VeoYpD3yBD0",
    "Зажигалки": "https://youtu.be/X5bJK3oB7wE",
    "Русское народное творчество Филигрань часть 2": "https://youtu.be/P113NXIrPu8",
    "Продай мне эту ручку": "https://youtu.be/tvIQE0k3Fps",
    "Интерстеллар (веселый)": "https://youtu.be/i5uu11dnDzk"
}

# Главное меню
def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("Каталоги", callback_data='catalogs')],
        [InlineKeyboardButton("Новинки", callback_data='new_items')],
        [InlineKeyboardButton("Видео", callback_data='videos')],
        [InlineKeyboardButton("Наш сайт", url="https://russian-filigran.ru/")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Начать", callback_data='start')]])
    await update.message.reply_text('Добро пожаловать! Нажмите кнопку "Начать" для использования бота.', reply_markup=reply_markup)

# Обработчик для нажатия кнопки "Начать"
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Выберите опцию:", reply_markup=main_menu_keyboard())

# Обработчик для кнопки "Каталоги"
async def handle_catalogs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = "Каталог продукции:\n"
    for i, (name, link) in enumerate(catalog_links.items(), 1):
        message += f"{i}. Каталог \"{name}\" - [смотреть каталог]({link})\n"
    keyboard = [[InlineKeyboardButton("Назад", callback_data='start')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text=message, parse_mode='Markdown', reply_markup=reply_markup)

# Обработчик для кнопки "Новинки"
async def handle_new_items(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    files = os.listdir(new_items_dir)
    image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    if not image_files:
        await query.edit_message_text(text="В папке с новинками нет доступных изображений.", reply_markup=main_menu_keyboard())
        return

    for file_name in image_files:
        file_path = os.path.join(new_items_dir, file_name)
        with open(file_path, 'rb') as f:
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=f)

    keyboard = [[InlineKeyboardButton("Назад", callback_data='start')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=query.message.chat_id, text="Возвращение в главное меню", reply_markup=reply_markup)

# Обработчик для кнопки "Видео"
async def handle_videos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = "Видео ролики:\n"
    for i, (title, link) in enumerate(video_links.items(), 1):
        message += f"{i}. {title} - [смотреть видео]({link})\n"
    keyboard = [[InlineKeyboardButton("Назад", callback_data='start')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text=message, parse_mode='Markdown', reply_markup=reply_markup)

def main() -> None:
    # Вставьте ваш токен сюда
    application = Application.builder().token("7231643606:AAE5SueX-BKcjTbbWfzzusX6iPKSI5s7Eck").build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button, pattern='^start$'))
    application.add_handler(CallbackQueryHandler(handle_catalogs, pattern='^catalogs$'))
    application.add_handler(CallbackQueryHandler(handle_new_items, pattern='^new_items$'))
    application.add_handler(CallbackQueryHandler(handle_videos, pattern='^videos$'))

    application.run_polling()

if __name__ == '__main__':
    main()
