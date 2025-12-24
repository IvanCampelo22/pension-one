from api.v1.apps.client.service.service import insert, get_all, get_one, update, remove, get_client_by_email
from fastapi import APIRouter, status, Depends
from api.v1.apps.client.schemas.schemas import ClientSchema, ClientUpdateSchema
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_async_session

router = APIRouter()

@router.post('/create-client/', responses={
    201: {
        "description": "Cliente cadastrado com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "id: 9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a"
                    }
                ]
            }
        },
        400: {"description": "Informe um valor válido para o cpf"},
        400: {"description": "Informe um valor válido para o email"},
        400: {"description": "Informe um valor válido para a renda mensal."},
        400: {"description": "Informe um valor válido para a idade."},
        400: {"description": "Informe um valor válido para o nome."},
        400: {"description": "Informe um valor válido para o gênero."},
        400: {"description": "Informe um valor válido para a renda mensal."}
}}, status_code=status.HTTP_201_CREATED)
async def create_client(client: ClientSchema, session: AsyncSession = Depends(get_async_session)):
    """Cadastro de clientes que vão utilizar os benefícios da empresa"""
    client_data_create = client.dict() 
    return await insert(args=client_data_create)
    

@router.get('/get-client/', responses={
    200: {
        "description": "Listagem de clientes realizada com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "cpf": "12345678901",
                        "name": "Cliente Teste",
                        "email": "cliente@teste.com",
                        "date_of_birth": "01-01-1991",
                        "gender": "Masculino",
                        "monthly_income": 5000.00
                    }
                ]
            }
        },
        400: {"description": "Erro ao listar clientes"},
}}, status_code=status.HTTP_200_OK)
async def get_client(session: AsyncSession = Depends(get_async_session)):
    """Faz a listagem de todos os clientes cadastrados"""
    return await get_all(ClientSchema)
    

@router.get('/get-one-client/{client_id}/', responses={
    200: {
        "description": "Filtragem de clientes por id realizada com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "cpf": "12345678901",
                        "name": "Cliente Teste",
                        "email": "cliente@teste.com",
                        "date_of_birth": "01-01-1991",
                        "gender": "Masculino",
                        "monthly_income": 5000.00
                    }
                ]
            }
        },
        500: {"description": "client_id inválido. Deve ser um UUID válido."},
}}, status_code=status.HTTP_200_OK)
async def get_one_client(client_id: str, session: AsyncSession = Depends(get_async_session)):
    """Filtra o cliente por id e retorna todas as suas informações para consultas"""  
    return await get_one(client_id=client_id)
    

@router.get('/filter-client-by-email/{client_email}/', responses={
    200: {
        "description": "Filtragem de clientes por email realizada com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                        "cpf": "12345678901",
                        "name": "Cliente Teste",
                        "email": "cliente@teste.com",
                        "date_of_birth": "01-01-1991",
                        "gender": "Masculino",
                        "monthly_income": 5000.00
                    }
                ]
            }
        },
        400: {"description": "Informe um email válido para o cliente."},
}}, status_code=status.HTTP_200_OK)
async def filter_client_by_email(client_email: str, session: AsyncSession = Depends(get_async_session)):
    """Filtra cliente por email e retorna todas as suas informações para consultas"""
    return await get_client_by_email(client_email=client_email)
    
   
@router.put('/update-client/{client_id}/', responses={
    200: {
        "description": "Atualização de clientes realizada com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a"   
                    }
                ]
            }
        },
        400: {"description": "Informe um valor válido para a idade."},
        404: {"description": "Cliente não encontrado"},
}}, status_code=status.HTTP_200_OK)
async def update_client(client_id: str, client: ClientUpdateSchema, session: AsyncSession = Depends(get_async_session)):
    """Atualiza informações do cliente cadastrado"""
    client_data_update = client.dict(exclude_unset=True) 
    return await update(client_id=client_id, **client_data_update)
    

@router.delete('/delete-client/{client_id}/', responses={
    200: {
        "description": "Cliente deletado com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "id": "9c3a5b52-8f0d-4b58-9bfb-987f3a1c457a",
                    }
                ]
            }
        },
        400: {"description": "cliente inválido. Deve ser um UUID válido."},
}}, status_code=status.HTTP_200_OK)
async def delete_client(client_id: str, session: AsyncSession = Depends(get_async_session)):
    """Deleta clientes cadastrados"""
    return await remove(client_id=client_id)
    
    