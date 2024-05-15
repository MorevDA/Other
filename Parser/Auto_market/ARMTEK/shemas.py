from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Suggestion:
    price: float
    value: int
    min_delivery_time: int
    max_delivery_time: int


@dataclass
class Part:
    brand: str
    part_number: str
    name: str
    artid: str = None
    suggestions: list[Suggestion] = field(default_factory=list)


@dataclass
class Shop:
    shop_name: str
    original_parts: Part = None
    analog_parts: list[Part] = field(default_factory=list)
