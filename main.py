from models import Calculator, Coin


async def main():
    start = ['Calculator']
    for s in start:
        s = Calculator(
            name=s,
        )
        await s.save()

    coins = ["bitcoin", "bitcoin-cash", "litecoin", "ethereum-classic", "zcash", "dash", "kadena", "decred"]
    for co in coins:
        co = Coin(
            name=co,
        )
        await co.save()


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())