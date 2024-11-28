from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from Parsers_aio.Main_info_crypto_parser_aio import General
from Parsers_aio.Item_info_crypto_parser_aio import Crypto


get_info_commands_router = Router()


# Обработчик команды "/get_total_capitalization"
@get_info_commands_router.message(Command("get_total_capitalization"))
async def get_total_capitalization(message: types.Message):
    curr_General = General()
    curr_capitalization = curr_General.get_data_market_capitalization()[0]
    curr_change = curr_General.get_change_market_capitalization()
    curr_change_value = curr_change[0]
    curr_direction = "увеличилась" if curr_change[2] == "up" else "уменьшилась"

    await message.answer(
        f"Общая рыночная каптилизация составляет:\n$ {curr_capitalization}\n\nРыночная капитализация {curr_direction}\nна {curr_change_value} за последние 24 часа."
    )


# Обработчик команды "/get_total_trading_volume"
@get_info_commands_router.message(Command("get_total_trading_volume"))
async def get_total_trading_volume(message: types.Message):
    curr_General = General()
    curr_volume = curr_General.get_total_trading_volume_per_day()[0]
    await message.answer(
        f"Общий объём торгов криптовалютой составляет:\n$ {curr_volume}"
    )


# Класс с инициализацией машины состояний после команды "/get_crypto_capitalization"
class Form_crypto_cap(StatesGroup):
    waiting_for_message_crypto_cap = State()


# Обработчик команды "/get_crypto_capitalization"
@get_info_commands_router.message(Command("get_crypto_capitalization"))
async def get_crypto_capitalization(message: types.Message, state: FSMContext):
    # Установка состояния ожидания названия криптовалюты для получения её капитализации
    await state.set_state(Form_crypto_cap.waiting_for_message_crypto_cap)
    await message.answer(
        "Для получения рыночной капитализации,\nвведите название криптовалюты:"
    )


# Обработчик состояния ожидания названия криптовалюты для получения её капитализации
@get_info_commands_router.message(Form_crypto_cap.waiting_for_message_crypto_cap)
async def process_message_crypto_cap(message: types.Message, state: FSMContext):
    try:
        curr_Crypto = Crypto(message.text)
        curr_name = curr_Crypto.get_crypto_name
        curr_capitalization = curr_Crypto.get_current_crypto_capitalization()[0]
        if curr_capitalization != "Нет информации":
            await message.answer(
                f"Рыночная капитализация {curr_name}:\n$ {curr_capitalization}"
            )
        else:
            await message.answer(f"Нет информации о рыночной капитализации {curr_name}")
    except:
        await message.answer("Введена некорректная криптовалюта")

    await state.clear()


# Класс с инициализацией машины состояний после команды "/get_crypto_price"
class Form_crypto_price(StatesGroup):
    waiting_for_message_crypto_price = State()


# Обработчик команды "/get_crypto_price"
@get_info_commands_router.message(Command("get_crypto_price"))
async def get_crypto_price(message: types.Message, state: FSMContext):
    # Установка состояния ожидания названия криптовалюты для получения её стоимости
    await state.set_state(Form_crypto_price.waiting_for_message_crypto_price)
    await message.answer(
        "Для получения средней стоимости,\nвведите название криптовалюты:"
    )


# Обработчик состояния ожидания названия криптовалюты для получения её стоимости
@get_info_commands_router.message(Form_crypto_price.waiting_for_message_crypto_price)
async def process_message_crypto_price(message: types.Message, state: FSMContext):
    try:
        curr_Crypto = Crypto(message.text)
        curr_name = curr_Crypto.get_crypto_name
        curr_price = curr_Crypto.get_current_average_crypto_price()[0]
        await message.answer(f"Средняя стоимость {curr_name}:\n$ {curr_price}")
    except:
        await message.answer("Введена некорректная криптовалюта")

    await state.clear()
