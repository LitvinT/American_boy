





from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from handlers.users.math import math
from keyboards.inline.users import coin_ikb
from keyboards.inline.users.general import UserCallbackData
from parser.connection import connect_to_db

user_fromilize_router = Router(name='user_formilize')


class Form(StatesGroup):
    user = State()
    coin = State()
    cost_electr = State()
    hash_rate = State()
    potr_electr = State()
    comm_pull = State()
    finish = State()


@user_fromilize_router.callback_query(UserCallbackData.filter((F.target == 'main') & (F.action == 'get')))
async def get_coin(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Form.cost_electr)

    await callback.message.delete()

    await callback.message.answer(
        text='Choose a coin',
        reply_markup=await coin_ikb()
    )


@user_fromilize_router.callback_query(UserCallbackData.filter((F.target == 'coins') & (F.action == 'get')))
async def get_cost(callback: CallbackQuery, state: FSMContext, callback_data: UserCallbackData):
    connect_to_db()

    if callback_data.coin_id == 1:
        coin = 'bitcoin'
    elif callback_data.coin_id == 2:
        coin = 'bitcoin-cash'
    elif callback_data.coin_id == 3:
        coin = 'litecoin'
    elif callback_data.coin_id == 4:
        coin = 'ethereum-classic'
    elif callback_data.coin_id == 5:
        coin = 'zcash'
    elif callback_data.coin_id == 6:
        coin = 'dash'
    elif callback_data.coin_id == 7:
        coin = 'kadena'
    elif callback_data.coin_id == 8:
        coin = 'decred'
    else:
        coin = 'bitcoin'

    user = callback.from_user.id

    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("""UPDATE users SET coin = (%s) WHERE id = (%s)""", (coin, user))
    conn.commit()

    await state.update_data(coin=callback_data.coin_id)
    await state.set_state(Form.hash_rate)

    await callback.message.answer(
        text='Enter electricity price (kW/h) in dollars:',
    )

    cur.close()
    conn.close()


@user_fromilize_router.message(Form.hash_rate)
async def get_hash(message: Message, state: FSMContext):
    connect_to_db()

    tip = message.text

    if tip.isdecimal():

        if message.text < '0':
            await message.answer(
                text='Minimum electricity price (kW/h) 0.01:',
            )
        else:
            cost = message.text

            user = message.from_user.id

            conn = connect_to_db()
            cur = conn.cursor()

            cur.execute("""UPDATE users SET cost_electricity = (%s) WHERE id = (%s)""", (cost, user))
            conn.commit()

            cur.execute("""SELECT coin FROM users WHERE id = (%s)""", (user,))

            coin_type = cur.fetchall()[0][0]

            cur.close()
            conn.close()

            await state.update_data(cost_electr=message.text)
            await state.set_state(Form.potr_electr)

            if coin_type == "bitcoin" or coin_type == "bitcoin-cash" or coin_type == "kadena" or coin_type == "decred":
                await message.answer(
                    text='Enter hashrate (Th/s):',
                )

            elif coin_type == "litecoin" or coin_type == "dash":
                await message.answer(
                    text='Enter hashrate (Gh/s):',
                )

            elif coin_type == "ethereum-classic":
                await message.answer(
                    text='Enter hashrate (Mh/s):',
                )

            elif coin_type == "zcash":
                await message.answer(
                    text='Enter hashrate (kh/s):',
                )
    else:
        try:
            float(tip)

            if message.text < '0.01':
                await message.answer(
                    text='Minimum electricity price (kWh) 0.01:',
                )
            else:
                cost = message.text

                user = message.from_user.id

                conn = connect_to_db()
                cur = conn.cursor()

                cur.execute("""UPDATE users SET cost_electricity = (%s) WHERE id = (%s)""", (cost, user))
                conn.commit()

                cur.execute("""SELECT coin FROM users WHERE id = (%s)""", (user,))
                coin_type = cur.fetchall()[0][0]

                cur.close()
                conn.close()

                await state.update_data(cost_electr=message.text)
                await state.set_state(Form.potr_electr)

                if coin_type == "bitcoin" or coin_type == "bitcoin-cash" or coin_type == "kadena" or\
                        coin_type == "decred":

                    await message.answer(
                        text='Enter hashrate (Th/s):',
                    )

                elif coin_type == "litecoin" or coin_type == "dash":
                    await message.answer(
                        text='Enter hashrate (Gh/s):',
                    )

                elif coin_type == "ethereum-classic":
                    await message.answer(
                        text='Enter hashrate (Mh/s):',
                    )

                elif coin_type == "zcash":
                    await message.answer(
                        text='Enter hashrate (kh/s):',
                    )

        except ValueError:
            await message.answer(
                text='Enter the price of electricity (kW/h) as a number:',
            )


@user_fromilize_router.message(Form.potr_electr)
async def get_potr(message: Message, state: FSMContext):
    connect_to_db()

    tip = message.text

    if tip.isdecimal():
        if message.text < '0':
            await message.answer(
                text='Enter hashrate greater than 0.09:',
            )
        else:
            hash = message.text

            user = message.from_user.id

            conn = connect_to_db()
            cur = conn.cursor()

            cur.execute("""UPDATE users SET hash = (%s) WHERE id = (%s)""", (hash, user))
            conn.commit()

            cur.close()
            conn.close()

            await state.update_data(hash_rate=message.text)
            await state.set_state(Form.comm_pull)

            await message.answer(
                text='Enter consumption (Watt):',
            )
    else:
        try:
            float(tip)

            if message.text < '0.1':
                await message.answer(
                    text='Enter hashrate greater than 0.09:',
                )

            else:
                hash = message.text

                user = message.from_user.id

                conn = connect_to_db()
                cur = conn.cursor()

                cur.execute("""UPDATE users SET hash = (%s) WHERE id = (%s)""", (hash, user))
                conn.commit()

                cur.close()
                conn.close()

                await state.update_data(hash_rate=message.text)
                await state.set_state(Form.comm_pull)

                await message.answer(
                    text='Enter consumption (Watt):',
                )

        except ValueError:
            await message.answer(
                text='Enter hashrate as a number:',
            )

@user_fromilize_router.message(Form.comm_pull)
async def get_comm(message: Message, state: FSMContext):
    connect_to_db()

    tip = message.text

    if tip.isdecimal():
        if message.text < '0':
            await message.answer(
                text='Enter consumption (Watt) greater than 0.09:',
            )
        else:
            potr = message.text
            user = message.from_user.id

            conn = connect_to_db()
            cur = conn.cursor()

            cur.execute("""UPDATE users SET potreb = (%s) WHERE id = (%s)""", (potr, user))
            conn.commit()

            cur.close()
            conn.close()

            await state.update_data(potr_electr=message.text)
            await state.set_state(Form.finish)

            await message.answer(
                text='Enter pool fee (%):',
            )
    else:
        try:
            float(tip)

            if message.text < '0.1':
                await message.answer(
                    text='Enter consumption (Watt) greater than 0.09:',
                )
            else:
                potr = message.text
                user = message.from_user.id

                conn = connect_to_db()
                cur = conn.cursor()

                cur.execute("""UPDATE users SET potreb = (%s) WHERE id = (%s)""", (potr, user))
                conn.commit()

                cur.close()
                conn.close()

                await state.update_data(potr_electr=message.text)
                await state.set_state(Form.finish)

                await message.answer(
                    text='Enter pool fee (%):',
                )

        except ValueError:
            await message.answer(
                text='Enter consumption (Watt) as a number:',
            )


@user_fromilize_router.message(Form.finish)
async def get_final(message: Message, state: FSMContext):
    tip = message.text

    if tip.isdecimal():
        if message.text < '0':
            await message.answer(
                text='Specify the pool fee (%) greater than 0.1:',
            )

        else:
            await state.update_data(comm_pull=message.text)
            await state.update_data(finish='done')

            com = message.text
            user = message.from_user.id

            connect_to_db()

            conn = connect_to_db()
            cur = conn.cursor()

            cur.execute("""UPDATE users SET komm = (%s) WHERE id = (%s)""", (com, user))
            conn.commit()

            user = message.from_user.id

            cur.execute("""SELECT cost_electricity FROM users WHERE id = (%s)""", (user,))
            conn.commit()
            cost_electricity = cur.fetchall()[0][0]

            cur.execute("""SELECT hash FROM users WHERE id = (%s)""", (user,))
            conn.commit()
            hash = cur.fetchall()[0][0]

            cur.execute("""SELECT potreb FROM users WHERE id = (%s)""", (user,))
            conn.commit()
            potreb = cur.fetchall()[0][0]

            cur.execute("""SELECT komm FROM users WHERE id = (%s)""", (user,))
            conn.commit()
            komm = cur.fetchall()[0][0]

            cur.execute("""SELECT coin FROM users WHERE id = (%s)""", (user,))
            conn.commit()
            coin_type = (cur.fetchall()[0][0]).capitalize()

            result = math(coin_type, cost_electricity, hash, potreb, komm)

            if coin_type == "Bitcoin":
                coin = 'BTC'
                hashrate = 'Th/s'

            elif coin_type == "Litecoin":
                coin = 'LTC'
                hashrate = 'Gh/s'

            elif coin_type == "Ethereum-classic":
                coin = 'ETC'
                hashrate = 'Mh/s'

            elif coin_type == "Zcash":
                coin = 'ZEC'
                hashrate = 'kh/s'

            elif coin_type == "Bitcoin-cash":
                coin = 'BCH'
                hashrate = 'Th/s'

            elif coin_type == "Kadena":
                coin = 'KDA'
                hashrate = 'Th/s'

            elif coin_type == "Decred":
                coin = 'DCR'
                hashrate = 'Th/s'

            else:
                coin = 'DASH'
                hashrate = 'Gh/s'

            await message.answer(
                text=f"Coin: {coin_type}"
                     f"\nCurrency: USD"
                     f"\nElectricity price: {cost_electricity}"
                     f"\nYour hashrate: {hash} {hashrate} "
                     f"\nElectricity consumption: {potreb} Watt"
                     f"\nPool fee: {komm} %"
                     "\n\n💵 PROFIT"
                     f"\n{result[-4]} $ (in 1 hour)"
                     f"\n{result[-3]} $ (in 1 day)"
                     f"\n{result[-2]} $ (in 1 week)"
                     f"\n{result[-1]} $ (in 1 month)"
                     "\n\n🥇 REWARD"
                     f"\n{result[0]} {coin} (in 1 hour)"
                     f"\n{result[1]} {coin} (in 1 day)"
                     f"\n{result[2]} {coin} (in 1 week)"
                     f"\n{result[3]} {coin} (in 1 month)"
                     "\n\n➕ INCOME"
                     f"\n{result[4]} $ (in 1 hour)"
                     f"\n{result[5]} $ (in 1 day)"
                     f"\n{result[6]} $ (in 1 week)"
                     f"\n{result[7]} $ (in 1 month)"
                     "\n\n➖ EXPENSES"
                     f"\n{result[8]} $ (in 1 hour)"
                     f"\n{result[9]} $ (in 1 day)"
                     f"\n{result[10]} $ (in 1 week)"
                     f"\n{result[11]} $ (in 1 month)",
            )

            date = str(datetime.now())
            user = message.from_user.id

            cur.execute("""UPDATE users SET date = (%s) WHERE id = (%s)""", (date, user))
            conn.commit()

            await state.clear()

            cur.close()
            conn.close()

    else:
        try:
            float(tip)

            if message.text < '0.1':
                await message.answer(
                    text='Enter pool fee (%) greater than 0.1:',
                )
            else:
                await state.update_data(comm_pull=message.text)
                await state.update_data(finish='done')

                com = message.text
                user = message.from_user.id

                connect_to_db()

                conn = connect_to_db()
                cur = conn.cursor()

                cur.execute("""UPDATE users SET komm = (%s) WHERE id = (%s)""", (com, user))
                conn.commit()

                user = message.from_user.id

                cur.execute("""SELECT cost_electricity FROM users WHERE id = (%s)""", (user,))
                conn.commit()
                cost_electricity = cur.fetchall()[0][0]

                cur.execute("""SELECT hash FROM users WHERE id = (%s)""", (user,))
                conn.commit()
                hash = cur.fetchall()[0][0]

                cur.execute("""SELECT potreb FROM users WHERE id = (%s)""", (user,))
                conn.commit()
                potreb = cur.fetchall()[0][0]

                cur.execute("""SELECT komm FROM users WHERE id = (%s)""", (user,))
                conn.commit()
                komm = cur.fetchall()[0][0]

                cur.execute("""SELECT coin FROM users WHERE id = (%s)""", (user,))
                conn.commit()
                coin_type = (cur.fetchall()[0][0]).capitalize()

                result = math(coin_type, cost_electricity, hash, potreb, komm)

                if coin_type == "Bitcoin":
                    coin = 'BTC'
                    hashrate = 'Th/s'

                elif coin_type == "Litecoin":
                    coin = 'LTC'
                    hashrate = 'Gh/s'

                elif coin_type == "Ethereum-classic":
                    coin = 'ETC'
                    hashrate = 'Mh/s'

                elif coin_type == "Zcash":
                    coin = 'ZEC'
                    hashrate = 'kh/s'

                elif coin_type == "Bitcoin-cash":
                    coin = 'BCH'
                    hashrate = 'Th/s'

                elif coin_type == "Kadena":
                    coin = 'KDA'
                    hashrate = 'Th/s'

                elif coin_type == "Decred":
                    coin = 'DCR'
                    hashrate = 'Th/s'

                else:
                    coin = 'DASH'
                    hashrate = 'Gh/s'

                await message.answer(
                    text=f"Coin: {coin_type}"
                         f"\nCurrency: USD"
                         f"\nElectricity price: {cost_electricity}"
                         f"\nYour hashrate: {hash} {hashrate} "
                         f"\nElectricity consumption: {potreb} Watt"
                         f"\nPool fee: {komm} %"
                         "\n\n💵 PROFIT"
                         f"\n{result[-4]} $ (in 1 hour)"
                         f"\n{result[-3]} $ (in 1 day)"
                         f"\n{result[-2]} $ (in 1 week)"
                         f"\n{result[-1]} $ (in 1 month)"
                         "\n\n🥇 REWARD"
                         f"\n{result[0]} {coin} (in 1 hour)"
                         f"\n{result[1]} {coin} (in 1 day)"
                         f"\n{result[2]} {coin} (in 1 week)"
                         f"\n{result[3]} {coin} (in 1 month)"
                         "\n\n➕ INCOME"
                         f"\n{result[4]} $ (in 1 hour)"
                         f"\n{result[5]} $ (in 1 day)"
                         f"\n{result[6]} $ (in 1 week)"
                         f"\n{result[7]} $ (in 1 month)"
                         "\n\n➖ EXPENSES"
                         f"\n{result[8]} $ (in 1 hour)"
                         f"\n{result[9]} $ (in 1 day)"
                         f"\n{result[10]} $ (in 1 week)"
                         f"\n{result[11]} $ (in 1 month)",
                )

                date = str(datetime.now())
                user = message.from_user.id

                cur.execute("""UPDATE users SET date = (%s) WHERE id = (%s)""", (date, user))
                conn.commit()

                await state.clear()

                cur.close()
                conn.close()

        except ValueError:
            await message.answer(
                text='Enter pool fee (%) as a number:',
            )

        await state.clear()

