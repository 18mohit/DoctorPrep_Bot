from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from config import ADMIN_ID, GROUP_INVITE_LINK, PAYMENT_OPTIONS
from utils.storage import save_users, load_users
from datetime import datetime, timedelta

async def approve_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("Only admin can approve student IDs.")
        return
    if not context.args or len(context.args) != 1:
        await update.message.reply_text("Usage: /approveid USERID")
        return
    target_userid = context.args[0]
    users = load_users()
    if target_userid not in users:
        await update.message.reply_text("This user has not registered yet.")
        return
    users[target_userid]['idapproved'] = True
    save_users(users)
    await update.message.reply_text(f"ID approved for user {target_userid}.")
    keyboard = [[opt[0]] for opt in PAYMENT_OPTIONS]
    replymarkup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    try:
        await context.bot.send_message(
            chat_id=int(target_userid),
            text="Your student ID has been verified by the admin!\nSelect your plan to continue.",
            reply_markup=replymarkup
        )
    except Exception as ex:
        await update.message.reply_text(f"Could not notify user: {ex}")

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("Only admin can approve users.")
        return
    if not context.args or len(context.args) != 1:
        await update.message.reply_text("Usage: /approve USERID")
        return
    target_userid = context.args[0]
    users = load_users()
    if target_userid not in users:
        await update.message.reply_text("This user has not registered yet.")
        return
    if not users[target_userid].get("idapproved", False):
        await update.message.reply_text("First approve student ID using /approveid USERID.")
        return
    if not users[target_userid].get("payment_ss_fileid"):
        await update.message.reply_text("User has not uploaded payment screenshot yet.")
        return
    users[target_userid]["paymentapproved"] = True
    pack = users[target_userid].get("pack", "Trial pack 1 month")
    if "Trial pack 1 month" in pack:
        days = 30
    elif "Subscription 3 months" in pack:
        days = 90
    elif "6 month pack" in pack:
        days = 180
    elif "1 year pack" in pack:
        days = 365
    else:
        days = 30
    jointime = datetime.now()
    expirytime = jointime + timedelta(days=days)
    users[target_userid]["plan"] = pack
    users[target_userid]["joindate"] = jointime.strftime("%a %b %d %Y %H:%M:%S GMT+05:30 India Standard Time")
    users[target_userid]["expirydate"] = expirytime.strftime("%a %b %d %Y %H:%M:%S GMT+05:30 India Standard Time")
    users[target_userid]["invitelink"] = GROUP_INVITE_LINK
    save_users(users)
    await update.message.reply_text(f"Approved and activated {target_userid} for {pack} ({days} days)")
    try:
        await context.bot.send_message(
            chat_id=int(target_userid),
            text=(
                f"🎉 Your payment has been verified and your subscription activated!\n"
                f"Plan: {pack}\n"
                f"Join Date: {users[target_userid]['joindate']}\n"
                f"Expiry Date: {users[target_userid]['expirydate']}\n"
                f"Group Link: {GROUP_INVITE_LINK}\n"
            )
        )
    except Exception as ex:
        await update.message.reply_text(f"Could not notify user: {ex}")
