# app/infrastructure/memory/inmemory_product_repository.py
from typing import Iterable, Optional
from app.domain.product import Product
from app.use_cases.ports.product_repository import ProductRepository

class InMemoryProductRepository(ProductRepository):
    def __init__(self):
        self._items: dict[int, Product] = {}
        self._auto = 0

    def list(self) -> Iterable[Product]:
        return list(self._items.values())

    def create(self, product: Product) -> Product:
        self._auto += 1
        p = Product(id=self._auto, name=product.name, price=product.price, stock=product.stock)
        self._items[p.id] = p
        return p

    def update(self, product: Product) -> None:
        if product.id in self._items:
            self._items[product.id] = product

    def delete(self, product_id: int) -> bool:
        return self._items.pop(product_id, None) is not None

    def get(self, product_id: int) -> Optional[Product]:
        return self._items.get(product_id)