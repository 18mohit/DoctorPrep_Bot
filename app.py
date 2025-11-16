from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, filters
from handlers.registration import start, get_name, get_phone, get_id_image, NAME, PHONE, IDIMAGE
from handlers.admin import approve_id, approve
from handlers.status import status
from handlers.status import extend, link, contact
from handlers.payment import receivepack, receivepaymentss
from config import TOKEN, PAYMENT_OPTIONS
import re

app = ApplicationBuilder().token(TOKEN).build()  # <-- only ONCE!

# Registration flow
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        IDIMAGE: [
            MessageHandler(filters.PHOTO, get_id_image),
            MessageHandler(filters.Document.IMAGE, get_id_image),
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_id_image),
        ],       
    },
    fallbacks=[],
)
app.add_handler(conv_handler)

def error_handler(update, context):
    print(f"Update {update} caused error {context.error}")

app.add_error_handler(error_handler)  # register to the same app!

# Admin handlers
app.add_handler(CommandHandler("approveid", approve_id))
app.add_handler(CommandHandler("approve", approve))

# Plan selection handler
plan_names = [re.escape(opt[0]) for opt in PAYMENT_OPTIONS]
regex = '^(' + '|'.join(plan_names) + ')$'
app.add_handler(MessageHandler(filters.Regex(regex), receivepack))

# Payment screenshot
app.add_handler(MessageHandler(filters.PHOTO, receivepaymentss))
app.add_handler(MessageHandler(filters.Document.IMAGE, receivepaymentss))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receivepaymentss))

# Status
app.add_handler(CommandHandler("status", status))
# ADD OTHER COMMANDS if needed
app.add_handler(CommandHandler("extend", extend))
app.add_handler(CommandHandler("link", link))
app.add_handler(CommandHandler("contact", contact))

if __name__ == "__main__":
    # app.run_polling().
    pass  # IGNORE for now