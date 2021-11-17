from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], #특정한 HTTP method 혹은 '*'(= wildcard = 아무 값)
    allow_headers=["*"], #특정한 HTTP hearder 혹은 '*'(= wildcard = 아무 값)
)

@app.get("/")
async def main():
    return {"message": "Hello World"}
