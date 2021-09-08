import os
from dotenv import load_dotenv
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          Defaults)

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
import logging
import redis
from MyHandlers import improve_handler, danger_handler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')


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

    update.message.reply_text(reply_msg)


def error(update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():

    # r.set('example', 'text')
    # example_text = r.get('example')

    updater = Updater(BOT_TOKEN,
                      defaults=Defaults(parse_mode="Markdown"),
                      use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(improve_handler.improve_handler)
    dp.add_handler(danger_handler.danger_handler)
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
