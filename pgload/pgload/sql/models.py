from dataclasses import dataclass
from datetime import datetime


@dataclass
class Store:
    store_id: str
    owner_email: str
    name: str
    created_at: datetime


@dataclass
class Product:
    product_id: str
    name: str
    description: str
    price: float
    quantity: int
    store_id: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Purchase:
    purchase_id: str
    product_id: str
    price: float
    purchased_at: datetime


@dataclass
class PurchaseWithStore:
    purchase_id: str
    product_id: str
    store_id: str
    price: float
    purchased_at: datetime
