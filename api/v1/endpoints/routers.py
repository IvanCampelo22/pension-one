from fastapi.routing import APIRouter
from api.v1.endpoints import client
from api.v1.endpoints import products
from api.v1.endpoints import plan
from api.v1.endpoints import extra_contribuition
from api.v1.endpoints import rescue
from api.v1.endpoints import websockets

api_router = APIRouter()


api_router.include_router(client.router, prefix='/clients', tags=['clients'])
api_router.include_router(products.router, prefix='/products', tags=['products'])
api_router.include_router(plan.router, prefix='/plans', tags=['plans'])
api_router.include_router(extra_contribuition.router, prefix='/extra_contribuitions', tags=['extra_contribuitions'])
api_router.include_router(rescue.router, prefix='/rescues', tags=['rescues'])
api_router.include_router(websockets.router, prefix='/websockets', tags=['websockets'])