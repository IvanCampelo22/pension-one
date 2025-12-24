from api.v1.apps.client.schemas.schemas import ClientSchema, GenderTypeEnum
from api.v1.apps.client.models.models import Client
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import async_session
from typing import List, Dict, Optional
from sqlalchemy.future import select
from loguru import logger
from fastapi import HTTPException
from uuid import UUID



"""
    Nesse aquivo contém todas as funções que serão utilizadas para manipular os dados dos clientes.
    Essas funções podem ser utilizadas em qualquer parte do código, no entanto, froram criadas para 
    complementar a lógica dos endpoints

"""


@async_session
async def insert(session: AsyncSession, args: Dict[str, any]) -> Dict[str, str]:
    """Função para salvar informações dos clientes
    
    Args:
        session (AsyncSession): Sessão assíncrona do SQLAlchemy para execução de consultas.
        args (Dict[str, any]): Dicionário com as informações do cliente.

    Returns:
        Dict[str, str]: Mensagem de sucesso ou falha.

    """
    cpf = args.get('cpf')
    email = args.get('email')
    monthly_income = args.get('monthly_income')
    name = args.get('name')
    gender = args.get('gender')

    if not cpf:
        raise HTTPException(status_code=400, detail="Informe um valor válido para o cpf")
    
    if not email:
        raise HTTPException(status_code=400, detail="Informe um valor válido para o email")
    
    if not monthly_income or monthly_income <= 0:
        raise HTTPException(status_code=400, detail="Informe um valor válido para a renda mensal.")
    
    if not name:
        raise HTTPException(status_code=400, detail="Informe um valor válido para o nome.")
    
    if gender not in GenderTypeEnum.__members__.values():
        raise HTTPException(status_code=400, detail="Informe um valor válido para o gênero.")

    new_client = Client(**args)
    
    if new_client.monthly_income <= 0:
        raise HTTPException(status_code=400, detail="Informe um valor válido para a renda mensal.")
    
    session.add(new_client)
    await session.commit()
    await session.refresh(new_client)
    logger.success("Novo cliente registrado com sucesso")
    return {"id": str(new_client.id)}

@async_session
async def get_all(session: AsyncSession, client_schema) -> List[ClientSchema]:
    """Função para listar todos os clientes
    
    Args:
        session (AsyncSession): Sessão assíncrona do SQLAlchemy para execução de consultas.
        client_schema: Esquema do cliente.

    Returns:
        List[ClientSchema]: Lista de clientes.
    """
    try:
        query = select(Client)
        result = await session.execute(query)
        list: List[client_schema] = result.scalars().all()
        return list
    except Exception as e:
        logger.error(f"Erro ao listar aportes: {e}")
        raise HTTPException(status_code=500, detail="Erro ao listar clientes")
    
@async_session
async def get_one(session: AsyncSession, client_id: str) -> Dict:
    """Resgata um cliente pelo identificador
    Args:
        session (AsyncSession): Sessão assíncrona do SQLAlchemy para execução de consultas.
        client_id (int): Identificador do cliente a ser resgatado.
    
    Returns:
        Dict: Dicionário com mensagem de sucesso ou falha.
    """
    try:
        UUID(str(client_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="client_id inválido. Deve ser um UUID válido.")

    obj = await session.execute(select(Client).where(Client.id == client_id))
    obj_client = obj.scalar_one()
    return obj_client

@async_session
async def get_client_by_email(session: AsyncSession, client_email: str) -> Dict:
    """Resgata um cliente pelo email
    Args:
        session (AsyncSession): Sessão assíncrona do SQLAlchemy para execução de consultas.
        client_email (str): Email do cliente a ser resgatado.

    Returns:
        Dict: Dicionário com mensagem de sucesso ou falha.

    """
    
    if not client_email:
        raise HTTPException(status_code=400, detail="Informe um email válido para o cliente.")

    obj = await session.execute(select(Client).where(Client.email == client_email))
    obj_client = obj.scalars().all()
    return obj_client
    
@async_session
async def update(session: AsyncSession, client_id: str, **kwargs) -> Dict[str, Optional[str]]:
    """Atualiza informações de um cliente.

    Args:
        session (AsyncSession): A sessão assíncrona do SQLAlchemy para execução de consultas.
        client_id (str): ID do cliente a ser atualizado.
        **kwargs: Campos chave-valor que precisam ser atualizados.

    Returns:
        Dict[str, Optional[str]]: Mensagem sobre o sucesso ou falha da atualização.
    """
    monthly_income = kwargs.get('monthly_income')
    gender = kwargs.get('gender')

    try:
        UUID(str(client_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="client_id inválido. Deve ser um UUID válido.")

    client_result = await session.execute(select(Client).where(Client.id == client_id))
    existing_client = client_result.scalars().first()

    if gender not in GenderTypeEnum.__members__.values():
        raise HTTPException(status_code=400, detail="Informe um valor válido para o gênero.")

    if monthly_income <= 0:
        raise HTTPException(status_code=400, detail="Informe um valor válido para a renda mensal.")

    if not existing_client:
        raise HTTPException(status_code=400, detail="Cliente não encontrado")

    for key, value in kwargs.items():
        if value is not None and hasattr(existing_client, key):
            setattr(existing_client, key, value)

    await session.commit()
    return {"message": f"Cliente {existing_client.id}: atualizado com sucesso"}
   

@async_session
async def remove(session: AsyncSession, client_id: str) -> Dict[str, str]:
    """Função para deletar clientes pelo identificador
    
    Args:
        session (AsyncSession): Sessão assíncrona do SQLAlchemy para execução de consultas.
        client_id (str): Identificador do cliente a ser deletado.

    Returns:
        Dict[str, str]: Mensagem de sucesso ou falha.
    """
    try:
        UUID(str(client_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="client_id inválido. Deve ser um UUID válido.")

    obj_id = await session.execute(select(Client).where(Client.id == client_id))
    obj_client = obj_id.scalar_one_or_none()

    if obj_client is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    await session.delete(obj_client)
    await session.commit()
    return {"message": f"Cliente {obj_client.id}: deletado com sucesso"}
    
   