from app.domain.product import Product
from app.use_cases.ports.product_repository import ProductRepository

class UpdateProduct:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    def __call__(self, *, product_id: int, name: str | None = None,
                 price: float | None = None, stock: int | None = None) -> bool:
        existing = self.repo.get(product_id)
        if not existing:
            return False
        new_name = existing.name if name is None else name
        new_price = existing.price if price is None else price
        new_stock = existing.stock if stock is None else stock
        updated = Product(id=existing.id, name=new_name, price=new_price, stock=new_stock)
        self.repo.update(updated)
        return True