from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from Parsers_aio.Main_info_crypto_parser_aio import General
from Parsers_aio.Item_info_crypto_parser_aio import Crypto
from get_crypto_volatility import calc_volatility_coeff


get_info_commands_router = Router()


# Обработчик команды "/get_total_capitalization"
@get_info_commands_router.message(Command("get_total_capitalization"))
async def get_total_capitalization(message: types.Message):
    waiting_message = await message.answer("Запрос обрабатывается...")

    curr_General = General()
    curr_capitalization = curr_General.get_data_market_capitalization()[0]
    curr_change = curr_General.get_change_market_capitalization()
    curr_change_value = curr_change[0]
    curr_direction = "увеличилась" if curr_change[2] == "up" else "уменьшилась"

    await waiting_message.delete()
    await message.answer(
        f"Общая рыночная каптилизация составляет:\n$ {curr_capitalization}\n\nРыночная капитализация {curr_direction}\nна {curr_change_value} за последние 24 часа."
    )


# Обработчик команды "/get_total_trading_volume"
@get_info_commands_router.message(Command("get_total_trading_volume"))
async def get_total_trading_volume(message: types.Message):
    waiting_message = await message.answer("Запрос обрабатывается...")

    curr_General = General()
    curr_volume = curr_General.get_total_trading_volume_per_day()[0]

    await waiting_message.delete()
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
    await state.clear()

    if "/" in message.text:
        await message.answer(
            "Ошибка!\nВы ввели команду!\nВведите команду ещё раз или повторите свои последние действия"
        )
        return

    waiting_message = await message.answer("Запрос обрабатывается...")

    try:
        curr_Crypto = Crypto(message.text)
        curr_name = curr_Crypto.get_crypto_name
        curr_capitalization = curr_Crypto.get_current_crypto_capitalization()[0]
        await waiting_message.delete()

        if curr_capitalization != "Нет информации":
            await message.answer(
                f"Рыночная капитализация {curr_name}:\n$ {curr_capitalization}"
            )
        else:
            await message.answer(f"Нет информации о рыночной капитализации {curr_name}")
    except:
        await waiting_message.delete()
        await message.answer("Введена некорректная криптовалюта")


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
    await state.clear()

    if "/" in message.text:
        await message.answer(
            "Ошибка!\nВы ввели команду!\nВведите команду ещё раз или повторите свои последние действия"
        )
        return

    waiting_message = await message.answer("Запрос обрабатывается...")

    try:
        curr_Crypto = Crypto(message.text)
        curr_name = curr_Crypto.get_crypto_name
        curr_price = curr_Crypto.get_current_average_crypto_price()[0]
        await waiting_message.delete()
        await message.answer(f"Средняя стоимость {curr_name}:\n$ {curr_price}")
    except:
        await waiting_message.delete()
        await message.answer("Введена некорректная криптовалюта")


# Класс с инициализацией машины состояний после команды "/get_crypto_volatility"
class Form_crypto_volatility(StatesGroup):
    waiting_for_message_crypto_volatility = State()


# Обработчик команды "/get_crypto_volatility"
@get_info_commands_router.message(Command("get_crypto_volatility"))
async def get_crypto_volatility(message: types.Message, state: FSMContext):
    # Установка состояния ожидания названия криптовалюты для получения её волатильности
    await state.set_state(Form_crypto_volatility.waiting_for_message_crypto_volatility)
    await message.answer(
        "Для получения волатильности криптовалютной пары, введите сокращённые названия валют и срок, за который будет получена информация, (от 1 до 365 дней) через запятую,\nнапример, BTC, usd, 30"
    )


# Обработчик состояния ожидания названия криптовалюты для получения её волатильности
@get_info_commands_router.message(
    Form_crypto_volatility.waiting_for_message_crypto_volatility
)
async def process_message_crypto_volatility(message: types.Message, state: FSMContext):
    await state.clear()

    if "/" in message.text:
        await message.answer(
            "Ошибка!\nВы ввели команду!\nВведите команду ещё раз или повторите свои последние действия"
        )
        return

    try:
        text = message.text.split(",")
    except:
        await message.answer("Некорректный формат ввода данных!")
        return

    if len(text) != 3:
        await message.answer("Некорректный формат ввода данных!")
        return

    try:
        duration = int(text[2].strip())
    except:
        await message.answer("Некорректный формат ввода данных!")
        return

    if duration < 1 or duration > 365:
        await message.answer(
            "Введена некорректная длительность, она должна принимать значения от 1 до 365"
        )
        return

    coin1 = text[0].strip().upper()
    coin2 = text[1].strip().upper()
    volatility_coeff = calc_volatility_coeff(coin1, coin2, duration)

    if volatility_coeff == "error":
        await message.answer("Введены некорректные криптовалюты")
    else:
        volatility_coeff = round(volatility_coeff, 5)
        await message.answer(
            f"Коэффициент волатильности {coin1}_{coin2} за последние {duration} дней = {volatility_coeff}\n* Чем больше коэффициент волатильности, тем стабильнее цены криптовалют друг относительно друга"
        )
