from copy import deepcopy
from collections import Counter
from dataclasses import dataclass
from decimal import Decimal
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


def get_change(money: Coins, value: Decimal, change: Coins) -> typing.Optional[Coins]:
    if value == 0:
        return change
    if value < 0:
        return None
    for coin in money:
        new_money = money.copy()
        new_money[coin] -= 1
        new_change = change.copy()
        new_change.update({coin: 1})
        new_money += Counter()
        new_value = value - coin
        ret = get_change(new_money, new_value, new_change)
        if ret:
            return ret
    return None


class Machine:
    def __init__(self, slots: int, slot_depth: int) -> None:
        self._coins: Coins = Counter()
        self._slots: typing.Dict[SlotCode, Product] = {}
        self._slots_quantity = slots
        self._slot_depth = slot_depth

    def load_products(self, assortment: Assortment) -> None:
        for item in assortment.items():
            self._fit_product(item)

    def load_coins(self, coins: Coins) -> None:
        self._coins.update(coins)

    def get_available_products(self) -> Menu:
        return {product.name: (code, product.price) for code, product in self._slots.items()}

    def choose_product(self, product_code: SlotCode, money: Coins) -> typing.Tuple[typing.Optional[Product], typing.Optional[Coins]]:
        product = self._slots.get(product_code)
        if not product:
            return None, money
        value = money_to_value(money)
        if value < product.price:
            return None, money
        value_to_change = value - product.price
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

    def _get_change(self, money: Coins, value_to_change: Decimal) -> typing.Optional[Coins]:
        change = get_change(money, value_to_change, Counter())
        if change:
            return change
        change = get_change(Counter({**money, **self._coins}), value_to_change, Counter())
        if change:
            return change
        return None

    def _load_more(self, product: Product) -> Product:
        for code in self._slots:
            if self._slots[code].name == product.name:
                how_much_to_load = min(self._slot_depth - self._slots[code].quantity, product.quantity)
                self._slots[code].quantity += how_much_to_load
                product.quantity -= how_much_to_load
        return product

    def _fit_product(self, item: typing.Tuple[ProductName, Product]) -> None:
        name, product = item
        product = self._load_more(product)
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