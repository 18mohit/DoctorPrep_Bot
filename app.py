from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, filters
from handlers.registration import start, get_name, get_phone, get_id_image, NAME, PHONE, IDIMAGE
from handlers.admin import approve_id, approve
from handlers.status import status
from handlers.payment import receivepack, receivepaymentss
from config import TOKEN, PAYMENT_OPTIONS
import re

app = ApplicationBuilder().token(TOKEN).build()

# Registration flow: only ask for name, phone, and ID proof
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        IDIMAGE: [
                    MessageHandler(filters.PHOTO, get_id_image),
                    MessageHandler(filters.Document.IMAGE, get_id_image),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, get_id_image),  # for error text like "hello"
                 ],      
    },
    fallbacks=[],
)
app.add_handler(conv_handler)

# ADMIN HANDLERS
app.add_handler(CommandHandler("approveid", approve_id))
app.add_handler(CommandHandler("approve", approve))

# PLAN SELECTION HANDLER — Matches single correct plan names only
plan_names = [re.escape(opt[0]) for opt in PAYMENT_OPTIONS]
regex = '^(' + '|'.join(plan_names) + ')$'
app.add_handler(MessageHandler(filters.Regex(regex), receivepack))

# PAYMENT SCREENSHOT
app.add_handler(MessageHandler(filters.PHOTO, receivepaymentss))
app.add_handler(MessageHandler(filters.Document.IMAGE, receivepaymentss))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receivepaymentss))

# STATUS COMMAND
app.add_handler(CommandHandler("status", status))
# ADD OTHER COMMANDS if needed
# app.add_handler(CommandHandler("extend", extend))
# app.add_handler(CommandHandler("link", link))
# app.add_handler(CommandHandler("contact", contact))

if __name__ == "__main__":
    app.run_polling()