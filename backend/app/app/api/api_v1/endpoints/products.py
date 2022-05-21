import csv
import os
from tempfile import NamedTemporaryFile
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.models import Product

router = APIRouter()


@router.get("/", response_model=List[schemas.Product])
def read_products(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
       
) -> Any:
    """
    Retrieve products.
    """
    products = crud.product.get_multi(db, skip=skip, limit=limit)
    return products


@router.post("/", response_model=schemas.Product)
def create_product(
        *,
        db: Session = Depends(deps.get_db),
        product_in: schemas.ProductCreate,
       
) -> Any:
    """
    Create new product.
    """
    product = crud.product.create(db=db, obj_in=product_in)
    return product


@router.post("/batch", response_model=List[schemas.Product])
async def batch(file: UploadFile = File(...), db: Session = Depends(deps.get_db)):
    contents = await file.read()
    data = []
    file_copy = NamedTemporaryFile(delete=False)
    try:
        with file_copy as f:  # The 'with' block ensures that the file closes and data are stored
            f.write(contents)
        with open(file_copy.name, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                data.append(row)
        response = []
        for product in data[1::]:
            new_product = Product()
            new_product.id = product[0].split(',')[0]
            new_product.product_name = product[0].split(',')[2]
            new_product.offer_id = product[0].split(',')[1]
            existing_product = crud.product.get(db=db, id=new_product.id)
            if not existing_product:
                response.append(crud.product.create(db=db, obj_in=new_product))
            else:
                response.append(crud.product.update(db=db, db_obj=existing_product, obj_in=new_product.__dict__))
        return response
    finally:
        file_copy.close()  # Remember to close any file instances before removing the temp file
        os.unlink(file_copy.name)  # delete


@router.put("/{id}", response_model=schemas.Product)
def update_product(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        product_in: schemas.ProductUpdate,
       
) -> Any:
    """
    Update an product.
    """
    product = crud.product.get(db=db, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    
    product = crud.product.update(db=db, db_obj=product, obj_in=product_in)
    return product


@router.get("/{id}", response_model=schemas.Product)
def read_product(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
       
) -> Any:
    """
    Get product by ID.
    """
    product = crud.product.get_by_key(db=db, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    
    return product


@router.delete("/{id}", response_model=schemas.Product)
def delete_product(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
       
) -> Any:
    """
    Delete an product.
    """
    product = crud.product.get(db=db, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    
    product = crud.product.remove(db=db, id=id)
    return product
