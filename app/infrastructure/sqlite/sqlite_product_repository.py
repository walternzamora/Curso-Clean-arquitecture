# app/infrastructure/sqlite/sqlite_product_repository.py

from typing import Iterable, Optional
from app.domain.product import Product
from app.use_cases.ports.product_repository import ProductRepository
from app.infrastructure.config.db import get_conn

class SQLiteProductRepository(ProductRepository):
    def list(self) -> Iterable[Product]:
        with get_conn() as conn:
            cur = conn.execute("SELECT id, name, price, stock FROM products ORDER BY id")
            for row in cur.fetchall():
                yield Product(id=row["id"], name=row["name"], price=row["price"], stock=row["stock"])

    def create(self, product: Product) -> Product:
        with get_conn() as conn:
            cur = conn.execute(
                "INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
                (product.name, product.price, product.stock),
            )
            pid = cur.lastrowid
            return Product(id=pid, name=product.name, price=product.price, stock=product.stock)

    def update(self, product: Product) -> None:
        with get_conn() as conn:
            conn.execute(
                "UPDATE products SET name = ?, price = ?, stock = ? WHERE id = ?",
                (product.name, product.price, product.stock, product.id),
            )

    def delete(self, product_id: int) -> bool:
        with get_conn() as conn:
            cur = conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
            return cur.rowcount > 0

    def get(self, product_id: int) -> Optional[Product]:
        with get_conn() as conn:
            cur = conn.execute("SELECT id, name, price, stock FROM products WHERE id = ?", (product_id,))
            row = cur.fetchone()
            if not row:
                return None
            return Product(id=row["id"], name=row["name"], price=row["price"], stock=row["stock"])
