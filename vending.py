from collections import Counter
from dataclasses import dataclass
from decimal import Decimal
import typing

ProductName = typing.NewType('ProductName', str)
SlotCode = typing.NewType('SlotCode', str)
Price = typing.NewType('Price', Decimal)
Assortment = typing.Dict[ProductName, 'Product']
Coins = typing.Counter[Decimal]
Menu = typing.Dict[ProductName, typing.Tuple[SlotCode, Price]]


class MachineOverloadedException(Exception):
    pass


@dataclass
class Product:
    name: ProductName
    quantity: int
    price: Decimal


class Machine:
    def __init__(self, slots: int, slot_depth: int) -> None:
        self._available_assortment: Assortment = {}
        self._coins: Coins = Counter()

    def load_products(self, assortment: Assortment) -> None:
        self._available_assortment = assortment

    def load_coins(self, coins: Coins) -> None:
        pass

    def get_available_products(self) -> Menu:
        ret = {name: (SlotCode("1"), product.price) for name, product in self._available_assortment.items()}
        return ret

    def choose_product(self, product_code: SlotCode, money: Coins) -> typing.Tuple[typing.Optional[Product], typing.Optional[Coins]]:
        return None, money

    def get_balance(self) -> Decimal:
        return sum([face_value * quantity for face_value, quantity in self._coins.items()])

    def cash_out(self) -> Coins:
        pass