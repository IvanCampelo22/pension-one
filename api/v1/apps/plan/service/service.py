from api.v1.apps.plan.schemas.schemas import PlanSchema
from api.v1.apps.products.models.models import Products
from api.v1.apps.plan.models.models import Plan
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import async_session
from typing import List, Dict, Optional
from datetime import datetime, timezone
from sqlalchemy.future import select
from loguru import logger
from fastapi import HTTPException
from uuid import UUID

"""
    Nesse aquivo contém todas as funções que serão utilizadas para manipular os dados dos planos.
    Essas funções podem ser utilizadas em qualquer parte do código, no entanto, froram criadas para 
    complementar a lógica dos endpoints

"""


@async_session
async def insert(session: AsyncSession, args: Dict[str, any]) -> Dict[str, str]:
    """Função para salvar informações dos planos
    
    Args:
        session (AsyncSession): Sessão assíncrona do SQLAlchemy para execução de consultas.
        args (Dict[str, any]): Dicionário com as informações do cliente.

    Returns:
        Dict[str, str]: Mensagem de sucesso ou falha.

    """
    contribution = args.get('contribution')
    age_of_retirement = args.get('age_of_retirement')
    product_id = args.get('product_id')
    client_id = args.get('client_id')

    try:
        UUID(str(client_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="client_id inválido. Deve ser um UUID válido.")
    
    try:
        UUID(str(product_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="product_id inválido. Deve ser um UUID válido.")

    if contribution <= 0:
        raise HTTPException(status_code=400, detail="Informe um valor válido para o aporte inicial.")
    
    if age_of_retirement <= 0:
        raise HTTPException(status_code=400, detail="Informe uma idade de aposentadoria válida.")

    new_plan = Plan(**args)
    product_query = select(Products).where(Products.id == new_plan.product_id)
    product = await session.scalar(product_query)

    min_value_aporte_extra: float = 100.00
    min_value_aporte_initial: float = 1000.00
    min_age: int = 18
    max_age: int = 60 

    if product and product.expiration_of_sale <= datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Não é possível contratar este produto porque o prazo de venda expirou.")
    
    if product and product.value_minimum_aporte_extra < min_value_aporte_extra:
        raise HTTPException(status_code=400, detail="Não é possível contratar este produto porque o valor mínimo de aporte extra é menor que R$ 100,00.")

    if product and product.value_minimum_aporte_initial < min_value_aporte_initial:
        raise HTTPException(status_code=400, detail="Não é possível contratar este produto porque o valor mínimo de aporte inicial é menor que R$ 1.000")

    if product and product.entry_age < min_age:
        raise HTTPException(status_code=400, detail="Não é possível contratar este produto porque a idade mínima de entrada é menor que  18 anos.")
    
    if product and product.age_of_exit > max_age:
        raise HTTPException(status_code=400, detail="Não é possível contratar este produto porque a idade máxima de saída é maior que 60 anos.")

    session.add(new_plan)
    await session.commit()
    logger.success("Novo plan registrado com sucesso")
    return {"id": str(new_plan.id)}

@async_session
async def get_all(session: AsyncSession, plan_schema) -> List[PlanSchema]:
    """Função para listar todos os planos
    
    Args:
        session (AsyncSession): Sessão assíncrona do SQLAlchemy para execução de consultas.
        plan_schema: Esquema do plano.

    Returns:
        List[PlanSchema]: Lista de planos.
    """
    try:
        query = select(Plan)
        result = await session.execute(query)
        list: List[plan_schema] = result.scalars().all()
        return list
    except Exception as e:
        logger.error(f"Erro ao listar planos: {e}")
        raise HTTPException(status_code=500, detail="Erro ao listar planos")

@async_session
async def get_one(session: AsyncSession, plan_id: str) -> Dict:
    """Resgata um plano pelo identificador
    Args:
        session (AsyncSession): Sessão assíncrona do SQLAlchemy para execução de consultas.
        client_id (int): Identificador do plano a ser resgatado.
    
    Returns:
        Dict: Dicionário com mensagem de sucesso ou falha.
    """
    try:
        UUID(str(plan_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="plan_id inválido. Deve ser um UUID válido.")

    obj = await session.execute(select(Plan).where(Plan.id == plan_id))
    obj_client = obj.scalar_one()
    return obj_client

@async_session
async def get_plan_by_client_id(session: AsyncSession, client_id: str) -> Dict:
    """Resgata um plano pelo id do cliente
    Args:
        session (AsyncSession): Sessão assíncrona do SQLAlchemy para execução de consultas.
        client_name (str): Id do cliente a ser resgatado.

    Returns:
        Dict: Dicionário com mensagem de sucesso ou falha.

    """

    try:
        UUID(str(client_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="client_id inválido. Deve ser um UUID válido.")
    
    obj = await session.execute(select(Plan).where(Plan.client_id == client_id))
    obj_plan = obj.scalars().all()
    return obj_plan
    
@async_session
async def update(session: AsyncSession, plan_id: int, **kwargs) -> Dict[str, Optional[str]]:
    """Atualiza informações de um plano.

    Args:
        session (AsyncSession): A sessão assíncrona do SQLAlchemy para execução de consultas.
        plan_id (int): ID do plano a ser atualizado.
        **kwargs: Campos chave-valor que precisam ser atualizados.

    Returns:
        Dict[str, Optional[str]]: Mensagem sobre o sucesso ou falha da atualização.
        
    """
    contribution = kwargs.get('contribution')
    age_of_retirement = kwargs.get('age_of_retirement')
    product_id = kwargs.get('product_id')
    client_id = kwargs.get('client_id')
    try:
        UUID(str(plan_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="plan_id inválido. Deve ser um UUID válido.")

    try:
        UUID(str(client_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="client_id inválido. Deve ser um UUID válido.")
    
    try:
        UUID(str(product_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="product_id inválido. Deve ser um UUID válido.")

    product_query = select(Products).where(Products.id == product_id)
    product = await session.scalar(product_query)

    if contribution <= 0:
        raise HTTPException(status_code=400, detail="Informe um valor válido para o aporte inicial.")
    
    if age_of_retirement <= 0:
        raise HTTPException(status_code=400, detail="Informe uma idade de aposentadoria válida.")
    
    min_value_aporte_extra: float = 100.00
    min_value_aporte_initial: float = 1000.00
    min_age: int = 18
    max_age: int = 60 

    if product and product.expiration_of_sale <= datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Informe um prazo de venda válido.")
    
    if product and product.value_minimum_aporte_extra < min_value_aporte_extra:
        raise HTTPException(status_code=400, detail="O valor mínimo de aporte extra é menor que R$ 100,00.")

    if product and product.value_minimum_aporte_initial < min_value_aporte_initial:
        raise HTTPException(status_code=400, detail="O valor mínimo de aporte inicial é menor que R$ 1.000")

    if product and product.entry_age < min_age:
        raise HTTPException(status_code=400, detail="A idade mínima de entrada é menor que  18 anos.")
    
    if product and product.age_of_exit > max_age:
        raise HTTPException(status_code=400, detail="A idade máxima de saída é maior que 60 anos.")

    plan_result = await session.execute(select(Plan).where(Plan.id == plan_id))
    existing_plan = plan_result.scalars().first()

    if not existing_plan:
        raise HTTPException(status_code=404, detail="Plano não encontrado")

    for key, value in kwargs.items():
        if value is not None and hasattr(existing_plan, key):  
            setattr(existing_plan, key, value)

    await session.commit()
    return {"message": f"Produto {existing_plan.id}: atualizado com sucesso"}
   
@async_session
async def remove(session: AsyncSession, plan_id: str) -> Dict[str, str]:
    """Função para deletar planos pelo identificador
    
    Args:
        session (AsyncSession): Sessão assíncrona do SQLAlchemy para execução de consultas.
        plan_id (int): Identificador do plano a ser deletado.

    Returns:
        Dict[str, str]: Mensagem de sucesso ou falha.
    """
    try:
        UUID(str(plan_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="plan_id inválido. Deve ser um UUID válido.")
    
    obj_id = await session.execute(select(Plan).where(Plan.id == plan_id))
    obj_plan = obj_id.scalar_one_or_none()

    if obj_plan is None:
        raise HTTPException(status_code=404, detail="Plano não encontrado.")

    await session.delete(obj_plan)
    await session.commit()
    return {"message": f"Plan {obj_plan.id}: deletado com sucesso"}
    
   