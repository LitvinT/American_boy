from models import Calculator, Category



async def main():
    # start = ['Сalculator']
    # for s in start:
    #     s = Calculator(
    #         name=s
    #     )
    #     await s.save()

    coins = ["bitcoin", "bitcoin-cash", "litecoin", "ethereum-classic", "zcash", "dash"]
    for co in coins:
        co = Category(
            name=co,
        )
        await co.save()


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())