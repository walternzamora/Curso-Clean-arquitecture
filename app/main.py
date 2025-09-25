from app.infrastructure.config.db import init_db
from app.infrastructure.sqlite.sqlite_product_repository import SQLiteProductRepository
from app.use_cases.list_products import ListProducts
from app.use_cases.create_product import CreateProduct
from app.use_cases.update_product import UpdateProduct
from app.use_cases.delete_product import DeleteProduct
from app.interface_adapters.http.flask_app import create_app

def build_app():
    init_db()
    repo = SQLiteProductRepository()
    list_uc = ListProducts(repo)
    create_uc = CreateProduct(repo)
    update_uc = UpdateProduct(repo)
    delete_uc = DeleteProduct(repo)
    return create_app(
        list_uc=list_uc,
        create_uc=create_uc,
        update_uc=update_uc,
        delete_uc=delete_uc,
    )

if __name__ == "__main__":
    app = build_app()
    app.run(debug=True, host="127.0.0.1", port=5000, use_reloader=False)
