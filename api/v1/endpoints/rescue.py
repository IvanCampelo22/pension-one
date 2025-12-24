from api.v1.apps.rescue.service.service import insert, get_all, get_one, update, remove, get_rescue_by_plan_id
from api.v1.apps.rescue.schemas.schemas import RescueSchema, RescueUpdateSchema
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, status, Depends
from database.session import get_async_session

router = APIRouter()

@router.post('/create-rescue/', responses={
    201: {
        "description": "Resgate realizado com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a"
                    }
                    
                ]
            }
        },
        400: {"description": "Não há saldo suficiente para resgatar o valor informado."},
        404: {"description": "Plano ou produto não encontrado"},
        400: {"description": "Carência inicial de resgate de 60 dias não foi cumprida."}
    }
}, status_code=status.HTTP_201_CREATED)
async def create_rescue(rescue: RescueSchema, session: AsyncSession = Depends(get_async_session)):
    """Realiza resgates para clientes que já estão cadastrados e segue o plano de benefícios"""
    rescue_data_create = rescue.dict()
    return await insert(args=rescue_data_create)


@router.get('/get-rescue/', responses={
    200: {
        "description": "Listagrem de resgates realizados com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "plan_id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "rescue_value": 2000.00
                    }
                ]
            }
        },
        500: {"description": "Erro ao listar resgates"},
    }
}, status_code=status.HTTP_200_OK)
async def get_rescue(session: AsyncSession = Depends(get_async_session)):
    """Faz a listagem de todos os resgates realizados"""   
    return await get_all(RescueSchema)
    

@router.get('/get-one-rescue/{rescue_id}/', responses={
    200: {
        "description": "Filtro de resgate realizado com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "plan_id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "rescue_value": 2000.00
                    }
                    
                ]
            }
        },
        400: {"description": "rescue_id inválido. Deve ser um UUID válido."},
    }
}, status_code=status.HTTP_200_OK)
async def get_one_rescue(rescue_id: str, session: AsyncSession = Depends(get_async_session)):
    """Filtra resgate pelo id"""
    return await get_one(rescue_id=rescue_id)


@router.get('/filter-rescue-by-plan/', responses={
    200: {
        "description": "Filtro de resgate realizado com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "plan_id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "rescue_value": 2000.00
                    }
                    
                ]
            }
        },
        400: {"description": "plan_id inválido. Deve ser um UUID válido."},
    }
}, status_code=status.HTTP_200_OK)
async def filter_rescue_by_plan(plan_id: str, session: AsyncSession = Depends(get_async_session)):
    """Filtra resgate pelo id do plano"""    
    return await get_rescue_by_plan_id(plan_id=plan_id)
    

@router.put('/update-rescue/{rescue_id}/', responses={
    200: {
        "description": "Resgate atualizado com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                    }
                    
                ]
            }
        },
        400: {"description": "plan_id inválido. Deve ser um UUID válido."},
        400: {"description": "Valor do resgate deve ser maior que 0."},
        404: {"description": "Resgate não encontrado"},
        404: {"description": "Plano associado não encontrado"},
        404: {"description": "Produto associado ao plano não encontrado"}
    }
}, status_code=status.HTTP_200_OK)
async def update_rescue(rescue_id: str, rescue: RescueUpdateSchema, session: AsyncSession = Depends(get_async_session)):
    """Atualiza resgate"""
    rescue_data_update = rescue.dict(exclude_unset=True)    
    return await update(rescue_id=rescue_id, **rescue_data_update)
    

@router.delete('/delete-rescue/{rescue_id}/', responses={
    200: {
        "description": "Resgate deletado com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                    }
                    
                ]
            }
        },
        400: {"description": "plan_id inválido. Deve ser um UUID válido."},
    }
}, status_code=status.HTTP_200_OK)
async def delete_rescue(rescue_id: str, session: AsyncSession = Depends(get_async_session)):
    """Deleta resgate"""
    return await remove(rescue_id=rescue_id)