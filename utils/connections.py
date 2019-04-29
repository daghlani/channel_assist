from models.bale_moduls import *
from config import public

# Bale Bot Authorization Token
updater = Updater(token=public.token,
                  loop=asyncio.get_event_loop())
# Define dispatcher
dispatcher = updater.dispatcher


