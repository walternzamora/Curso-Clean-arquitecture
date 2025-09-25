# app/interface_adapters/http/flask_app.py
from flask import Flask, jsonify, request
from app.use_cases.list_products import ListProducts
from app.use_cases.create_product import CreateProduct
from app.use_cases.update_product import UpdateProduct
from app.use_cases.delete_product import DeleteProduct

def create_app(*, list_uc: ListProducts, create_uc: CreateProduct,
               update_uc: UpdateProduct, delete_uc: DeleteProduct) -> Flask:
    app = Flask(__name__)

    @app.get("/ping")
    def ping():
        return {"status": "ok"}

    @app.get("/products")
    def list_products():
        items = [p.__dict__ for p in list_uc()]
        return jsonify(items)

    @app.post("/products")
    def create_product():
        data = request.get_json() or {}
        name = (data.get("name") or "").strip()
        price = float(data.get("price"))
        stock = int(data.get("stock", 0))
        product = create_uc(name=name, price=price, stock=stock)
        return jsonify(product.__dict__), 201

    @app.put("/products/<int:pid>")
    def update_product(pid: int):
        data = request.get_json() or {}
        ok = update_uc(
            product_id=pid,
            name=data.get("name"),
            price=float(data["price"]) if "price" in data else None,
            stock=int(data["stock"]) if "stock" in data else None,
        )
        if not ok:
            return jsonify({"error": "product not found"}), 404
        return jsonify({"status": "ok"})

    @app.delete("/products/<int:pid>")
    def delete_product(pid: int):
        ok = delete_uc(pid)
        if not ok:
            return jsonify({"error": "product not found"}), 404
        return jsonify({"status": "deleted"})

    return app
