from telegram import Update
from telegram.ext import ContextTypes
from config import GROUP_INVITE_LINK
from utils.storage import load_users

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    userid = str(update.message.from_user.id)
    users = load_users()
    userinfo = users.get(userid)

    if not userinfo:
        msg = "No registration found. Please use /start to begin."
    elif not userinfo.get("phone"):
        msg = "Your mobile number is pending. Please enter your mobile number (+91XXXXXXXXXX) in chat."
    elif not userinfo.get("idimage_fileid"):
        msg = "You have not uploaded your Student ID yet. Please upload your College ID proof to continue."
    elif not userinfo.get("idapproved", False):
        msg = "Your student ID verification is pending. Please wait for admin approval."
    elif not userinfo.get("pack"):
        msg = "Your ID is approved! Please select a plan from the options sent after approval."
    elif not userinfo.get("payment_ss_fileid"):
        msg = (f"You selected: {userinfo.get('pack', '-')}\n"
               "Please upload your payment screenshot to continue.")
    elif not userinfo.get("paymentapproved", False):
        msg = (f"Your payment for {userinfo.get('pack', '-')} is pending admin verification.\n"
               "Please wait for admin approval.")
    else:
        msg = (f"✅ Registration Complete!\n"
               f"Your Plan: {userinfo.get('plan', '-')}\n"
               f"Join Date: {userinfo.get('joindate', '-')}\n"
               f"Expiry Date: {userinfo.get('expirydate', '-')}\n"
               f"Group Link: {userinfo.get('invitelink', GROUP_INVITE_LINK)}")
    await update.message.reply_text(msg)


async def extend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Renew your study plan instructions.")

async def link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Didn't get added? Here is your group link: {GROUP_INVITE_LINK}")

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ask your doubts directly to the main admin.")
