import uvicorn
from fastapi import FastAPI

from app.infra.web.router import setup_routers

app = FastAPI()
setup_routers(app)

@app.get("/")
def hello_world() -> dict[str, str]:
    return {"message": "Hello, ToDAM Ticket System!"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
    )
