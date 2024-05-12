import logging
import subprocess
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api import v1_router
from src.core.config import config, LOG_FORMAT

logging.basicConfig(level=config.log_level, format=LOG_FORMAT)


@asynccontextmanager
async def lifespan(app: FastAPI):
    '''
    Creates migrations in DB on app startup
    '''
    subprocess.run(['alembic', 'upgrade', 'head']).check_returncode()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(v1_router, prefix='/api/v1')
