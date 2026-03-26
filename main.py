from fastapi import FastAPI
from api.routes import vehicles, status, ticks, queue, pumps, transactions
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(vehicles.router)
app.include_router(status.router)
app.include_router(ticks.router)
app.include_router(transactions.router)
app.include_router(pumps.router)
app.include_router(queue.router)
