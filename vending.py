from collections import Counter
from dataclasses import dataclass
from decimal import Decimal
import typing

ProductName = typing.NewType('ProductName', str)
SlotCode = typing.NewType('SlotCode', str)
Assortment = typing.Dict[ProductName, 'Product']
Coins = Counter[Decimal, int]
Menu = typing.Dict[ProductName, typing.Tuple[SlotCode, Decimal]]


class MachineOverloadedException(Exception):
    pass


@dataclass
class Product:
    name: ProductName
    quantity: int
    price: Decimal


class Machine:
    def __init__(self, slots: int, slot_depth: int) -> None:
        pass

    def load_products(self, assortment: Assortment) -> None:
        pass

    def load_coins(self, coins: Coins) -> None:
        pass

    def get_available_products(self) -> Menu:
        pass

    def choose_product(self, product_code: SlotCode, money: Coins) -> typing.Tuple[typing.Optional[Product], typing.Optional[Coins]]:
        pass

    def get_balance(self) -> Decimal:
        pass

    def cash_out(self) -> Coins:
        pass