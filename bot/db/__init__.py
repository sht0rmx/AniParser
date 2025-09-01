from decouple import config

from pocketbase import PocketBase
# from pocketbase.client import FileUpload

pb_url = config("PB_URL")
if type(pb_url) is not str:
    raise Exception("Invalid format of PocketBase url in .env")

client = PocketBase(pb_url)

admin_email, admin_password = config("PB_EMAIL"), config("PB_PASSWORD")
if type(admin_email) is not str or type(admin_password) is not str:
    raise Exception("Invalid format of PocketBase administrator account creditinals in .env")

admin_data = client.admins.auth_with_password(admin_email, admin_password)

if not admin_data.is_valid:
    raise Exception("Invalid PocketBase administrator account creditinals in .env")
