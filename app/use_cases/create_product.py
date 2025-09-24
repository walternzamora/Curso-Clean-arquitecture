# app/use_cases/create_product.py
from app.domain.product import Product
from app.use_cases.ports.product_repository import ProductRepository

class CreateProduct:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    def __call__(self, *, name: str, price: float, stock: int = 0) -> Product:
        # La validación ocurre al construir la entidad (dominio)
        p = Product(id=None, name=name, price=price, stock=stock)
        return self.repo.create(p)
