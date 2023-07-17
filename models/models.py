from sqlalchemy import Column, Integer, VARCHAR, select, Boolean, BigInteger, SmallInteger
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base


from loader import DATABASE_URL

Base = declarative_base()

class BaseMixin(object):
    id = Column(Integer, primary_key=True)

    engine = create_async_engine(f'postgresql+asyncpg://{DATABASE_URL}')

    def __init__(self, **kwargs) -> None:
        for kw in kwargs.items():
            self.__getattribute__(kw[0])
            self.__setattr__(*kw)

    @staticmethod
    def create_async_session(func):
        async def wrapper(*args, **kwargs):
            async with AsyncSession(bind=BaseMixin.engine) as session:
                return await func(*args, **kwargs, session=session)

        return wrapper

    @create_async_session
    async def save(self, session: AsyncSession = None) -> None:
        session.add(self)
        await session.commit()
        await session.refresh(self)

    @classmethod
    @create_async_session
    async def get(cls, pk: int, session: AsyncSession = None) -> Base:
        return await session.get(cls, pk)

    @classmethod
    @create_async_session
    async def all(cls, order_by: str = 'id', session: AsyncSession = None, **kwargs) -> list[Base]:
        return [obj[0] for obj in await session.execute(select(cls).filter_by(**kwargs).order_by(order_by))]

    @create_async_session
    async def delete(self, session: AsyncSession = None) -> None:
        await session.delete(self)
        await session.commit()


class Coin(BaseMixin, Base):
    __tablename__: str = 'coins'

    id = Column(SmallInteger, primary_key=True)
    name = Column(VARCHAR(64), nullable=False, unique=True)
    is_published = Column(Boolean, default=True)

    def __str__(self):
        return self.name


class User(BaseMixin, Base):
    __tablename__: str = 'users'

    id = Column(BigInteger, primary_key=True)
    name = Column(VARCHAR(128), nullable=True)
    username = Column(VARCHAR(128), nullable=True)
    coin = Column(VARCHAR(24), nullable=True)
    cost_electricity = Column(VARCHAR(128), nullable=True)
    hash = Column(VARCHAR(128), nullable=True)
    potreb = Column(VARCHAR(128), nullable=True)
    komm = Column(VARCHAR(128), nullable=True)
    date = Column(VARCHAR(28), nullable=True)

    def __str__(self):
        return self.id


class Calculator(BaseMixin, Base):
    __tablename__: str = 'calculator'

    id = Column(BigInteger, primary_key=True)
    name = Column(VARCHAR(128), nullable=False, unique=True)
    is_published = Column(Boolean, default=True)

    def __str__(self):
        return self.id

class Admin(BaseMixin, Base):
    __tablename__: str = 'admin'

    id = Column(BigInteger, primary_key=True)
    name = Column(VARCHAR(32), nullable=False)


