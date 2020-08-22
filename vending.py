from copy import deepcopy
from collections import Counter
from dataclasses import dataclass
from decimal import Decimal
from functools import lru_cache
import math
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


def money_to_value(money: Coins) -> Decimal:
        return sum([face_value * quantity for face_value, quantity in money.items()])


def num_ways(n: int) -> int:
    pass

@lru_cache(maxsize=64)
def can_get_change(money: Coins, value: Decimal) -> bool:
    print(money, value)
    if value == 0:
        return True
    if value < 0:
        return False
    for coin in money:
        new_money = money.copy()
        new_money[coin] -= 1
        new_money += Counter()
        new_value = value - coin
        if can_get_change(new_money, new_value):
            return True
    return False

class Machine:
    def __init__(self, slots: int, slot_depth: int) -> None:
        self._coins: Coins = Counter()
        self._slots: typing.Dict[SlotCode, Product] = {}
        self._slots_quantity = slots
        self._slot_depth = slot_depth

    def load_products(self, assortment: Assortment) -> None:
        for item in assortment.items():
            self._fit_product(item)

    def _fit_product(self, item: typing.Tuple[ProductName, Product]) -> None:
        name, product = item
        free_slots = self._slots_quantity - len(self._slots)
        if free_slots == 0:
            raise MachineOverloadedException
        free_places = free_slots * self._slot_depth
        if free_places < product.quantity:
            raise MachineOverloadedException
        taken_slots = math.ceil(product.quantity / self._slot_depth)
        codes = list(set(range(self._slots_quantity)) - self._slots.keys())[:taken_slots]
        remaining_places = product.quantity
        for code in codes:
            taken_places = min(self._slot_depth, remaining_places)
            self._slots[code] = Product(name, taken_places, product.price)
            remaining_places -= taken_places

    def load_coins(self, coins: Coins) -> None:
        self._coins.update(coins)

    def get_available_products(self) -> Menu:
        ret = {product.name: (code, product.price) for code, product in self._slots.items()}
        return ret

    def _get_change(self, money: Coins, value_to_change: Decimal) -> typing.Optional[Coins]:
        pass

    def choose_product(self, product_code: SlotCode, money: Coins) -> typing.Tuple[typing.Optional[Product], typing.Optional[Coins]]:
        product = self._slots.get(product_code)
        if not product:
            return None, money
        value = money_to_value(money)
        if value < product.price:
            return None, money
        value_to_change = product.price - value
        if value_to_change == 0:
            product.quantity -= 1
            if product.quantity == 0:
                del self._slots[product_code]
            return Product(product.name, 1, product.price), None
        change = self._get_change(money, value_to_change)
        if not change:
            return None, money
        else:
            product.quantity -= 1
            if product.quantity == 0:
                del self._slots[product_code]
            return Product(product.name, 1, product.price), change

    def get_balance(self) -> Decimal:
        return money_to_value(self._coins)

    def cash_out(self) -> Coins:
        ret = deepcopy(self._coins)
        self._coins = Counter()
        return ret
