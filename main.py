from fastapi import FastAPI, status
from pydantic import BaseModel
from src.book import book_router
from src.db.main import init_db

app = FastAPI(
    version="1.0",
)

@app.on_event("startup")
async def startup():
    print("Server is Starting...")
    await init_db()


@app.on_event("shutdown")
async def shutdown():
    print("Server Shutdown")


class HealthCheckResponse(BaseModel):
    success: bool
    message: str

@app.get("/health", status_code=status.HTTP_200_OK, response_model=HealthCheckResponse, tags=["health"])
def health_check() -> HealthCheckResponse:
    return {
        "success" : True,
        "message" : "Server is Healthy"
    }

app.include_router(book_router, prefix="/books", tags=["books"])
