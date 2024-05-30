from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot Token
ADMINS = list(map(int,env.list("ADMINS")))  # adminlar ro'yxati
CHANNELS = list(map(int,env.list("CHANNELS"))) 
ADMINLAR_GURUHI = -4229402774
TELEFON_BOZOR = -1002103868463