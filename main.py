from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import auth, game_order

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="My Game Order API",
    description="An API for managing game orders",
    version="1.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Support Team",
        "url": "http://example.com/contact/",
        "email": "ehsan.moradi.it@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

app.include_router(game_order.router)
app.include_router(auth.router)
