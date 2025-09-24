# app/use_cases/ports/product_repository.py
from __future__ import annotations
from typing import Protocol, Iterable, Optional
from app.domain.product import Product

class ProductRepository(Protocol):
    def list(self) -> Iterable[Product]:
        ...

    def create(self, product: Product) -> Product:
        ...

    def update(self, product: Product) -> None:
        ...

    def delete(self, product_id: int) -> bool:
        ...

    def get(self, product_id: int) -> Optional[Product]:
        ...
