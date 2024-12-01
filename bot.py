from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

import re

# Global variables to track posts and process state
pending_posts = []
is_creating_post = False

FONT_MAPPING = {
    "A": "𝖠", "B": "𝖡", "C": "𝖢", "D": "𝖣", "E": "𝖤", "F": "𝖥", "G": "𝖦",
    "H": "𝖧", "I": "𝖨", "J": "𝖩", "K": "𝖪", "L": "𝖫", "M": "𝖬", "N": "𝖭",
    "O": "𝖮", "P": "𝖯", "Q": "𝖰", "R": "𝖱", "S": "𝖲", "T": "𝖳", "U": "𝖴",
    "V": "𝖵", "W": "𝖶", "X": "𝖷", "Y": "𝖸", "Z": "𝖹",
    "a": "𝖺", "b": "𝖻", "c": "𝖼", "d": "𝖽", "e": "𝖾", "f": "𝖿", "g": "𝗀",
    "h": "𝗁", "i": "𝗂", "j": "𝗃", "k": "𝗄", "l": "𝗅", "m": "𝗆", "n": "𝗇",
    "o": "𝗈", "p": "𝗉", "q": "𝗊", "r": "𝗋", "s": "𝗌", "t": "𝗍", "u": "𝗎",
    "v": "𝗏", "w": "𝗐", "x": "𝗑", "y": "𝗒", "z": "𝗓",
    "1": "𝟣", "2": "𝟤", "3": "𝟥", "4": "𝟦", "5": "𝟧", "6": "𝟨", "7": "𝟩",
    "8": "𝟪", "9": "𝟫", "0": "𝟢", ".": "․", "-": "-"
}

CHANNEL_ID = "-1002350512596"  # Replace with your channel username or ID


def convert_to_math_sans(text: str) -> str:
    text = re.sub(r"_", ".", text)  # Convert _ to .
    text = re.sub(r"[^\w\.-]", "", text)  # Remove unwanted characters except . and -
    return ''.join(FONT_MAPPING.get(char, char) for char in text)


def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("Create Post", callback_data="create_post")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Click below to start creating posts.", reply_markup=reply_markup)


def create_post(update: Update, context: CallbackContext):
    global is_creating_post
    is_creating_post = True
    keyboard = [
        [
            InlineKeyboardButton("Auto1", callback_data="auto1"),
            InlineKeyboardButton("Auto2", callback_data="auto2"),
            InlineKeyboardButton("Auto3", callback_data="auto3"),
            InlineKeyboardButton("Auto4", callback_data="auto4"),
        ],
        [
            InlineKeyboardButton("Cancel", callback_data="cancel"),
            InlineKeyboardButton("Done", callback_data="done"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text("Select an option for your post:", reply_markup=reply_markup)


def handle_auto1(update: Update, context: CallbackContext):
    update.callback_query.edit_message_text("Send an image with text to proceed.")


def handle_auto2(update: Update, context: CallbackContext):
    update.callback_query.edit_message_text("Send a document with text to proceed.")


def handle_auto3(update: Update, context: CallbackContext):
    update.callback_query.edit_message_text("Send a video with text to proceed.")


def handle_auto4(update: Update, context: CallbackContext):
    update.callback_query.edit_message_text("Send an image or sticker to proceed.")


def cancel_process(update: Update, context: CallbackContext):
    global pending_posts, is_creating_post
    pending_posts = []
    is_creating_post = False
    update.callback_query.edit_message_text("Process cancelled.")


def done_process(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("Confirm", callback_data="confirm")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text("Click confirm to post all pending messages.", reply_markup=reply_markup)


def confirm_posts(update: Update, context: CallbackContext):
    global pending_posts, is_creating_post
    bot: Bot = context.bot
    for post in pending_posts:
        bot.send_message(chat_id=CHANNEL_ID, text=post, parse_mode=ParseMode.HTML)
    pending_posts = []
    is_creating_post = False
    update.callback_query.edit_message_text("All posts sent to the channel.")


def main():
    # Replace with your bot token
    BOT_TOKEN = "7577588868:AAFFZHTAsc0AwWaTPZxpP7EgGCqQEAQote8"
    updater = Updater(BOT_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(create_post, pattern="create_post"))
    dp.add_handler(CallbackQueryHandler(handle_auto1, pattern="auto1"))
    dp.add_handler(CallbackQueryHandler(handle_auto2, pattern="auto2"))
    dp.add_handler(CallbackQueryHandler(handle_auto3, pattern="auto3"))
    dp.add_handler(CallbackQueryHandler(handle_auto4, pattern="auto4"))
    dp.add_handler(CallbackQueryHandler(cancel_process, pattern="cancel"))
    dp.add_handler(CallbackQueryHandler(done_process, pattern="done"))
    dp.add_handler(CallbackQueryHandler(confirm_posts, pattern="confirm"))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
