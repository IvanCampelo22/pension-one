from api.v1.apps.products.service.service import insert, get_all, get_one, update, remove, get_products_by_name
from api.v1.apps.products.schemas.schemas import ProductsSchema, ProductsUpdateSchema
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, status, Depends
from database.session import get_async_session

router = APIRouter()

@router.post('/create-product/', responses={
    201: {
        "description": "Produto adquirido com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",               
                    }
                ]
            }
        },
        400: {"description": "Informe um nome para o produto."},
        400: {"description": "Informe um código SUSEP para o produto."},
        400: {"description": "Não é possível fazer um aporte extra  para este produto, porque o valor tem que ser acima de R$ 100,00."},
        400: {"description": "Não é possível comprar este produto, porque o valor tem que ser acima de R$ 1.000"},
        400: {"description": "Não é possível obter este produto, porque a idade mínima é de 18 anos."},
        400: {"description": "A idade máxima para começar a usufruir deste produto é de 60 anos."}
}}, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductsSchema, session: AsyncSession = Depends(get_async_session)):
    """Adquire produtos para clientes que já estão cadastrados"""
    product_data_create = product.dict()
    return await insert(args=product_data_create)
    

@router.get('/get-product/', responses={
    200: {
        "description": "Listagem de produtos realizada com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "name": "Produto Teste",
                        "susep": "1234567890",
                        "expiration_of_sale": "2025-11-02T19:30:24.117000+00:00",  
                        "value_minimum_aporte_initial": 1000.00,
                        "value_minimum_aporte_extra": 500.00,
                        "entry_age": 18,
                        "age_of_exit": 45,
                        "lack_initial_of_rescue": 60,
                        "lack_entre_resgates": 30 
                    }
                ]
            }
        },
        500: {"description": "Erro ao listar produtos"},
}}, status_code=status.HTTP_200_OK)
async def get_product(session: AsyncSession = Depends(get_async_session)):
    """Listagem dos produtos cadastrados"""   
    return await get_all(ProductsSchema)


@router.get('/get-one-product/{product_id}/', responses={
    200: {
        "description": "Filtragem de produtos pelo id realizada com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "name": "Produto Teste",
                        "susep": "1234567890",
                        "expiration_of_sale": "2025-11-02T19:30:24.117000+00:00",  
                        "value_minimum_aporte_initial": 1000.00,
                        "value_minimum_aporte_extra": 500.00,
                        "entry_age": 18,
                        "age_of_exit": 45,
                        "lack_initial_of_rescue": 60,
                        "lack_entre_resgates": 30 
                    }
                ]
            }
        },
        400: {"description": "product_id inválido. Deve ser um UUID válido."},
}}, status_code=status.HTTP_200_OK)
async def get_one_product(product_id: str, session: AsyncSession = Depends(get_async_session)):
    """Filtra produtos pelo id"""
    return await get_one(product_id=product_id)
    

@router.get('/filter-product-by-name/', responses={
    200: {
        "description": "Filtragem de produtos pelo nome realizada com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "name": "Produto Teste",
                        "susep": "1234567890",
                        "expiration_of_sale": "2025-11-02T19:30:24.117000+00:00",  
                        "value_minimum_aporte_initial": 1000.00,
                        "value_minimum_aporte_extra": 500.00,
                        "entry_age": 18,
                        "age_of_exit": 45,
                        "lack_initial_of_rescue": 60,
                        "lack_entre_resgates": 30 
                    }
                ]
            }
        },
        400: {"description": "Informe um nome válido para o produto."},
        400: {"description": "Informe um nome para o produto."},
}}, status_code=status.HTTP_200_OK)
async def filter_product_by_name(product_name: str, session: AsyncSession = Depends(get_async_session)):
    """Filtra produtos pelo nome"""
    return await get_products_by_name(product_name=product_name)
    

@router.put('/update-product/{product_id}/', responses={
    200: {
        "description": "Atualização de produto realizada com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "name": "Produto Teste",
                        "susep": "1234567890",
                        "expiration_of_sale": "2025-11-02T19:30:24.117000+00:00",  
                        "value_minimum_aporte_initial": 1000.00,
                        "value_minimum_aporte_extra": 500.00,
                        "entry_age": 18,
                        "age_of_exit": 45,
                        "lack_initial_of_rescue": 60,
                        "lack_entre_resgates": 30 
                    }
                ]
            }
        },
        400: {"description": "plan_id inválido. Deve ser um UUID válido."},
        400: {"description": "O valor tem que ser acima de R$ 100,00."},
        400: {"description": "O valor tem que ser acima de R$ 1.000"},
        400: {"description": "A idade mínima é de 18 anos."},
        400: {"description": "A idade precisa ser acima de 60 anos."},
        404: {"description": "Produto não encontrado"},
}}, status_code=status.HTTP_200_OK)
async def update_product(product_id: str, product: ProductsUpdateSchema, session: AsyncSession = Depends(get_async_session)):
    """Atualiza produtos cadastrados"""
    product_data_update = product.dict(exclude_unset=True)
    return await update(product_id=product_id, **product_data_update)
    

@router.delete('/delete-product/{product_id}/', responses={
    200: {
        "description": "Produto deletado com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                    }
                ]
            }
        },
        400: {"description": "Informe um nome válido para o produto."},
}}, status_code=status.HTTP_200_OK)
async def delete_product(product_id: str, session: AsyncSession = Depends(get_async_session)):
    """Deleta produtos cadastrados"""
    return await remove(product_id=product_id)
    
    