# TOKEN = "8457357260:AAFqeHMH5OXhLP8oc3Tk3LgIdwK4U3IH2co"  # Your bot token
# ADMIN_ID = 1843805619
# GROUP_INVITE_LINK = "https://t.me/COWlMskALCA4MmI9"
# USERS_FILE = "users.json"

# PAYMENT_OPTIONS = [
#     ("Trial pack 1 month", 200),
#     ("Subscription 3 months", 300),
#     ("6 month pack", 500),
#     ("1 year pack", 750)
# ]
import os
import ast

# Print at startup for debugging: REMOVE or comment out after confirming!
print(">>> Loading config.py - environment variables:")

TOKEN = os.getenv("TOKEN")
print("TOKEN present?", "yes" if TOKEN else "MISSING")

ADMIN_ID = os.getenv("ADMIN_ID")
print("ADMIN_ID:", ADMIN_ID)

GROUP_INVITE_LINK = os.getenv("GROUP_INVITE_LINK")
print("GROUP_INVITE_LINK:", GROUP_INVITE_LINK)

MONGO_URI = os.getenv("MONGO_URI")
print("MONGO_URI present?", "yes" if MONGO_URI else "MISSING")

USERS_FILE = "users.json"

PAYMENT_OPTIONS_RAW = os.getenv("PAYMENT_OPTIONS")
if PAYMENT_OPTIONS_RAW:
    try:
        PAYMENT_OPTIONS = ast.literal_eval(PAYMENT_OPTIONS_RAW)
        print("PAYMENT_OPTIONS loaded:", PAYMENT_OPTIONS)
    except Exception as e:
        print("PAYMENT_OPTIONS parse error:", e)
        PAYMENT_OPTIONS = []
else:
    PAYMENT_OPTIONS = [
        ("Trial pack 1 month", 200),
        ("Subscription 3 months", 300),
        ("6 month pack", 500),
        ("1 year pack", 750)
    ]
    print("PAYMENT_OPTIONS using default list.")
