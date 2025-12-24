from api.v1.apps.plan.service.service import insert, get_all, get_one, update, remove, get_plan_by_client_id
from fastapi import APIRouter, status, Depends
from api.v1.apps.plan.schemas.schemas import PlanSchema, PlanUpdateSchema
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_async_session

router = APIRouter()


@router.post('/create-plan/', responses={
    201: {
        "description": "Plano adquirido com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                            "id: 9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a"
                    }
                ]
            }
        },
        400: {"description": "Não é possível contratar este produto porque o prazo de venda expirou."},
        400: {"description": "Informe um valor válido para o aporte inicial."},
        400: {"description": "Informe uma idade de aposentadoria válida."},
        400: {"description": "Não é possível contratar este produto porque o valor mínimo de aporte extra é menor que R$ 100,00."},
        400: {"description": "Não é possível contratar este produto porque o valor mínimo de aporte inicial é menor que R$ 1.000"},
        400: {"description": "Não é possível contratar este produto porque a idade mínima de entrada é menor que  18 anos."},
        400: {"description": "Não é possível contratar este produto porque a idade máxima de saída é maior que 60 anos."}
}}, status_code=status.HTTP_201_CREATED)
async def create_plan(plan: PlanSchema, session: AsyncSession = Depends(get_async_session)):
    """Adquire planos para clientes que já estão cadastrados"""
    plan_data_create = plan.dict()
    return await insert(args=plan_data_create)
    
    
@router.get('/get-plan/', responses={
    200: {
        "description": "Planos listados com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "client_id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "product_id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "contribution": 1500.00,
                        "date_of_contract": "2024-11-02T20:46:03.566Z",
                        "age_of_retirement": 65
        
            }
                    
                ]
            }
        },
        500: {"description": "Erro ao listar planos"},
}}, status_code=status.HTTP_200_OK)
async def get_plan(session: AsyncSession = Depends(get_async_session)):
    """Realiza a listagem dos planos cadastrados"""   
    return await get_all(PlanSchema)
    
    
@router.get('/get-one-plan/{plan_id}/', responses={
    200: {
        "description": "Filtragem de planos pelo id realizada com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "client_id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "product_id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "contribution": 1500.00,
                        "date_of_contract": "2024-11-02T20:46:03.566Z",
                        "age_of_retirement": 65
            }
                    
                ]
            }
        },
        400: {"description": "plan_id inválido. Deve ser um UUID válido."},
}}, status_code=status.HTTP_200_OK)
async def get_one_plan(plan_id: str, session: AsyncSession = Depends(get_async_session)):
    """Filtra planos pelo id"""
    return await get_one(plan_id=plan_id)
    
    
@router.get('/filter-plan-by-client/{client_id}/', responses={
    200: {
        "description": "Filtragem de planos pelo id do cliente realizada com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "client_id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "product_id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "contribution": 1500.00,
                        "date_of_contract": "2024-11-02T20:46:03.566Z",
                        "age_of_retirement": 65
            }
                    
                ]
            }
        },
        400: {"description": "client_id inválido. Deve ser um UUID válido."},
}}, status_code=status.HTTP_200_OK)
async def filter_plan_by_client(client_id: str, session: AsyncSession = Depends(get_async_session)):
    """Filtra planos pelo id do cliente"""
    return await get_plan_by_client_id(client_id=client_id)
    

@router.put('/update-plan/{plan_id}/', 
            responses={
    200: {
        "description": "Atualização do plano realizada com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a"
                    }
                ]
            }
        },
        400: {"description": "Informe um valor válido para o aporte inicial."},
        400: {"description": "Informe uma idade de aposentadoria válida."},
        400: {"description": "Informe um prazo de venda válido."},
        400: {"description": "O valor mínimo de aporte extra é menor que R$ 100,00."},
        400: {"description": "O valor mínimo de aporte inicial é menor que R$ 1.000"},
        400: {"description": "A idade mínima de entrada é menor que  18 anos."},
        400: {"description": "A idade máxima de saída é maior que 60 anos."},
        404: {"description": "Plano não encontrado"}
}}, status_code=status.HTTP_200_OK)
async def update_plan(plan_id: str, plan: PlanUpdateSchema, session: AsyncSession = Depends(get_async_session)):
    """Atualiza planos cadastrados"""
    plan_data_update = plan.dict(exclude_unset=True)
    return await update(plan_id=plan_id, **plan_data_update)
    

@router.delete('/delete-plan/{plan_id}/', responses={
    200: {
        "description": "Plano deletado com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a"
                        
                     }
                    
                ]
            }
        },
        400: {"description": "plan inválido. Deve ser um UUID válido."},
}}, status_code=status.HTTP_200_OK)
async def delete_plan(plan_id: str, session: AsyncSession = Depends(get_async_session)):
    """Deleta planos cadastrados"""
    return await remove(plan_id=plan_id)
    
    