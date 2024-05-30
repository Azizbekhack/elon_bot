from aiogram import Bot,Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command
from aiogram import F
from aiogram.types import Message,InlineKeyboardButton,CallbackQuery
from data import config
import asyncio
import logging
import sys
from menucommands.set_bot_commands  import set_default_commands
from baza.sqlite import Database
from filters.admin import IsBotAdminFilter
from filters.check_sub_channel import IsCheckSubChannels
from keyboard_buttons import admin_keyboard
from aiogram.fsm.context import FSMContext #new
from states.reklama import Adverts,Telefon
from aiogram.utils.keyboard import InlineKeyboardBuilder

import time 
from keyboard_buttons.inlinebuttons import tasdiqlash
from aiogram.client.session.aiohttp import AiohttpSession



ADMINS = config.ADMINS
TOKEN = config.BOT_TOKEN
CHANNELS = config.CHANNELS
ADMINLAR_GURUHI = config.ADMINLAR_GURUHI
TELEFON_BOZOR = config.TELEFON_BOZOR


dp = Dispatcher()

@dp.message(IsCheckSubChannels())
async def kanalga_obuna(message:Message):
    text = ""
    inline_channel = InlineKeyboardBuilder()
    for index,channel in enumerate(CHANNELS):
        ChatInviteLink = await bot.create_chat_invite_link(channel)
        inline_channel.add(InlineKeyboardButton(text=f"{index+1}-kanal",url=ChatInviteLink.invite_link))
    inline_channel.adjust(1,repeat=True)
    button = inline_channel.as_markup()
    await message.answer(f"{text} Kanallarga azo bo'ling",reply_markup=button)





@dp.message(CommandStart())
async def start_command(message:Message):
    full_name = message.from_user.full_name
    telegram_id = message.from_user.id
    try:
        db.add_user(full_name=full_name,telegram_id=telegram_id) #foydalanuvchi bazaga qo'shildi
        await message.answer(text="Assalomu alaykum, botimizga hush kelibsiz",reply_markup=admin_keyboard.elon_button)
    except:
        await message.answer(text="Assalomu alaykum",reply_markup=admin_keyboard.elon_button)


@dp.message(F.text=="📱 Elon berish")
async def elon(message:Message,state:FSMContext):
    await message.answer("📱 Telefon rasmini yuboring")
    await state.set_state(Telefon.rasm)



@dp.message(F.photo,Telefon.rasm)
async def rasm_qbul_qilish(message:Message,state:FSMContext):
    rasm_id = message.photo[-1].file_id
    await state.update_data(rasm_id=rasm_id)
    await state.set_state(Telefon.model)
    await message.answer("📱 Telefoningiz modelini kiriting:")


@dp.message(F.text,Telefon.model)
async def model_qbul_qilish(message:Message,state:FSMContext):
    model = message.text
    await state.update_data(model=model)
    await state.set_state(Telefon.narxi)
    await message.answer("💰 Telefoningiz narxini kiriting:")


@dp.message(F.text,Telefon.narxi)
async def rasm_qbul_qilish(message:Message,state:FSMContext):
    narxi = message.text
    await state.update_data(narxi=narxi)
    await state.set_state(Telefon.tel)
    await message.answer("Telefoningiz raqamini kiriting:")


@dp.message(F.text,Telefon.narxi)
async def narxi_qbul_qilish(message:Message,state:FSMContext):
    narxi = message.text
    await state.update_data(narxi=narxi)
    await state.set_state(Telefon.tel)
    await message.answer("📞 Telefoningiz nomeringizni kiriting:")

@dp.message(F.text,Telefon.tel)
async def tel_qbul_qilish(message:Message,state:FSMContext):
    tel = message.text
    await state.update_data(tel=tel)
    await state.set_state(Telefon.rangi)
    await message.answer("🎨 Telefoningiz rangini kiriting:")

@dp.message(F.text,Telefon.rangi)
async def tel_qbul_qilish(message:Message,state:FSMContext):
    rangi = message.text
    await state.update_data(rangi=rangi)
    await state.set_state(Telefon.karobka)
    await message.answer("Telefoningiz 📦&📑 bormi:")

@dp.message(F.text,Telefon.karobka)
async def tel_qbul_qilish(message:Message,state:FSMContext):
    karobka = message.text
    await state.update_data(karobka=karobka)
    await state.set_state(Telefon.xolati)
    await message.answer("🛠 Telefoningiz  xolati qanaqa:")


@dp.message(F.text,Telefon.xolati)
async def tel_qbul_qilish(message:Message,state:FSMContext):
    xolati = message.text
    await state.update_data(xolati=xolati)
    await state.set_state(Telefon.xotirasi)
    await message.answer("🧠 Telefoningiz xotirasi qancha:")


@dp.message(F.text,Telefon.xotirasi)
async def rangi_qbul_qilish(message:Message,state:FSMContext):
    rangi = message.text
    data = await state.get_data()

    xotirasi = message.text
    rasm = data.get("rasm_id")
    model = data.get("model")
    narxi = data.get("narxi")
    tel = data.get("tel")
    rangi = data.get("rangi")
    karobka = data.get("karobka")
    karobka = data.get("karobka")
    xolati = data.get("xolati")
    
    text = f"""#Продается \n📱:{model}\n🛠: {xolati}\n🎨: {rangi}\n📦&📑: {karobka}\n🧠: {xotirasi}\n💰: {narxi}\n📞: {tel}!\n\n\nAdmin murojat : @solo_hub\nKanlimiz : https://t.me/telefon_re """
    await bot.send_photo(chat_id=ADMINLAR_GURUHI,photo=rasm,caption=text,reply_markup=tasdiqlash)


    await state.clear()
    await message.answer("📝Elonningiz adminga yuborildi🧑‍💻:💲Undan oldin tulov qiling💲.\nElon uchun raxmat !!!\nAdmin murojat : @solo_hub\nKanlimiz : https://t.me/telefon_re")


@dp.callback_query(F.data=="False")
async def tasdiqlanmadi(callback_query:CallbackQuery):
    
    await callback_query.message.delete()


@dp.callback_query(F.data=="True")
async def tasdiqlanmadi(callback_query:CallbackQuery):
    rasm = callback_query.message.photo[-1].file_id
    text = callback_query.message.caption
    await bot.send_photo(chat_id=TELEFON_BOZOR,photo=rasm,caption=text)
    await callback_query.message.delete()








#help commands
@dp.message(Command("help"))
async def help_commands(message:Message):
    await message.answer("Sizga qanday yordam kerak\nBizning adminimizga yozing\n@solo_hub :::>> 24/7")



#about commands
@dp.message(Command("about"))
async def about_commands(message:Message):
    await message.answer("Assalomu alaykum.Bizning botimizga hush kelibsiz !!!!!\n@solo_hub tomonidan tayorlangan\nBu botda online kampyuter va telefonlar sotib olasiz")


@dp.message(Command("admin"),IsBotAdminFilter(ADMINS))
async def is_admin(message:Message):
    await message.answer(text="Admin menu",reply_markup=admin_keyboard.admin_button)


@dp.message(F.text=="Foydalanuvchilar soni",IsBotAdminFilter(ADMINS))
async def users_count(message:Message):
    counts = db.count_users()
    text = f"Botimizda {counts[0]} ta foydalanuvchi bor"
    await message.answer(text=text)

@dp.message(F.text=="Reklama yuborish",IsBotAdminFilter(ADMINS))
async def advert_dp(message:Message,state:FSMContext):
    await state.set_state(Adverts.adverts)
    await message.answer(text="Reklama yuborishingiz mumkin !")

@dp.message(Adverts.adverts)
async def send_advert(message:Message,state:FSMContext):
    
    message_id = message.message_id
    from_chat_id = message.from_user.id
    users = db.all_users_id()
    count = 0
    for user in users:
        try:
            await bot.copy_message(chat_id=user[0],from_chat_id=from_chat_id,message_id=message_id)
            count += 1
        except:
            pass
        time.sleep(0.01)
    
    await message.answer(f"Reklama {count}ta foydalanuvchiga yuborildi")
    await state.clear()


@dp.startup()
async def on_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin),text="Bot ishga tushdi")
        except Exception as err:
            logging.exception(err)

#bot ishga tushganini xabarini yuborish
@dp.shutdown()
async def off_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin),text="Bot ishdan to'xtadi!")
        except Exception as err:
            logging.exception(err)


def setup_middlewares(dispatcher: Dispatcher, bot: Bot) -> None:
    """MIDDLEWARE"""
    from middlewares.throttling import ThrottlingMiddleware

    # Spamdan himoya qilish uchun klassik ichki o'rta dastur. So'rovlar orasidagi asosiy vaqtlar 0,5 soniya
    dispatcher.message.middleware(ThrottlingMiddleware(slow_mode_delay=0.5))



async def main() -> None:
    global bot,db
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    db = Database(path_to_db="main.db")
    await set_default_commands(bot)
    await dp.start_polling(bot)
    setup_middlewares(dispatcher=dp, bot=bot)




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(main())