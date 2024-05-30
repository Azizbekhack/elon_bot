from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

tasdiqlash = InlineKeyboardMarkup(
    inline_keyboard=[
         [InlineKeyboardButton(text="✅",callback_data="True"),InlineKeyboardButton(text="❌",callback_data="False")] 
    ]
)