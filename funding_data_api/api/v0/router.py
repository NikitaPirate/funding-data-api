from fastapi import APIRouter

from funding_data_api.api.v0.meta import router as meta_router

router = APIRouter(prefix="/api/v0")

router.include_router(meta_router)
