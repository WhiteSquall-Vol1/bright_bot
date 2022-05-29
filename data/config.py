from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = int(env.str("ADMINS"))
IP = env.str("ip")

support_ids = [
    514793636
]
