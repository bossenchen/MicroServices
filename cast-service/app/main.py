from fastapi import FastAPI
from .api.casts import casts
from .api.db import metadata, database, engine
from fastapi.middleware.cors import CORSMiddleware


metadata.create_all(engine)

app = FastAPI(
    openapi_url="/api/v1/casts/openapi.json",
    docs_url="/api/v1/casts/docs"
)

origins = [
    'http://localhost:*',
    'https://localhost:*'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[
        '*'
    ],
    allow_headers=[
        '*'
    ]
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(casts, prefix='/api/v1/casts', tags=['casts'])
