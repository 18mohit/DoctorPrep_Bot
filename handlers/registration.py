from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from config import ADMIN_ID
from utils.storage import save_users, load_users

NAME, PHONE, IDIMAGE = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    userid = str(update.message.from_user.id)
    users = load_users()
    if userid in users and users[userid].get("name") and users[userid].get("idimage_fileid"):
        await update.message.reply_text("You have already registered.\nUse /status to know your registration and payment status.")
        return ConversationHandler.END
    if userid not in users:
        users[userid] = {
            "name": "",
            "phone": "",
            "idimage_fileid": "",
            "idapproved": False,
            "pack": "",
            "amount": "",
            "payment_ss_fileid": "",
            "paymentapproved": False,
        }
        save_users(users)
    await update.message.reply_text("Welcome! What is your name?")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    userid = str(update.message.from_user.id)
    users = load_users()
    users[userid]["name"] = update.message.text
    save_users(users)
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Thank you, now please enter your phone number in format +91XXXXXXXXXX")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    userid = str(update.message.from_user.id)
    text = update.message.text.strip()
    if not text.startswith("+91") or len(text) != 13 or not text[1:].isdigit():
        await update.message.reply_text("Please give phone number in this format: +91XXXXXXXXXX")
        return PHONE
    users = load_users()
    users[userid]["phone"] = text
    save_users(users)
    context.user_data["phone"] = text
    await update.message.reply_text("Great! Now upload your College ID proof (PNG or JPG only)")
    return IDIMAGE

async def get_id_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = None
    userid = str(update.message.from_user.id)
    if update.message.photo:
        file = update.message.photo[-1]
    elif update.message.document and update.message.document.mime_type in ["image/jpeg", "image/png"]:
        file = update.message.document
    if file:
        users = load_users()
        users[userid]["idimage_fileid"] = file.file_id
        save_users(users)
        context.user_data["idimage_fileid"] = file.file_id
        userinfo = (
            f"New Registration\n"
            f"Name: {users[userid]['name']}\n"
            f"Phone: {users[userid]['phone']}\n"
            f"User ID: {userid}"
        )
        await context.bot.send_message(chat_id=ADMIN_ID, text=userinfo)
        await context.bot.send_photo(chat_id=ADMIN_ID, photo=file.file_id)
        await update.message.reply_text("Your student ID is uploaded and sent for admin verification. Please wait until your ID is approved.")
        return ConversationHandler.END
    else:
        await update.message.reply_text("Please upload a College ID photo in JPG or PNG format.")
        return IDIMAGE
