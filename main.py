import os
from dotenv import load_dotenv
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          Defaults, ConversationHandler)

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
import logging
import redis

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
# REDIS_HOST = os.environ['REDIS_HOST']
# REDIS_PORT = os.environ['REDIS_PORT']
# REDIS_PASSWORD = os.environ['REDIS_PASSWORD']

UP_MENU_TEXT = 'Предложить улучшение условий труда'
DOWN_MENU_TEXT = 'Сообщить о рисках, несоответствиях, происшествиях'
CANCEL_TEXT = 'Отмена'

MENU_KEYBOARD = [[UP_MENU_TEXT], [DOWN_MENU_TEXT], [CANCEL_TEXT]]
SECRET, PERSONAL_DATA, FIO, IMPROVE, DANGER_TYPE, PLACE, DANGER, AWARED, PHOTO = range(
    9)


def start(update, context):
    """Send a message when the command /start is issued."""
    example_text = """\
 Здравствуйте!\nЯ - *Электронный консультант по вопросам ЕСУПБ*.\n\
С радостью отвечу на Ваши вопросы.\n
Чтобы получить дополнительную информацию о боте, наберите команду /help"""
    update.message.reply_text(example_text)


def help(update, context):
    """Send a message when the command /help is issued."""
    help_text = """*Дополнительная информация:*\n\n\
Чтобы предложить улучшение условий и охраны труда, наберите команду /improve\n\
Чтобы сообщить о рисках, несоответствиях, происшествиях, наберите команду /danger\n\n\
Бот отвечает на вопросы по темам:\n\
- Ключевые правила безопасности ПАО «Газпром»;\n\
- термины и определения ЕСУПБ;\n\
- Политика ПАО «Газпром»\n\
- основные положения СТО Газпром 18000.1-001-2021;\n\
- основы промышленной безопасности А.1;\n\
- информационный лист для работника Очерского ЛПУМГ о ЕСУПБ;\n\
- памятка о правилах поведения работников при встрече с дикими животными;\n\
- памятка работнику по пожарной безопасности;\n\
- газоопасные работы;\n\
- положение о культуре производства;\n\
- кодекс корпоративной этики"""
    update.message.reply_text(help_text)


def ESUPB_helper(update, context):
    """ESUPB_helper"""

    reply_msg = 'Единая система управления производственной безопасностью (ЕСУПБ) - комплекс организационных и технических мероприятий, выполняемых для обеспечения производственной безопасности.'

    msg = update.message.text
    reply_markup = ReplyKeyboardRemove()

    if msg.lower() == "меню":
        reply_markup = ReplyKeyboardMarkup(MENU_KEYBOARD,
                                           one_time_keyboard=False,
                                           resize_keyboard=True)
        reply_msg = 'Выберите пункт меню'

    elif msg == CANCEL_TEXT:
        reply_msg = 'Действие отменено'

    elif msg == UP_MENU_TEXT:
        reply_msg = "up text"

    elif msg == DOWN_MENU_TEXT:
        reply_msg = "down text"

    update.message.reply_text(reply_msg, reply_markup=reply_markup)


def error(update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def improvement_cancel(update, context) -> int:
    """Cancels improvements."""
    user = update.message.from_user
    logger.info(f"User {user.first_name} canceled the improvement.")
    update.message.reply_text(
        'Внесение предложения по улучшению условий и охраны труда отменено',
        reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def improvement(update, context) -> int:
    """Starts improvements."""
    update.message.reply_text(
        'Опишите предлагаемое улучшение.\n'
        'Чтобы отменить подачу улучшения, наберите команду /cancel')
    return FIO


def personal_data_consent(update, context) -> int:
    context.user_data['FIO'] = update.message.text
    reply_keyboard = [['Да', 'Нет']]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard,
                                       one_time_keyboard=True,
                                       resize_keyboard=True)
    reply_text = """Вы согласны на обработку персональных данных согласно\
Федерального закона от 27.07.2006 №152-ФЗ 'О персональных данных'\n\n\
Если Вы нажмете "Нет", предложенное улучшение отправится анонимно\n\n\
Чтобы отменить подачу улучшения, наберите команду /cancel"""
    update.message.reply_text(reply_text, reply_markup=reply_markup)
    return IMPROVE


def type_FIO(update, context) -> int:
    context.user_data['improvement'] = update.message.text
    reply_text = f"""Спасибо. Ваше предложение по улучшению условий и охраны \
труда принято в обработку.\n\n Укажите Ваши контактные данные, например: \
Имя, газовый телефон, сотовый телефон или почту. \
\n\nЧтобы отменить подачу улучшения, наберите команду /cancel"""
    update.message.reply_text(reply_text)
    return PERSONAL_DATA


def save_improvement(update, context) -> int:

    consent = update.message.text

    if not (consent == "Да" or consent == "Нет"):
        return IMPROVE

    if consent == "Нет":
        context.user_data['FIO'] = "Инкогнито"

    reply_text = (f"{context.user_data['FIO']} "
                  f"({update.message.from_user.id}):\n"
                  f"{context.user_data['improvement']}")

    del context.user_data['FIO']
    del context.user_data['improvement']

    update.message.reply_text(reply_text, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main():

    # r.set('example', 'text')
    # example_text = r.get('example')

    updater = Updater(BOT_TOKEN,
                      defaults=Defaults(parse_mode="Markdown"),
                      use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    improve_handler = ConversationHandler(
        entry_points=[CommandHandler('improve', improvement)],
        states={
            FIO: [MessageHandler(Filters.text & ~Filters.command, type_FIO)],
            PERSONAL_DATA: [
                MessageHandler(Filters.text & ~Filters.command,
                               personal_data_consent)
            ],
            IMPROVE: [
                MessageHandler(Filters.text & ~Filters.command,
                               save_improvement)
            ]
        },
        fallbacks=[CommandHandler('cancel', improvement_cancel)],
    )

    dp.add_handler(improve_handler)
    dp.add_handler(MessageHandler(Filters.text, ESUPB_helper))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    # r = redis.Redis(
    #     host=REDIS_HOST,
    #     port=REDIS_PORT,
    #     password=REDIS_PASSWORD
    # )
    main()
