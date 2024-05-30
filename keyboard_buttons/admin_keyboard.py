from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


admin_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Foydalanuvchilar soni"),
            KeyboardButton(text="Reklama yuborish"),
        ]
        
    ],
   resize_keyboard=True,
   input_field_placeholder="Menudan birini tanlang"
)

elon_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱 Elon berish")]
    ],
    resize_keyboard=True,
   input_field_placeholder="🧾 E'lon berishni boshlang"

)