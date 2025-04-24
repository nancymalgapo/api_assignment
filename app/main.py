from fastapi import FastAPI

from app.routers.router import router
from app.constants import APP_TITLE, APP_DESCRIPTION

app = FastAPI(
    title=APP_TITLE,
    docs_url="/",
    description=APP_DESCRIPTION
    )

app.include_router(router=router)
