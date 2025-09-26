# tests/test_use_case_create.py
from app.use_cases.create_product import CreateProduct
from app.domain.product import Product
from app.use_cases.ports.product_repository import ProductRepository

class DummyRepo(ProductRepository):
    def __init__(self): self.created = []
    def list(self): return []
    def create(self, product: Product) -> Product:
        self.created.append(product)
        return Product(id=1, name=product.name, price=product.price, stock=product.stock)
    def update(self, product: Product): pass
    def delete(self, product_id: int) -> bool: return True
    def get(self, product_id: int): return None

def test_create_product_uc():
    uc = CreateProduct(DummyRepo())
    p = uc(name="Phone", price=99.9, stock=3)
    assert p.id == 1 and p.name == "Phone"
