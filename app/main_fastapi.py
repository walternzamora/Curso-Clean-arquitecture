from app.infrastructure.config.db import init_db # si usas SQLite
from app.infrastructure.sqlite.sqlite_product_repository import SQLiteProductRepository
# Si quieres probar memoria, cambia la importación:
# from app.infrastructure.memory.inmemory_product_repository import InMemoryProductRepository


from app.use_cases.list_products import ListProducts
from app.use_cases.create_product import CreateProduct
from app.use_cases.update_product import UpdateProduct
from app.use_cases.delete_product import DeleteProduct
from app.interface_adapters.http.fastapi_app import create_app


# Construye la app inyectando casos de uso
repo = SQLiteProductRepository()
# repo = InMemoryProductRepository() # ← cambia repositorio sin tocar reglas


init_db() # si usas SQLite; quítalo si usas memoria


list_uc = ListProducts(repo)
create_uc = CreateProduct(repo)
update_uc = UpdateProduct(repo)
delete_uc = DeleteProduct(repo)


app = create_app(
    list_uc=list_uc,
    create_uc=create_uc,
    update_uc=update_uc,
    delete_uc=delete_uc,
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main_fastapi:app", host="127.0.0.1", port=8000, reload=True)