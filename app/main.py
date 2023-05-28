from fastapi import FastAPI

from app.routes.analysis_route import router as analysis_route

app = FastAPI(
    title="IntelliDent API",
    description="API para la aplicación IntelliDent",
    version="1.0.0"
)

app.include_router(analysis_route)


@app.get("/")
async def root():
    return {
        "message": "Bienvenido a IntelliDent API",
        "version": "1.0.0",
        "author": "Jorge Gustavo Banegas Melgar",
        "email": "jorge.g.banegas@gmail.com"
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host='0.0.0.0', port=8000, reload=True)
