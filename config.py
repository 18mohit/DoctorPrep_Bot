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

TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
GROUP_INVITE_LINK = os.getenv("GROUP_INVITE_LINK")
MONGO_URI = os.getenv("MONGO_URI")
USERS_FILE = "users.json"

# PAYMENT_OPTIONS needs special handling
PAYMENT_OPTIONS_RAW = os.getenv("PAYMENT_OPTIONS")
if PAYMENT_OPTIONS_RAW:
    # This is risky, but should work if you paste a Python list/tuple string in Render env var
    PAYMENT_OPTIONS = eval(PAYMENT_OPTIONS_RAW)
else:
    PAYMENT_OPTIONS = [
        ("Trial pack 1 month", 200),
        ("Subscription 3 months", 300),
        ("6 month pack", 500),
        ("1 year pack", 750)
    ]
