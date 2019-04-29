import os

token = os.environ.get("TOKEN", "")
root_admins = os.environ.get("ROOT_ADMIN", "1900520795")
root_admins = root_admins.split(",")
admins_card_number = os.environ.get("ADMIN_CARD_NUMBER", "")
channel_name = os.environ.get("CHANNEL_ADDRESS", "فروشگاه احمدی")
log_file = os.environ.get("LOG_FILE", "log_file.log")
