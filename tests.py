import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from main import app  
from database.session import Base  
from httpx import AsyncClient
from fastapi import HTTPException
from datetime import date
from unittest.mock import AsyncMock
from api.v1.apps.client.models.models import Client
from api.v1.apps.client.service.service import insert as insert_client
from api.v1.apps.products.service.service import insert as insert_product
from api.v1.apps.plan.service.service import insert as insert_plan
from api.v1.apps.extra_contribution.service.service import insert as insert_extra_contribution
from api.v1.apps.rescue.service.service import insert as insert_rescue

from datetime import datetime
import asyncio
import uuid

DATABASE_URL = "postgresql+asyncpg://postgres:12345678@db/postgres"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture()
async def async_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()

@pytest.fixture(scope="function", autouse=True)
async def transactional_session(async_session):
    async with async_session.begin():
        yield async_session
        await async_session.rollback()

# Tests clients
@pytest.mark.asyncio
async def test_create_client_success():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8080") as client:
        new_client_data = {
            "cpf": "12345678901",
            "name": "Cliente Teste",
            "email": "cliente@teste.com",
            "date_of_birth": str(date(1990, 1, 1)),
            "gender": "Masculino",
            "monthly_income": 5000.0
        }

        response = await client.post("/clients/create-client/", json=new_client_data)

        assert response.status_code == 201
        response_data = response.json()
        assert "id" in response_data
        assert isinstance(response_data["id"], str)


@pytest.mark.asyncio
async def test_insert_invalid_monthly_income():
    client_data = {
        "cpf": "12345678901",
        "name": "Cliente Inválido",
        "email": "cliente@invalido.com",
        "date_of_birth": "1990-05-15",
        "gender": "Feminino",
        "monthly_income": 0.0
    }

    with pytest.raises(HTTPException) as exc_info:
        result = await insert_client(client_data)
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Informe um valor válido para a renda mensal."
    


#Tests products
@pytest.mark.asyncio
async def test_create_product_success():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8080") as client:
        new_product_data = {
            "name": "Produto Teste",
            "susep": "1234567890",
            "expiration_of_sale": "2025-11-02T19:30:24.117000+00:00",  
            "value_minimum_aporte_initial": 1000.00,
            "value_minimum_aporte_extra": 500.00,
            "entry_age": 18,
            "age_of_exit": 45,
            "lack_initial_of_rescue": 30,
            "lack_entre_resgates": 15 
        }

        response = await client.post("/products/create-product/", json=new_product_data)

        assert response.status_code == 201
        response_data = response.json()
        assert "id" in response_data
        assert isinstance(response_data["id"], str)


@pytest.mark.asyncio
async def test_insert_invalid_contribution_extra():
    new_product_data = {
            "name": "Produto Teste",
            "susep": "1234567890",
            "expiration_of_sale": "2025-11-02T19:30:24.117000+00:00",  
            "value_minimum_aporte_initial": 1000.00,
            "value_minimum_aporte_extra": 50.00,
            "entry_age": 18,
            "age_of_exit": 45,
            "lack_initial_of_rescue": 30,
            "lack_entre_resgates": 15 
        }

    with pytest.raises(HTTPException) as exc_info:
        result = await insert_product(new_product_data)
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Não é possível fazer um aporte extra  para este produto, porque o valor tem que ser acima de R$ 100,00."


@pytest.mark.asyncio
async def test_insert_invalid_initial_contribution():
    new_product_data = {
            "name": "Produto Teste",
            "susep": "1234567890",
            "expiration_of_sale": "2025-11-02T19:30:24.117000+00:00",  
            "value_minimum_aporte_initial": 100.00,
            "value_minimum_aporte_extra": 100.00,
            "entry_age": 18,
            "age_of_exit": 45,
            "lack_initial_of_rescue": 30,
            "lack_entre_resgates": 15 
        }

    with pytest.raises(HTTPException) as exc_info:
        result = await insert_product(new_product_data)
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Não é possível comprar este produto, porque o valor tem que ser acima de R$ 1.000"


@pytest.mark.asyncio
async def test_insert_invalid_entry_age():
    new_product_data = {
            "name": "Produto Teste",
            "susep": "1234567890",
            "expiration_of_sale": "2025-11-02T19:30:24.117000+00:00",  
            "value_minimum_aporte_initial": 1000.00,
            "value_minimum_aporte_extra": 100.00,
            "entry_age": 17,
            "age_of_exit": 45,
            "lack_initial_of_rescue": 30,
            "lack_entre_resgates": 15 
        }

    with pytest.raises(HTTPException) as exc_info:
        result = await insert_product(new_product_data)
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Não é possível obter este produto, porque a idade mínima é de 18 anos."

@pytest.mark.asyncio
async def test_insert_invalid_age_of_exit():
    new_product_data = {
            "name": "Produto Teste",
            "susep": "1234567890",
            "expiration_of_sale": "2025-11-02T19:30:24.117000+00:00",  
            "value_minimum_aporte_initial": 1000.00,
            "value_minimum_aporte_extra": 100.00,
            "entry_age": 18,
            "age_of_exit": 65,
            "lack_initial_of_rescue": 30,
            "lack_entre_resgates": 15 
        }

    with pytest.raises(HTTPException) as exc_info:
        result = await insert_product(new_product_data)
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "A idade máxima para começar a usufruir deste produto é de 60 anos."


#Teste plans
@pytest.mark.asyncio
async def test_create_plan_success():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8080") as client:

        # Criação do cliente
        client_data = {
            "id": str(uuid.uuid4()),
            "cpf": "12345678901",
            "name": "Cliente Teste",
            "email": "cliente@teste.com",
            "date_of_birth": datetime.strptime("1990-05-15", "%Y-%m-%d").date(),
            "gender": "Feminino",
            "monthly_income": 6000.0
        }
        result_client = await insert_client(args=client_data)
        client_id = result_client.get("id")

        new_product_data = {
            "id": str(uuid.uuid4()),
            "name": "Produto Teste",
            "susep": "1234567890",
            "expiration_of_sale": datetime.fromisoformat("2025-11-02T19:30:24.117000+00:00"),
            "value_minimum_aporte_initial": 1000.00,
            "value_minimum_aporte_extra": 100.00,
            "entry_age": 18,
            "age_of_exit": 45,
            "lack_initial_of_rescue": 30,
            "lack_entre_resgates": 15
        }
        result_product = await insert_product(args=new_product_data)
        product_id = result_product.get("id")

        assert client_id is not None, "Client ID é None"
        assert product_id is not None, "Product ID é None"

        new_plan_data = {
            "client_id": client_id,
            "product_id": product_id,
            "contribution": 1500.00,
            "date_of_contract": "2024-11-02T20:46:03.566Z",
            "age_of_retirement": 65
        }

        response = await client.post("/plans/create-plan/", json=new_plan_data)

        assert response.status_code == 201
        response_data = response.json()
        assert "id" in response_data
        assert isinstance(response_data["id"], str)


@pytest.mark.asyncio
async def test_plan_invalid_expiration_of_sale():
    client_data = {
        "id": str(uuid.uuid4()),
        "cpf": "12345678901",
        "name": "Cliente Teste",
        "email": "cliente@teste.com",
        "date_of_birth": datetime.strptime("1990-05-15", "%Y-%m-%d").date(),
        "gender": "Feminino",
        "monthly_income": 6000.0
    }
    result_client = await insert_client(args=client_data)
    client_id = result_client.get("id")

    new_product_data = {
        "id": str(uuid.uuid4()),
        "name": "Produto Teste",
        "susep": "1234567890",
        "expiration_of_sale": datetime.fromisoformat("2024-11-02T19:30:24.117000+00:00"),
        "value_minimum_aporte_initial": 1000.00,
        "value_minimum_aporte_extra": 100.00,
        "entry_age": 18,
        "age_of_exit": 45,
        "lack_initial_of_rescue": 30,
        "lack_entre_resgates": 15
    }
    result_product = await insert_product(args=new_product_data)
    product_id = result_product.get("id")

    new_plan_data = {
        "client_id": client_id,
        "product_id": product_id,
        "contribution": 1500.00,
        "date_of_contract": datetime.fromisoformat("2024-11-02T20:46:03.566+00:00"),
        "age_of_retirement": 65
    }

    with pytest.raises(HTTPException) as exc_info:
        result = await insert_plan(new_plan_data)
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Não é possível contratar este produto porque o prazo de venda expirou."


@pytest.mark.asyncio
async def test_create_extra_contribution_success():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8080") as client:

        # Criação do cliente
        client_data = {
            "id": str(uuid.uuid4()),
            "cpf": "12345678901",
            "name": "Cliente Teste",
            "email": "cliente@teste.com",
            "date_of_birth": datetime.strptime("1990-05-15", "%Y-%m-%d").date(),
            "gender": "Feminino",
            "monthly_income": 6000.0
        }
        result_client = await insert_client(args=client_data)
        client_id = result_client.get("id")

        new_product_data = {
            "id": str(uuid.uuid4()),
            "name": "Produto Teste",
            "susep": "1234567890",
            "expiration_of_sale": datetime.fromisoformat("2025-11-02T19:30:24.117000+00:00"),
            "value_minimum_aporte_initial": 1000.00,
            "value_minimum_aporte_extra": 100.00,
            "entry_age": 18,
            "age_of_exit": 45,
            "lack_initial_of_rescue": 30,
            "lack_entre_resgates": 15
        }
        result_product = await insert_product(args=new_product_data)
        product_id = result_product.get("id")

        assert client_id is not None, "Client ID é None"
        assert product_id is not None, "Product ID é None"

        new_plan_data = {
            "id": str(uuid.uuid4()),
            "client_id": client_id,
            "product_id": product_id,
            "contribution": 1500.00,
            "date_of_contract": datetime.fromisoformat("2024-11-02T20:46:03.566+00:00"),
            "age_of_retirement": 65
        }
        result_plan = await insert_plan(args=new_plan_data)
        plan_id = result_plan.get("id")

        new_extra_contribution = {
            "client_id": client_id,
            "plan_id": plan_id,
            "contribution_value": 2000.00,
        }

        response = await client.post("/extra_contribuitions/create-extra-contribution/", json=new_extra_contribution)

        assert response.status_code == 201
        response_data = response.json()
        assert "id" in response_data
        assert isinstance(response_data["id"], str)


@pytest.mark.asyncio
async def test_extra_contribution_invalid_contribution_value():
    client_data = {
        "id": str(uuid.uuid4()),
        "cpf": "12345678901",
        "name": "Cliente Teste",
        "email": "cliente@teste.com",
        "date_of_birth": datetime.strptime("1990-05-15", "%Y-%m-%d").date(),
        "gender": "Feminino",
        "monthly_income": 6000.0
    }
    result_client = await insert_client(args=client_data)
    client_id = result_client.get("id")

    new_product_data = {
        "id": str(uuid.uuid4()),
        "name": "Produto Teste",
        "susep": "1234567890",
        "expiration_of_sale": datetime.fromisoformat("2025-11-02T19:30:24.117000+00:00"),
        "value_minimum_aporte_initial": 1000.00,
        "value_minimum_aporte_extra": 100.00,
        "entry_age": 18,
        "age_of_exit": 45,
        "lack_initial_of_rescue": 30,
        "lack_entre_resgates": 15
    }
    result_product = await insert_product(args=new_product_data)
    product_id = result_product.get("id")

    new_plan_data = {
        "id": str(uuid.uuid4()),
        "client_id": client_id,
        "product_id": product_id,
        "contribution": 1500.00,
        "date_of_contract": datetime.fromisoformat("2024-11-02T20:46:03.566+00:00"),
        "age_of_retirement": 65
    }

    result_plan = await insert_plan(args=new_plan_data)
    plan_id = result_plan.get("id")

    new_extra_contribution = {
            "client_id": client_id,
            "plan_id": plan_id,
            "contribution_value": 20.00,
        }

    with pytest.raises(HTTPException) as exc_info:
        result = await insert_extra_contribution(args=new_extra_contribution)
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Não é possível realizar aporte extra com valor menor que R$ 100,00."


@pytest.mark.asyncio
async def test_create_rescue_success():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8080") as client:

        # Criação do cliente
        client_data = {
            "id": str(uuid.uuid4()),
            "cpf": "12345678901",
            "name": "Cliente Teste",
            "email": "cliente@teste.com",
            "date_of_birth": datetime.strptime("1990-05-15", "%Y-%m-%d").date(),
            "gender": "Feminino",
            "monthly_income": 6000.0
        }
        result_client = await insert_client(args=client_data)
        client_id = result_client.get("id")

        new_product_data = {
            "id": str(uuid.uuid4()),
            "name": "Produto Teste",
            "susep": "1234567890",
            "expiration_of_sale": datetime.fromisoformat("2025-11-02T19:30:24.117000+00:00"),
            "value_minimum_aporte_initial": 1000.00,
            "value_minimum_aporte_extra": 100.00,
            "entry_age": 18,
            "age_of_exit": 45,
            "lack_initial_of_rescue": 60,
            "lack_entre_resgates": 30
        }
        result_product = await insert_product(args=new_product_data)
        product_id = result_product.get("id")

        assert client_id is not None, "Client ID é None"
        assert product_id is not None, "Product ID é None"

        new_plan_data = {
            "id": str(uuid.uuid4()),
            "client_id": client_id,
            "product_id": product_id,
            "contribution": 3000.00,
            "date_of_contract": datetime.fromisoformat("2024-11-02T20:46:03.566+00:00"),
            "age_of_retirement": 65
        }
        result_plan = await insert_plan(args=new_plan_data)
        plan_id = result_plan.get("id")

        new_rescue = {
            "plan_id": plan_id,
            "rescue_value": 2000.00
        }

        response = await client.post("/rescues/create-rescue/", json=new_rescue)

        assert response.status_code == 201
        response_data = response.json()
        assert "id" in response_data
        assert isinstance(response_data["id"], str)


@pytest.mark.asyncio
async def test_rescue_invalid_rescue_value():
    client_data = {
        "id": str(uuid.uuid4()),
        "cpf": "12345678901",
        "name": "Cliente Teste",
        "email": "cliente@teste.com",
        "date_of_birth": datetime.strptime("1990-05-15", "%Y-%m-%d").date(),
        "gender": "Feminino",
        "monthly_income": 6000.0
    }
    result_client = await insert_client(args=client_data)
    client_id = result_client.get("id")

    new_product_data = {
        "id": str(uuid.uuid4()),
        "name": "Produto Teste",
        "susep": "1234567890",
        "expiration_of_sale": datetime.fromisoformat("2025-11-02T19:30:24.117000+00:00"),
        "value_minimum_aporte_initial": 1000.00,
        "value_minimum_aporte_extra": 100.00,
        "entry_age": 18,
        "age_of_exit": 45,
        "lack_initial_of_rescue": 60,
        "lack_entre_resgates": 30
    }
    result_product = await insert_product(args=new_product_data)
    product_id = result_product.get("id")

    new_plan_data = {
        "id": str(uuid.uuid4()),
        "client_id": client_id,
        "product_id": product_id,
        "contribution": 1500.00,
        "date_of_contract": datetime.fromisoformat("2024-11-02T20:46:03.566+00:00"),
        "age_of_retirement": 65
    }

    result_plan = await insert_plan(args=new_plan_data)
    plan_id = result_plan.get("id")

    new_rescue = {
            "plan_id": plan_id,
            "rescue_value": 2000.00,
        }

    with pytest.raises(HTTPException) as exc_info:
        result = await insert_rescue(args=new_rescue)
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail ==  "Não há saldo suficiente para resgatar o valor informado."


@pytest.mark.asyncio
async def test_rescue_invalid_initial_lack():
    client_data = {
        "id": str(uuid.uuid4()),
        "cpf": "12345678901",
        "name": "Cliente Teste",
        "email": "cliente@teste.com",
        "date_of_birth": datetime.strptime("1990-05-15", "%Y-%m-%d").date(),
        "gender": "Feminino",
        "monthly_income": 6000.0
    }
    result_client = await insert_client(args=client_data)
    client_id = result_client.get("id")

    new_product_data = {
        "id": str(uuid.uuid4()),
        "name": "Produto Teste",
        "susep": "1234567890",
        "expiration_of_sale": datetime.fromisoformat("2025-11-02T19:30:24.117000+00:00"),
        "value_minimum_aporte_initial": 1000.00,
        "value_minimum_aporte_extra": 100.00,
        "entry_age": 18,
        "age_of_exit": 45,
        "lack_initial_of_rescue": 30,
        "lack_entre_resgates": 30
    }
    result_product = await insert_product(args=new_product_data)
    product_id = result_product.get("id")

    new_plan_data = {
        "id": str(uuid.uuid4()),
        "client_id": client_id,
        "product_id": product_id,
        "contribution": 15500.00,
        "date_of_contract": datetime.fromisoformat("2024-11-02T20:46:03.566+00:00"),
        "age_of_retirement": 65
    }

    result_plan = await insert_plan(args=new_plan_data)
    plan_id = result_plan.get("id")

    new_rescue = {
            "plan_id": plan_id,
            "rescue_value": 2000.00,
        }

    with pytest.raises(HTTPException) as exc_info:
        result = await insert_rescue(args=new_rescue)
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Carência inicial de resgate de 60 dias não foi cumprida."
    