from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters
import logging

DANGER_TYPES = [
    "Охрана труда",
    "Промышленная безопасность",
    "Пожарная безопасность",
    "Безопасность дорожного движения",
    "Другое"
]

D_FIO, D_PERSONAL_DATA, DANGER_TYPE, PLACE, DANGER, AWARED, SAVING = range(7)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


def accept_secret(update, context) -> int:
    keyboard = [["Ознакомлен"]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    reply_text = (
        "Заполнение ведется по шагам, согласно бланку обращения о "
        "происшествии (предпосылке к происшествию) (приложение Б, «Порядок "
        "работы по обращениям и жалобам, поступающим в ООО «Газпром трансгаз "
        "Чайковский», по направлениям ЕСУПБ)\n\n"
        "Вы ознакомлены об ответственности за распространение информации, "
        "составляющей государственную тайну, заведомо ложных сведений, "
        "порочащих честь и достоинство работников и третьих лиц, для "
        "сведения личных счетов, достижения личных целей, получения "
        "выгоды, и хулиганских побуждений и в иных противоправных целях?"
        "\n\nЧтобы отменить подачу сообщения, наберите команду /cancel"
    )
    update.message.reply_text(reply_text, reply_markup=reply_markup)
    return D_PERSONAL_DATA


def accept_personal_data(update, context) -> int:
    msg_text = update.message.text

    if not msg_text == "Ознакомлен":
        return D_PERSONAL_DATA
    
    reply_keyboard = [['Да', 'Нет']]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard,
                                       one_time_keyboard=True,
                                       resize_keyboard=True)
    
    reply_text = (
        "Вы согласны на обработку персональных данных согласно "
        "Федерального закона от 27.07.2006 №152-ФЗ 'О персональных "
        "данных'\n\nЕсли Вы нажмете 'Нет', сообщение отправится анонимно"
        "\n\nЧтобы отменить подачу сообщения, наберите команду /cancel"
    )

    update.message.reply_text(reply_text, reply_markup=reply_markup)
    return D_FIO


def typed_FIO(update, context) -> int:
    msg_text = update.message.text
    if not (msg_text == "Нет" or msg_text == "Да"):
        return D_FIO
    
    reply_text_yes = (
        "Укажите данные для обратной связи (ФИО, контактный телефон, "
        "адрес электронной почты)"
        "\n\nЧтобы отменить подачу сообщения, наберите команду /cancel"
    )
    reply_text_no = (
        "Ваше сообщение будет отправлено анонимно. Нажмите кнопку «ОК»."
        "\n\nЧтобы отменить подачу сообщения, наберите команду /cancel"
    )
    
    if msg_text == "Нет":
        context.user_data['contacts'] = "Unknown"
        reply_markup = ReplyKeyboardMarkup([["ОК"]],resize_keyboard=True,
                                           one_time_keyboard=True)
        update.message.reply_text(reply_text_no, reply_markup=reply_markup)

    if msg_text == "Да":
        update.message.reply_text(reply_text_yes, reply_markup=ReplyKeyboardRemove())
    
    return DANGER_TYPE


def get_danger_type(update, context) -> int:
    msg_text = update.message.text
    if not context.user_data.get('contacts'):
        context.user_data['contacts'] = msg_text
    else:
        if not msg_text == "ОК":
            return DANGER_TYPE
    
    reply_markup = ReplyKeyboardMarkup.from_column(
        DANGER_TYPES,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    reply_text = (
        "Выберите область, направление или категорию сообщения"
        "\n\nЧтобы отменить подачу сообщения, наберите команду /cancel"
    )
    update.message.reply_text(reply_text, reply_markup=reply_markup)
    return PLACE


def get_danger_place(update, context) -> int:
    danger_type = update.message.text
    if danger_type not in DANGER_TYPES:
        return PLACE
    else:
        context.user_data["danger_type"] = danger_type
    reply_text = (
        "Укажите место, где выявлена опасность. При необходимости, "
        "укажите дату и время обнаружения опасности"
        "\n\nЧтобы отменить подачу сообщения, наберите команду /cancel"
    )

    update.message.reply_text(reply_text, reply_markup=ReplyKeyboardRemove())
    return DANGER


def danger_description(update, context) -> int:
    place = update.message.text
    context.user_data["place"] = place
    reply_text = (
        "Введите текст сообщения. "
        "Текст сообщения должен содержать следующую информацию:\n"
        " - суть сообщения;\n"
        " - опасные факторы (события), которые влияют на развитие "
        "опасности (предпосылки к происшествию);\n"
        " - краткое описание опасности (предпосылки к происшествию), "
        "в том числе конкретные существенные факты и обстоятельства, "
        "значимые подробности, возможные причины;\n"
        " - последствия для ООО «Газпром трансгаз Чайковский» и "
        "его работников."
        "\n\nЧтобы отменить подачу сообщения, наберите команду /cancel"
    )
    update.message.reply_text(reply_text)
    return AWARED


def awared_people(update, context) -> int:
    danger = update.message.text
    context.user_data['danger'] = danger
    reply_text = (
        "Укажите данные работников (ФИО, должность), "
        "осведомленных о риске, несоответствии, происшествии."
        "\n\nЧтобы отменить подачу сообщения, наберите команду /cancel"
    )
    update.message.reply_text(reply_text)
    return SAVING


def save_danger(update, context) -> int:
    awared = update.message.text
    context.user_data["awared"] = awared
    save_danger_to_db(context.user_data)
    reply_text = (
        "Ваше обращение принято в обработку. Спасибо."
        f'\n{context.user_data["contacts"]}'
        f'\n{context.user_data["danger_type"]}'
        f'\n{context.user_data["place"]}'
        f'\n{context.user_data["danger"]}'
        f'\n{context.user_data["awared"]}'
    )
    update.message.reply_text(reply_text)

    return ConversationHandler.END


def danger_cancel(update, context) -> int:
    """Cancels danger_handler."""
    user = update.message.from_user
    logger.info(f"User {user.first_name} canceled the danger.")
    context.user_data.clear()
    update.message.reply_text(
        'Подача сообщения о рисках, несоответствиях, происшествиях отменено',
        reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def save_danger_to_db(danger:dict):
    pass


danger_handler = ConversationHandler(
    entry_points=[CommandHandler('danger', accept_secret)],
    states={
        D_PERSONAL_DATA: [MessageHandler(Filters.text & ~Filters.command, accept_personal_data)],
        D_FIO: [MessageHandler(Filters.text & ~Filters.command, typed_FIO)],
        DANGER_TYPE: [MessageHandler(Filters.text & ~Filters.command, get_danger_type)],
        PLACE: [MessageHandler(Filters.text & ~Filters.command, get_danger_place)],
        DANGER: [MessageHandler(Filters.text & ~Filters.command, danger_description)],
        AWARED: [MessageHandler(Filters.text & ~Filters.command, awared_people)],
        SAVING: [MessageHandler(Filters.text & ~Filters.command, save_danger)]
    },
    fallbacks=[CommandHandler('cancel', danger_cancel)]
)