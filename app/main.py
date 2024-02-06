import uvicorn
from app.api.v1.router import api_router
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI

app = FastAPI(title="FastAPI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api_router, prefix="/api")
@app.get("/",tags=["Home Page"])
def home():
    return {"Welcome": "Welcome to the FastAPI CI CD"}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10052)