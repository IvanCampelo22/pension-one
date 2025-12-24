from api.v1.apps.extra_contribution.service.service import insert, get_all, get_one, update, remove, get_extra_contribution_by_client_id
from fastapi import APIRouter, status, Depends
from api.v1.apps.extra_contribution.schemas.schemas import ExtraContributionSchema, ExtraContributionUpdateSchema
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_async_session

router = APIRouter()

@router.post('/create-extra-contribution/', responses={
    201: {
        "description": "Aporte extra realizado com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "id: 9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a"
                    }
                ]
            }
        },
        400: {"description": "Não é possível realizar aporte extra com valor menor que R$ 100,00."},
        400: {"description": "plan_id inválido. Deve ser um UUID válido."},
        400: {"description": "client_id inválido. Deve ser um UUID válido."}
}}, status_code=status.HTTP_201_CREATED)
async def create_extra_contribution(extra_contribution: ExtraContributionSchema, session: AsyncSession = Depends(get_async_session)):
    """Realiza aportes extras para clientes que já estão cadastrados e segue o plano de benefícios"""
    extra_contribution_data_create = extra_contribution.dict()
    return await insert(args=extra_contribution_data_create)
    

@router.get('/get-extra_contribution/', responses={
    201: {
        "description": "Listagem de aportes extras realizada com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "client_id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "plan_id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "contribution_value": 100.00

                    }
                ]
            }
        },
        500: {"description": "Erro ao listar aportes extra"},
}}, status_code=status.HTTP_200_OK)
async def get_extra_contribution(session: AsyncSession = Depends(get_async_session)):
    """Faz a listagem de todos os aportes extras realizados"""   
    return await get_all(ExtraContributionSchema)
    

@router.get('/get-one-extra-contribution/{extra_contribution_id}/', responses={
    201: {
        "description": "Filtragem de aportes extras realizada com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "client_id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "plan_id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "contribution_value": 100.00

                    }
                ]
            }
        },
        400: {"description": "extra_contribution_id inválido. Deve ser um UUID válido."},
}}, status_code=status.HTTP_200_OK)
async def get_one_extra_contribution(extra_contribution_id: str, session: AsyncSession = Depends(get_async_session)):
    """Filtra aportes extras realizados pelo id"""
    return await get_one(extra_contribution_id=extra_contribution_id)


@router.get('/filter-extra-contribution-by-client/{client_id}/', responses={
    201: {
        "description": "Filtragem de aportes extras pelo id do client realizada com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "client_id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "plan_id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "contribution_value": 100.00

                    }
                ]
            }
        },
        400: {"description": "client_id inválido. Deve ser um UUID válido."},
}}, status_code=status.HTTP_200_OK)
async def filter_extra_contribution_by_client(client_id: str, session: AsyncSession = Depends(get_async_session)):
    """Filtra aportes extras realizados pelo id do cliente"""
    return await get_extra_contribution_by_client_id(client_id=client_id)
    

@router.put('/update-extra-contribution/{extra_contribution_id}/', responses={
    201: {
        "description": "Atualização de aportes extras realizada com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "client_id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "plan_id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "contribution_value": 100.00

                    }
                ]
            }
        },
        400: {"description": "plan_id inválido. Deve ser um UUID válido."},
        400: {"description": "client_id inválido. Deve ser um UUID válido."},
        400: {"description": "extra_contribution_id inválido. Deve ser um UUID válido."},
        400: {"description": "Aporte extra não encontrado"},
        400: {"description": "Não é possível realizar aporte extra com valor menor que R$ 100,00."},
}}, status_code=status.HTTP_200_OK)
async def update_extra_contribution(extra_contribution_id: str, extra_contribution: ExtraContributionUpdateSchema, session: AsyncSession = Depends(get_async_session)):
    """Atualiza aportes extras realizados"""
    extra_contribution_data_update = extra_contribution.dict()
    return await update(extra_contribution_id=extra_contribution_id, **extra_contribution_data_update)
    

@router.delete('/delete-extra-contribution/{extra_contribution_id}/', responses={
    201: {
        "description": "Aporte deletado com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "client_id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "plan_id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "contribution_value": 100.00

                    }
                ]
            }
        },
        400: {"description": "extra_contribution_id inválido. Deve ser um UUID válido."},
}}, status_code=status.HTTP_200_OK)
async def delete_extra_contribution(extra_contribution_id: str, session: AsyncSession = Depends(get_async_session)):
    """Remove aportes extras realizados""" 
    return await remove(extra_contribution_id=extra_contribution_id)
    
    