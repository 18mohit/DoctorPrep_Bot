from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
from config import PAYMENT_OPTIONS, ADMIN_ID
from utils.storage import save_users, load_users

async def receivepack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    selected = update.message.text.strip()
    valid = [opt[0] for opt in PAYMENT_OPTIONS]
    if selected not in valid:
        keyboard = [[option[0]] for option in PAYMENT_OPTIONS]
        replymarkup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Invalid selection, please choose from the buttons below.", reply_markup=replymarkup)
        return
    context.user_data["pack"] = selected

    for name, amt in PAYMENT_OPTIONS:
        if selected == name:
            context.user_data["amount"] = amt

    await update.message.reply_text(
        f"You have selected {context.user_data['pack']} ({context.user_data['amount']})\n"
        "Please pay on UPI 1234oksbin and upload payment screenshot (JPG/PNG only, not document).",
        reply_markup=ReplyKeyboardRemove()
    )
    
async def receivepaymentss(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = None
    if update.message.photo:
        file = update.message.photo[-1]
    elif update.message.document and update.message.document.mime_type in ["image/jpeg", "image/png"]:
        file = update.message.document
    if file:
        # process screenshot and continue
        await update.message.reply_text("Payment screenshot received! Waiting for admin verification.")
        # save file_id/etc...
        # proceed to next step or ConversationHandler.END
    else:
        await update.message.reply_text("Please upload a payment screenshot in JPG or PNG format.")
        
    users = load_users()
    userid = str(update.message.from_user.id)
    userinfo = users.get(userid, {})

    # BLOCK if mobile number is missing!
    if not userinfo.get("phone"):
        await update.message.reply_text("You must enter your mobile number before uploading screenshot. Please enter your mobile number (+91XXXXXXXXXX) in chat.")
        return

    if file:
        context.user_data["payment_ss_fileid"] = file.file_id
        # load existing user data and update relevant fields
        if userid not in users:
            users[userid] = {}
        users[userid].update(context.user_data)
        if "idapproved" not in users[userid]:
            users[userid]["idapproved"] = False
        users[userid]["payment_ss_fileid"] = file.file_id
        users[userid]["paymentapproved"] = False
        save_users(users)
        # SEND PAYMENT DETAILS TO ADMIN
        paymsg = (
            f"New Payment Proof Received\n"
            f"Name: {users[userid].get('name', '-')}\n"
            f"Phone: {users[userid].get('phone', '-')}\n"
            f"User ID: {userid}\n"
            f"Pack: {users[userid].get('pack', '-')}\n"
            f"Amount: {users[userid].get('amount', '-')}"
        )
        await context.bot.send_message(chat_id=ADMIN_ID, text=paymsg)
        await context.bot.send_photo(chat_id=ADMIN_ID, photo=file.file_id)
        await update.message.reply_text("Payment screenshot received. Please wait for admin approval.")
    else:
        await update.message.reply_text("Please upload a payment screenshot as JPG or PNG photo (no document).")
