import os

db_user = os.getenv('POSTGRES_USER', "")
db_password = os.getenv('POSTGRES_PASSWORD', "")
db_host = os.getenv('POSTGRES_HOST', "")
db_name = os.getenv('POSTGRES_DB', "")
db_port = os.getenv('POSTGRES_PORT', "")
# DB address
dbadress = "postgresql://{}:{}@{}:{}/{}".format(db_user, db_password, db_host, db_port, db_name) or None
# table names
users = os.getenv('USERS', 'users')
requests = os.getenv('REQUESTS', 'requests')
admins = os.getenv('ADMINS', 'admins')
products = os.getenv('PRODUCTS', 'products')
photos = os.getenv('PHOTOS', 'photos')
default_state = os.getenv('DEFAULT_STATE', 'در صف بررسی')
