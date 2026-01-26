from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from funding_data_api.api.v0.router import router as v0_router
from funding_data_api.db import engine
from funding_data_api.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manages application lifecycle."""
    # Startup: engine already initialized in db.py

    yield

    # Shutdown: dispose engine
    await engine.dispose()


app = FastAPI(title="Funding Data API", lifespan=lifespan)

# CORS middleware
app.add_middleware(CORSMiddleware, **settings.cors.to_middleware_kwargs())  # type: ignore[arg-type]

app.include_router(v0_router)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
