# app/infrastructure/mysql/mysql_product_repository.py
from typing import Iterable, Optional
from decimal import Decimal
from app.domain.product import Product
from app.use_cases.ports.product_repository import ProductRepository
from app.infrastructure.config.mysql import get_conn

def _to_float(value) -> float:
    """Convierte DECIMAL/str a float para la entidad Product."""
    if isinstance(value, Decimal):
        return float(value)
    return float(value)

class MySQLProductRepository(ProductRepository):
    def list(self) -> Iterable[Product]:
        conn = get_conn()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT id, name, price, stock FROM products ORDER BY id")
            rows = cur.fetchall()
            return [
                Product(
                    id=row["id"],
                    name=row["name"],
                    price=_to_float(row["price"]),
                    stock=row["stock"],
                )
                for row in rows
            ]
        finally:
            conn.close()

    def create(self, product: Product) -> Product:
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)",
                (product.name, product.price, product.stock),
            )
            conn.commit()
            pid = cur.lastrowid
            return Product(id=pid, name=product.name, price=product.price, stock=product.stock)
        finally:
            conn.close()

    def update(self, product: Product) -> None:
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE products SET name=%s, price=%s, stock=%s WHERE id=%s",
                (product.name, product.price, product.stock, product.id),
            )
            conn.commit()
        finally:
            conn.close()

    def delete(self, product_id: int) -> bool:
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM products WHERE id=%s", (product_id,))
            conn.commit()
            return cur.rowcount > 0
        finally:
            conn.close()

    def get(self, product_id: int) -> Optional[Product]:
        conn = get_conn()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                "SELECT id, name, price, stock FROM products WHERE id=%s",
                (product_id,),
            )
            row = cur.fetchone()
            if not row:
                return None
            return Product(
                id=row["id"],
                name=row["name"],
                price=_to_float(row["price"]),
                stock=row["stock"],
            )
        finally:
            conn.close()
