from api.v1.apps.rescue.schemas.schemas import RescueSchema
from api.v1.apps.products.models.models import Products
from api.v1.apps.rescue.models.models import Rescue
from sqlalchemy.ext.asyncio import AsyncSession
from api.v1.apps.plan.models.models import Plan
from database.session import async_session
from typing import List, Dict, Optional
from sqlalchemy.future import select
from loguru import logger
from fastapi import HTTPException
from uuid import UUID

"""
    Nesse aquivo contém todas as funções que serão utilizadas para manipular os dados dos resgates.
    Essas funções podem ser utilizadas em qualquer parte do código, no entanto, froram criadas para 
    complementar a lógica dos endpoints

    """


@async_session
async def insert(session: AsyncSession, args: Dict[str, any]) -> Dict[str, str]:
    """Função para salvar informações dos resgates
    
    Args:
        session (AsyncSession): Sessão assíncrona do SQLAlchemy para execução de consultas.
        args (Dict[str, any]): Dicionário com as informações do resgate.

    Returns:
        Dict[str, str]: Mensagem de sucesso ou falha.
    """
    try:
        UUID(str(args.get('plan_id')))
    except ValueError:
        raise HTTPException(status_code=400, detail="plan_id inválido. Deve ser um UUID válido.")
    
    new_rescue = Rescue(**args)
    plan_query = select(Plan).where(Plan.id == new_rescue.plan_id)
    plan = await session.scalar(plan_query)

    if not plan:
        raise HTTPException(status_code=404, detail="Plano não encontrado.")

    product_query = select(Products).where(Products.id == plan.product_id)
    product = await session.scalar(product_query)

    if not product:
        raise HTTPException(status_code=404, detail="Produto associado ao plano não encontrado.")

    if new_rescue.rescue_value > plan.contribution:
        raise HTTPException(status_code=400, detail="Não há saldo suficiente para resgatar o valor informado.")

    if product.lack_initial_of_rescue < 60:
        raise HTTPException(status_code=400, detail="Carência inicial de resgate de 60 dias não foi cumprida.")

    session.add(new_rescue)
    await session.commit()
    logger.success("Novo resgate registrado com sucesso")
    return {"id": str(new_rescue.id)}

@async_session
async def get_all(session: AsyncSession, rescue_schema) -> List[RescueSchema]:
    """Função para listar todos os resgates realizados
    
    Args:
        session (AsyncSession): Sessão assíncrona do SQLAlchemy para execução de consultas.
        rescue_schema: Esquema do resgate.

    Returns:
        List[RescueSchema]: Lista de resgates.
    """
    try: 
        query = select(Rescue)
        result = await session.execute(query)
        list: List[rescue_schema] = result.scalars().all()
        return list
    except Exception as e:
        logger.error(f"Erro ao listar resgates: {e}")
        raise HTTPException(status_code=500, detail="Erro ao listar resgates")
    
@async_session
async def get_one(session: AsyncSession, rescue_id: str) -> Dict:
    """Resgata um resgate pelo identificador
    Args:
        session (AsyncSession): Sessão assíncrona do SQLAlchemy para execução de consultas.
        rescue_id (str): Identificador do resgate a ser identificado.
    
    Returns:
        Dict: Dicionário com mensagem de sucesso ou falha.
    """
    try:
        UUID(str(rescue_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="rescue_id inválido. Deve ser um UUID válido.")

    obj = await session.execute(select(Rescue).where(Rescue.id == rescue_id))
    obj_rescue = obj.scalar_one()
    return obj_rescue

@async_session
async def get_rescue_by_plan_id(session: AsyncSession, plan_id: str) -> Dict:
    """Filtra um resgate pelo id do plano
    Args:
        session (AsyncSession): Sessão assíncrona do SQLAlchemy para execução de consultas.
        plan_id (str): Id do plano a ser resgatado.

    Returns:
        Dict: Dicionário com mensagem de sucesso ou falha.

    """
    try:
        UUID(str(plan_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="plan_id inválido. Deve ser um UUID válido.")
    
    obj = await session.execute(select(Rescue).where(Rescue.plan_id == plan_id))
    obj_plan = obj.scalars().all()
    return obj_plan

@async_session
async def update(session: AsyncSession, rescue_id: str, **kwargs) -> Dict[str, Optional[str]]:
    """Atualiza informações de um resgate.

    Args:
        session (AsyncSession): A sessão assíncrona do SQLAlchemy para execução de consultas.
        rescue_id (str): ID do resgate a ser atualizado.
        **kwargs: Campos chave-valor que precisam ser atualizados.

    Returns:
        Dict[str, Optional[str]]: Mensagem sobre o sucesso ou falha da atualização.
    """
    try:
        UUID(str(rescue_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="rescue_id inválido. Deve ser um UUID válido.")

    rescue_result = await session.execute(select(Rescue).where(Rescue.id == rescue_id))
    existing_rescue = rescue_result.scalars().first()

    rescue_value = kwargs.get('rescue_value')

    if rescue_value <= 0:
        raise HTTPException(status_code=400, detail="Valor do resgate deve ser maior que 0.")

    if not existing_rescue:
        raise HTTPException(status_code=404, detail="Resgate não encontrado")

    plan_result = await session.execute(select(Plan).where(Plan.id == existing_rescue.plan_id))
    plan = plan_result.scalars().first()

    if not plan:
        raise HTTPException(status_code=404, detail="Plano associado não encontrado")

    product_result = await session.execute(select(Products).where(Products.id == plan.product_id))
    product = product_result.scalars().first()

    if not product:
        raise HTTPException(status_code=400, detail="Produto associado ao plano não encontrado")

    if product.lack_entre_resgates < 30:
        raise HTTPException(status_code=400, detail=f"Carência de 30 dias entre resgates não foi cumprida.")

    for key, value in kwargs.items():
        if value is not None and hasattr(existing_rescue, key):
            setattr(existing_rescue, key, value)

    await session.commit()
    return {"message": f"Resgate {existing_rescue.id}: atualizado com sucesso"}

@async_session
async def remove(session: AsyncSession, rescue_id: str) -> Dict[str, str]:
    """Função para deletar resgate pelo identificador
    
    Args:
        session (AsyncSession): Sessão assíncrona do SQLAlchemy para execução de consultas.
        rescue_id (str): Identificador do resgate a ser deletado.

    Returns:
        Dict[str, str]: Mensagem de sucesso ou falha.
    """

    try:
        UUID(str(rescue_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="rescue_id inválido. Deve ser um UUID válido.")

    obj_id = await session.execute(select(Rescue).where(Rescue.id == rescue_id))
    obj_rescue = obj_id.scalar_one_or_none()

    if obj_rescue is None:
        raise HTTPException(status_code=404, detail="Resgate não encontrado.")

    await session.delete(obj_rescue)
    await session.commit()
    return {"message": f"Resgate {obj_rescue.id}: deletado com sucesso"}
    
   