# app/domain/product.py

from dataclasses import dataclass
from app.domain.exceptions import DomainValidationError
@dataclass(frozen=True)
class Product:
    id: int | None
    name: str
    price: float
    stock: int

    def __post_init__(self):
        name = (self.name or "").strip()
        if not name:
            raise DomainValidationError("name is required")
        if self.price is None:
            raise DomainValidationError("price is required")
        if self.price < 0:
            raise DomainValidationError("price must be >= 0")
        if self.stock is None:
            raise DomainValidationError("stock is required")
        if self.stock < 0:
            raise DomainValidationError("stock must be >= 0")
