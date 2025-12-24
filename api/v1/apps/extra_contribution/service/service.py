from api.v1.apps.extra_contribution.schemas.schemas import ExtraContributionSchema
from api.v1.apps.extra_contribution.models.models import ExtraContribution
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import async_session
from typing import List, Dict, Optional
from sqlalchemy.future import select
from loguru import logger
from fastapi import HTTPException
from uuid import UUID


"""
    Nesse aquivo contém todas as funções que serão utilizadas para manipular os dados dos aportes extras.
    Essas funções podem ser utilizadas em qualquer parte do código, no entanto, froram criadas para 
    complementar a lógica dos endpoints

"""


@async_session
async def insert(session: AsyncSession, args: Dict[str, any]) -> Dict[str, str]:
    """Função para salvar informações dos aportes extras
    
    Args:
        session (AsyncSession): Sessão assíncrona do SQLAlchemy para execução de consultas.
        args (Dict[str, any]): Dicionário com as informações do aporte extra.

    Returns:
        Dict[str, str]: Mensagem de sucesso ou falha.

    """

    min_contribution_value: float = 100.00
    plan_id = args.get('plan_id')
    client_id = args.get('client_id')

    try:
        UUID(str(client_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="client_id inválido. Deve ser um UUID válido.")
    
    try:
        UUID(str(plan_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="plan_id inválido. Deve ser um UUID válido.")

    new_extra_contribution = ExtraContribution(**args)
    if new_extra_contribution.contribution_value < min_contribution_value:
        raise HTTPException(status_code=400, detail="Não é possível realizar aporte extra com valor menor que R$ 100,00.")
    
    session.add(new_extra_contribution)
    await session.commit()
    logger.success("Novo aporte registrado com sucesso")
    return {"id": str(new_extra_contribution.id)}


@async_session
async def get_all(session: AsyncSession, extra_contribution_schema) -> List[ExtraContributionSchema]:
    """Função para listar todos os aportes extras
    
    Args:
        session (AsyncSession): Sessão assíncrona do SQLAlchemy para execução de consultas.
        extra_contribution_schema: Esquema do aporte

    Returns:
        List[ExtraContributionSchema]: Lista de aportes extras.
    """
    try:
        query = select(ExtraContribution)
        result = await session.execute(query)
        list: List[extra_contribution_schema] = result.scalars().all()
        return list
    except Exception as e:
        logger.error(f"Erro ao listar aportes: {e}")
        raise HTTPException(status_code=500, detail="Erro ao listar aportes extra")
    
@async_session
async def get_one(session: AsyncSession, extra_contribution_id: str) -> Dict:
    """Resgata um aporte pelo identificador
    Args:
        session (AsyncSession): Sessão assíncrona do SQLAlchemy para execução de consultas.
        extra_contribution_id (str): Identificador do aporte a ser resgatado.
    
    Returns:
        Dict: Dicionário com mensagem de sucesso ou falha.
    """
    try:
        UUID(str(extra_contribution_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="extra_contribution_id inválido. Deve ser um UUID válido.")
    
    obj = await session.execute(select(ExtraContribution).where(ExtraContribution.id == extra_contribution_id))
    obj_extra_contribution = obj.scalar_one()
    return obj_extra_contribution

@async_session
async def get_extra_contribution_by_client_id(session: AsyncSession, client_id: str) -> Dict:
    """Resgata um cliente pelo nome
    Args:
        session (AsyncSession): Sessão assíncrona do SQLAlchemy para execução de consultas.
        client_id (str): Id do cliente a ser resgatado.

    Returns:
        Dict: Dicionário com mensagem de sucesso ou falha.

    """
    try:
        UUID(str(client_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="client_id inválido. Deve ser um UUID válido.")

    obj = await session.execute(select(ExtraContribution).where(ExtraContribution.client_id == client_id))
    obj_extra_contrbution = obj.scalars().all()
    return obj_extra_contrbution
    
@async_session
async def update(session: AsyncSession, extra_contribution_id: str, **kwargs) -> Dict[str, Optional[str]]:
    """Atualiza informações de um aporte.

    Args:
        session (AsyncSession): A sessão assíncrona do SQLAlchemy para execução de consultas.
        extra_contribution_id (int): ID do aporte a ser atualizado.
        **kwargs: Campos chave-valor que precisam ser atualizados.

    Returns:
        Dict[str, Optional[str]]: Mensagem sobre o sucesso ou falha da atualização.
    """
    plan_id = kwargs.get('plan_id')
    client_id = kwargs.get('client_id')

    try:
        UUID(str(client_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="client_id inválido. Deve ser um UUID válido.")
    
    try:
        UUID(str(plan_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="plan_id inválido. Deve ser um UUID válido.")

    try:
        UUID(str(extra_contribution_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="extra_contribution_id inválido. Deve ser um UUID válido.")

    extra_contribution_result = await session.execute(select(ExtraContribution).where(ExtraContribution.id == extra_contribution_id))
    existing_extra_contribution = extra_contribution_result.scalars().first()

    if not existing_extra_contribution:
        raise HTTPException(status_code=400, detail="Aporte extra não encontrado")
        
    min_contribution_value: float = 100.00
    contribution_value = kwargs.get('contribution_value') 
    if contribution_value < min_contribution_value:
        raise HTTPException(status_code=400, detail="Não é possível realizar aporte extra com valor menor que R$ 100,00.")

    for key, value in kwargs.items():
        if value is not None and hasattr(existing_extra_contribution, key):
            setattr(existing_extra_contribution, key, value)

    await session.commit()
    return {"message": f"Aporte extra {existing_extra_contribution.id}: atualizado com sucesso"}
   
@async_session
async def remove(session: AsyncSession, extra_contribution_id: str) -> Dict[str, str]:
    """Função para deletar aportes pelo identificador
    
    Args:
        session (AsyncSession): Sessão assíncrona do SQLAlchemy para execução de consultas.
        extra_contribution_str (str): Identificador do aporte a ser deletado.

    Returns:
        Dict[str, str]: Mensagem de sucesso ou falha.
    """

    try:
        UUID(str(extra_contribution_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="extra_contribution_id inválido. Deve ser um UUID válido.")

    obj_id = await session.execute(select(ExtraContribution).where(ExtraContribution.id == extra_contribution_id))
    obj_extra_contribution = obj_id.scalar_one_or_none()

    if obj_extra_contribution is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    
    await session.delete(obj_extra_contribution)
    await session.commit()
    return {"message": f"Aporte {obj_extra_contribution.id}: deletado com sucesso"}
    
   