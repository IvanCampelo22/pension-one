from api.v1.apps.products.schemas.schemas import ProductsSchema
from api.v1.apps.products.models.models import Products
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import async_session
from typing import List, Dict, Optional
from sqlalchemy.future import select
from loguru import logger
from fastapi import HTTPException
from uuid import UUID

"""
    Nesse aquivo contém todas as funções que serão utilizadas para manipular os dados dos produtos.
    Essas funções podem ser utilizadas em qualquer parte do código, no entanto, froram criadas para 
    complementar a lógica dos endpoints

    """


@async_session
async def insert(session: AsyncSession, args: Dict[str, any]) -> Dict[str, str]:
    """Função para salvar informações dos produtos
    
    Args:
        session (AsyncSession): Sessão assíncrona do SQLAlchemy para execução de consultas.
        args (Dict[str, any]): Dicionário com as informações do produto.

    Returns:
        Dict[str, str]: Mensagem de sucesso ou falha.

    """

    min_value_aporte_extra: float = 100.00
    min_value_aporte_initial: float = 1000.00
    min_age: int = 18
    max_age: int = 60 

    new_products = Products(**args)

    if not new_products.name:
        raise HTTPException(status_code=400, detail="Informe um nome para o produto.")
    
    if not new_products.susep:
        raise HTTPException(status_code=400, detail="Informe um código SUSEP para o produto.")

    if new_products.value_minimum_aporte_extra < min_value_aporte_extra:
        raise HTTPException(status_code=400, detail="Não é possível fazer um aporte extra  para este produto, porque o valor tem que ser acima de R$ 100,00.")
    
    if new_products.value_minimum_aporte_initial < min_value_aporte_initial:
        raise HTTPException(status_code=400, detail="Não é possível comprar este produto, porque o valor tem que ser acima de R$ 1.000")
    
    if new_products.entry_age < min_age:
        raise HTTPException(status_code=400, detail="Não é possível obter este produto, porque a idade mínima é de 18 anos.")
    
    if new_products.age_of_exit > max_age:
        raise HTTPException(status_code=400, detail="A idade máxima para começar a usufruir deste produto é de 60 anos.")
    
    if new_products.age_of_exit <= new_products.entry_age:
        raise HTTPException(status_code=400, detail="Insira uma idade de saída maior que a idade de entrada.")

    session.add(new_products)
    await session.commit()
    await session.refresh(new_products)
    logger.success("Novo produto registrado com sucesso")
    return {"id": str(new_products.id)}

@async_session
async def get_all(session: AsyncSession, products_schema) -> List[ProductsSchema]:
    """Função para listar todos os produtos
    
    Args:
        session (AsyncSession): Sessão assíncrona do SQLAlchemy para execução de consultas.
        produtcs_schema: Esquema do produto.

    Returns:
        List[ProductsSchema]: Lista de produtos.
    """
    try:

        query = select(Products)
        result = await session.execute(query)
        list: List[products_schema] = result.scalars().all()
        return list
    except Exception as e:
        logger.error(f"Erro ao listar produtos: {e}")
        raise HTTPException(status_code=500, detail="Erro ao listar produtos")

@async_session
async def get_one(session: AsyncSession, product_id: str) -> Dict:
    """Resgata um produto pelo identificador
    Args:
        session (AsyncSession): Sessão assíncrona do SQLAlchemy para execução de consultas.
        product_id (int): Identificador do produto a ser resgatado.
    
    Returns:
        Dict: Dicionário com mensagem de sucesso ou falha.
    """
    try:
        UUID(str(product_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="product_id inválido. Deve ser um UUID válido.")

    obj = await session.execute(select(Products).where(Products.id == product_id))
    obj_product = obj.scalar_one()
    return obj_product

@async_session
async def get_products_by_name(session: AsyncSession, product_name: str) -> Dict:
    """Resgata um produto pelo nome
    Args:
        session (AsyncSession): Sessão assíncrona do SQLAlchemy para execução de consultas.
        product_name (str): Nome do produto a ser resgatado.

    Returns:
        Dict: Dicionário com mensagem de sucesso ou falha.

    """
    if not isinstance(product_name, str):
        raise HTTPException(status_code=400, detail="Informe um nome válido para o produto.")

    if not product_name:
        raise HTTPException(status_code=400, detail="Informe um nome para o produto.")
    
    obj = await session.execute(select(Products).where(Products.name == product_name))
    obj_product = obj.scalars().all()
    return obj_product
    
@async_session
async def update(session: AsyncSession, product_id: str, **kwargs) -> Dict[str, Optional[str]]:
    """Atualiza informações de um produto.

    Args:
        session (AsyncSession): A sessão assíncrona do SQLAlchemy para execução de consultas.
        product_id (int): ID do produto a ser atualizado.
        **kwargs: Campos chave-valor que precisam ser atualizados.

    Returns:
        Dict[str, Optional[str]]: Mensagem sobre o sucesso ou falha da atualização.
    """
    min_value_aporte_extra: float = 100.00
    min_value_aporte_initial: float = 1000.00
    min_age: int = 18
    max_age: int = 60 

    try:
        UUID(str(product_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="product_id inválido. Deve ser um UUID válido.")
    
    value_minimum_aporte_extra = kwargs.get('value_minimum_aporte_extra')
    value_minimum_aporte_initial = kwargs.get('value_minimum_aporte_initial')
    entry_age = kwargs.get('entry_age')
    age_of_exit = kwargs.get('age_of_exit')

    if value_minimum_aporte_extra < min_value_aporte_extra:
        raise HTTPException(status_code=400, detail="O valor tem que ser acima de R$ 100,00.")
    
    if value_minimum_aporte_initial < min_value_aporte_initial:
        raise HTTPException(status_code=400, detail="O valor tem que ser acima de R$ 1.000")
    
    if entry_age < min_age:
        raise HTTPException(status_code=400, detail="A idade mínima é de 18 anos.")
    
    if age_of_exit > max_age:
        raise HTTPException(status_code=400, detail="A idade precisa ser acima de 60 anos.")
    
    if age_of_exit <= entry_age:
        raise HTTPException(status_code=400, detail="Insira uma idade de saída maior que a idade de entrada.")

    product_result = await session.execute(select(Products).where(Products.id == product_id))
    existing_product = product_result.scalars().first()

    if not existing_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    for key, value in kwargs.items():
        if value is not None and hasattr(existing_product, key):  
            setattr(existing_product, key, value)

    await session.commit()
    return {"message": f"Produto {existing_product.id}: atualizado com sucesso"}

@async_session
async def remove(session: AsyncSession, product_id: str) -> Dict[str, str]:
    """Função para deletar produtos pelo identificador
    
    Args:
        session (AsyncSession): Sessão assíncrona do SQLAlchemy para execução de consultas.
        client_id (int): Identificador do produto a ser deletado.

    Returns:
        Dict[str, str]: Mensagem de sucesso ou falha.
    """

    try:
        UUID(str(product_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="product_id inválido. Deve ser um UUID válido.")

    obj_id = await session.execute(select(Products).where(Products.id == product_id))
    obj_product = obj_id.scalar_one_or_none()
    
    if obj_product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    
    await session.delete(obj_product)
    await session.commit()
    return {"message": f"Produto {obj_product.id}: deletado com sucesso"}
    
   