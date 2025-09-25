import pytest
from app.domain.product import Product
from app.domain.exceptions import DomainValidationError


def test_product_ok():
    p = Product(id=None, name="A", price=1.0, stock=0)
    assert p.name == "A"


def test_product_name_required():
    with pytest.raises(DomainValidationError):
        Product(id=None, name="   ", price=1.0, stock=0)

