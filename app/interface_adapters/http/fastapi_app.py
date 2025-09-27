from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from app.use_cases.list_products import ListProducts
from app.use_cases.create_product import CreateProduct
from app.use_cases.update_product import UpdateProduct
from app.use_cases.delete_product import DeleteProduct
from app.domain.exceptions import DomainValidationError


# DTOs solo en el adaptador (no tocan dominio)
class ProductIn(BaseModel):
    name: str = Field(..., min_length=1)
    price: float = Field(..., ge=0)
    stock: int = Field(0, ge=0)

class ProductPatch(BaseModel):
    name: Optional[str] = Field(None)
    price: Optional[float] = Field(None, ge=0)
    stock: Optional[int] = Field(None, ge=0)


class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    stock: int




def create_app(*, list_uc: ListProducts, create_uc: CreateProduct,
    update_uc: UpdateProduct, delete_uc: DeleteProduct) -> FastAPI:
    app = FastAPI(title="Clean Architecture – Products API (FastAPI)")


    @app.get("/ping")
    def ping():
        return {"status": "ok"}


    @app.get("/products", response_model=List[ProductOut])
    def list_products():
        items = [p.__dict__ for p in list_uc()]
        return items


    @app.post("/products", response_model=ProductOut, status_code=201)
    def create_product(payload: ProductIn):
        try:
            product = create_uc(name=payload.name.strip(), price=payload.price, stock=payload.stock)
            return product.__dict__
        except DomainValidationError as ex:
            raise HTTPException(status_code=400, detail=str(ex))


        @app.put("/products/{pid}")
        def update_product(pid: int, patch: ProductPatch):
            try:
                ok = update_uc(
                product_id=pid,
                name=patch.name.strip() if patch.name is not None else None,
                price=patch.price,
                stock=patch.stock,
            )
                if not ok:
                    raise HTTPException(status_code=404, detail="product not found")
                return {"status": "ok"}
            except DomainValidationError as ex:
                raise HTTPException(status_code=400, detail=str(ex))


        @app.delete("/products/{pid}")
        def delete_product(pid: int):
            ok = delete_uc(pid)
            if not ok:
                raise HTTPException(status_code=404, detail="product not found")
            return {"status": "deleted"}

    return app