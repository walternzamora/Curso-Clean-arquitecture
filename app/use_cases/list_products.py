# app/use_cases/list_products.py
from typing import Iterable
from app.domain.product import Product
from app.use_cases.ports.product_repository import ProductRepository

class ListProducts:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    def __call__(self) -> Iterable[Product]:
        return self.repo.list()
