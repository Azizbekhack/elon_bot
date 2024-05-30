from aiogram.fsm.state import State, StatesGroup

class Adverts(StatesGroup):
    adverts = State()

class Telefon(StatesGroup):
    rasm = State()
    model = State()
    rangi = State()
    narxi = State()
    tel = State()
    karobka = State()
    xolati = State()
    xotirasi = State()
