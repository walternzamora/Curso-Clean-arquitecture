from app.use_cases.ports.product_repository import ProductRepository

class DeleteProduct:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    def __call__(self, product_id: int) -> bool:
        return self.repo.delete(product_id)