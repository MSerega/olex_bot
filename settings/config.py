from environs import Env
import os

env = Env()
env.read_env()

# Token Telegram bot
BOT_TOKEN = env.str("BOT_TOKEN")

# Data base
DB_BASE = os.path.abspath("db/" + env.str("DB_BASE"))

# Admin users
SUPPORT_ADMINS = [145333452, 637190452]
ADMIN = 145333452

# Channels
c_pidsluhano_id = -1001466681334

# Groups
g_pidsluhano_id = -1001247030550

# Users

# Pages for parsing
PRIVAT_ECHANGE = env.str("PRIVAT_ECHANGE")

SINOPTIK = env.str("SINOPTIK")
GISMETIO = env.str("GISMETIO")

FUEL_ANP_SHELL = env.str("FUEL_ANP_SHELL")

SUBURNAN_TRAINS = env.str("SUBURNAN_TRAINS")
PASSENGER_TRAINS = env.str("PASSENGER_TRAINS")

HOROSCOPE = env.str("HOROSCOPE")




