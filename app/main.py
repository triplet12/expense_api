from fastapi import FastAPI

from .routers import categories, expenses, report


app = FastAPI()
app.include_router(categories.router)
app.include_router(expenses.router)
app.include_router(report.router)


@app.get("/health")
async def alive():
    return {"status": "ok"}
