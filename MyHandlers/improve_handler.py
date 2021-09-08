from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters
import logging

FIO, IMPROVE, PERSONAL_DATA = range(3)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


def improvement_cancel(update, context) -> int:
    """Cancels improve_handler."""
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